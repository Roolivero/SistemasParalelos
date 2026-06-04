"""Implementacion PyTorch CPU/GPU para RGB->gris y Sobel."""

from __future__ import annotations

import torch
import torch.nn.functional as F


SOBEL_X = torch.tensor(
    [[[[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]]]],
    dtype=torch.float32,
)
SOBEL_Y = torch.tensor(
    [[[[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]]]],
    dtype=torch.float32,
)


def set_torch_workers(workers: int | None) -> int:
    """Configura hilos de PyTorch CPU y devuelve la cantidad efectiva."""
    if workers is not None:
        if workers < 1:
            raise ValueError("--workers debe ser >= 1")
        torch.set_num_threads(workers)
    return int(torch.get_num_threads())


def ensure_torch_cuda_available() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA no esta disponible para PyTorch en este entorno")


def sobel_kernels(device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    return SOBEL_X.to(device), SOBEL_Y.to(device)


def rgb_to_gray_torch(rgb: torch.Tensor) -> torch.Tensor:
    """Convierte RGB HxWx3 a gris uint8 usando operaciones sobre tensores."""
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("La imagen RGB debe tener forma HxWx3")

    rgb_f = rgb.to(torch.float32)
    gray = 0.299 * rgb_f[:, :, 0] + 0.587 * rgb_f[:, :, 1] + 0.114 * rgb_f[:, :, 2]
    return gray.clamp(0.0, 255.0).to(torch.uint8)


def sobel_torch(gray: torch.Tensor, kernel_x: torch.Tensor, kernel_y: torch.Tensor) -> torch.Tensor:
    """Aplica Sobel con conv2d, dejando los bordes en cero como las otras versiones."""
    if gray.ndim != 2:
        raise ValueError("La imagen en gris debe ser una matriz 2D")

    height, width = gray.shape
    out = torch.zeros((height, width), dtype=torch.uint8, device=gray.device)
    if height < 3 or width < 3:
        return out

    image = gray.to(torch.float32).unsqueeze(0).unsqueeze(0)
    gx = F.conv2d(image, kernel_x)
    gy = F.conv2d(image, kernel_y)
    magnitude = torch.sqrt(gx * gx + gy * gy).clamp(0.0, 255.0)
    out[1:-1, 1:-1] = magnitude.squeeze(0).squeeze(0).to(torch.uint8)
    return out


def warmup_pytorch_cpu() -> None:
    """Ejecuta una prueba minima para estabilizar overhead inicial."""
    device = torch.device("cpu")
    rgb = torch.zeros((4, 4, 3), dtype=torch.uint8, device=device)
    kernel_x, kernel_y = sobel_kernels(device)
    gray = rgb_to_gray_torch(rgb)
    sobel_torch(gray, kernel_x, kernel_y)


def warmup_pytorch_gpu() -> None:
    """Ejecuta una prueba minima en CUDA fuera de la medicion."""
    ensure_torch_cuda_available()
    device = torch.device("cuda")
    rgb = torch.zeros((4, 4, 3), dtype=torch.uint8, device=device)
    kernel_x, kernel_y = sobel_kernels(device)
    gray = rgb_to_gray_torch(rgb)
    sobel_torch(gray, kernel_x, kernel_y)
    torch.cuda.synchronize()
