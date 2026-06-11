"""Filtro posterize pop-art para frames BGR de OpenCV.

El video se lee con OpenCV, por eso los frames llegan en orden BGR.
La paleta se define una sola vez y se usa igual en todas las versiones.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol

import numpy as np


METHOD_LABELS = {
    "secuencial": "secuencial",
    "pytorch_cpu": "PyTorch CPU",
    "pytorch_gpu": "PyTorch GPU",
}

# Paleta elegida para el TP4. Los nombres se documentan en RGB, pero OpenCV
# escribe frames BGR, por eso tambien se guarda la version invertida.
PALETTE_RGB = {
    "verde": (27, 127, 58),
    "fucsia": (232, 62, 140),
    "amarillo": (255, 216, 77),
    "blanco": (255, 255, 255),
}

PALETTE_ORDER = ("verde", "fucsia", "amarillo", "blanco")
PALETTE_BGR = tuple(
    (PALETTE_RGB[name][2], PALETTE_RGB[name][1], PALETTE_RGB[name][0])
    for name in PALETTE_ORDER
)


@dataclass
class FilterTiming:
    filter_s: float
    compute_s: float
    transfer_h2d_s: float | None = None
    transfer_d2h_s: float | None = None

    @property
    def transfer_total_s(self) -> float | None:
        if self.transfer_h2d_s is None and self.transfer_d2h_s is None:
            return None
        return (self.transfer_h2d_s or 0.0) + (self.transfer_d2h_s or 0.0)


class PosterizeProcessor(Protocol):
    method_key: str
    method_label: str
    workers: int

    def process(self, frame_bgr: np.ndarray) -> tuple[np.ndarray, FilterTiming]:
        """Devuelve el frame filtrado y los tiempos de la etapa de filtrado."""


def _validate_frame(frame_bgr: np.ndarray) -> None:
    if frame_bgr.ndim != 3 or frame_bgr.shape[2] != 3:
        raise ValueError("El frame debe tener forma HxWx3")
    if frame_bgr.dtype != np.uint8:
        raise ValueError("El frame debe ser uint8")


def _palette_index_from_luminance(luminance: int) -> int:
    if luminance < 64:
        return 0
    if luminance < 128:
        return 1
    if luminance < 192:
        return 2
    return 3


def posterize_sequential_bgr(frame_bgr: np.ndarray) -> np.ndarray:
    """Version secuencial pura: recorre cada pixel con bucles de Python."""
    _validate_frame(frame_bgr)
    height, width, _ = frame_bgr.shape
    raw = frame_bgr.tobytes()
    out = bytearray(len(raw))

    for offset in range(0, len(raw), 3):
        b = raw[offset]
        g = raw[offset + 1]
        r = raw[offset + 2]

        # Luminancia estandar expresada con enteros para que secuencial y
        # PyTorch clasifiquen igual en los limites de cada rango.
        luminance = (299 * r + 587 * g + 114 * b) // 1000
        palette_index = _palette_index_from_luminance(luminance)
        out_b, out_g, out_r = PALETTE_BGR[palette_index]

        out[offset] = out_b
        out[offset + 1] = out_g
        out[offset + 2] = out_r

    return np.frombuffer(out, dtype=np.uint8).reshape((height, width, 3)).copy()


class SequentialPosterize:
    method_key = "secuencial"
    method_label = METHOD_LABELS[method_key]
    workers = 1

    def process(self, frame_bgr: np.ndarray) -> tuple[np.ndarray, FilterTiming]:
        start = perf_counter()
        out = posterize_sequential_bgr(frame_bgr)
        elapsed = perf_counter() - start
        return out, FilterTiming(filter_s=elapsed, compute_s=elapsed)


class TorchPosterizeCPU:
    method_key = "pytorch_cpu"
    method_label = METHOD_LABELS[method_key]

    def __init__(self, workers: int | None = None) -> None:
        import torch

        self.torch = torch
        if workers is not None:
            if workers < 1:
                raise ValueError("--workers debe ser >= 1")
            torch.set_num_threads(workers)
        self.workers = int(torch.get_num_threads())
        self.palette = torch.tensor(PALETTE_BGR, dtype=torch.uint8, device="cpu")

    def process(self, frame_bgr: np.ndarray) -> tuple[np.ndarray, FilterTiming]:
        _validate_frame(frame_bgr)
        start = perf_counter()
        with self.torch.no_grad():
            frame = self.torch.from_numpy(frame_bgr).to(dtype=self.torch.int32)
            out = posterize_tensor_bgr(frame, self.palette, self.torch)
            out_host = out.numpy().copy()
        elapsed = perf_counter() - start
        return out_host, FilterTiming(filter_s=elapsed, compute_s=elapsed)


class TorchPosterizeGPU:
    method_key = "pytorch_gpu"
    method_label = METHOD_LABELS[method_key]
    workers = 1

    def __init__(self) -> None:
        import torch

        if not torch.cuda.is_available():
            raise RuntimeError("CUDA no esta disponible para PyTorch en este entorno")
        self.torch = torch
        self.device = torch.device("cuda")
        self.palette = torch.tensor(PALETTE_BGR, dtype=torch.uint8, device=self.device)

        # Warmup fuera de la medicion real.
        sample = torch.zeros((4, 4, 3), dtype=torch.uint8, device=self.device)
        posterize_tensor_bgr(sample.to(dtype=torch.int32), self.palette, torch)
        torch.cuda.synchronize()

    def process(self, frame_bgr: np.ndarray) -> tuple[np.ndarray, FilterTiming]:
        _validate_frame(frame_bgr)

        transfer_in_start = perf_counter()
        with self.torch.no_grad():
            frame_device = self.torch.from_numpy(frame_bgr).to(self.device, dtype=self.torch.int32)
        self.torch.cuda.synchronize()
        transfer_h2d_s = perf_counter() - transfer_in_start

        compute_start = perf_counter()
        with self.torch.no_grad():
            out_device = posterize_tensor_bgr(frame_device, self.palette, self.torch)
        self.torch.cuda.synchronize()
        compute_s = perf_counter() - compute_start

        transfer_out_start = perf_counter()
        out_host = out_device.cpu().numpy().copy()
        self.torch.cuda.synchronize()
        transfer_d2h_s = perf_counter() - transfer_out_start

        return out_host, FilterTiming(
            filter_s=transfer_h2d_s + compute_s + transfer_d2h_s,
            compute_s=compute_s,
            transfer_h2d_s=transfer_h2d_s,
            transfer_d2h_s=transfer_d2h_s,
        )


def posterize_tensor_bgr(frame_bgr, palette_bgr, torch_module):
    """Posterize para tensores HxWx3 en BGR.

    La luminancia usa la misma formula entera que la version secuencial:
    (299R + 587G + 114B) // 1000.
    """
    b = frame_bgr[:, :, 0]
    g = frame_bgr[:, :, 1]
    r = frame_bgr[:, :, 2]
    luminance = (299 * r + 587 * g + 114 * b) // 1000
    indices = torch_module.clamp(luminance // 64, min=0, max=3).to(dtype=torch_module.long)
    return palette_bgr[indices]


def build_processor(method_key: str, workers: int | None = None) -> PosterizeProcessor:
    if method_key == "secuencial":
        return SequentialPosterize()
    if method_key == "pytorch_cpu":
        return TorchPosterizeCPU(workers=workers)
    if method_key == "pytorch_gpu":
        return TorchPosterizeGPU()
    valid = ", ".join(METHOD_LABELS)
    raise ValueError(f"Metodo invalido: {method_key}. Validos: {valid}")
