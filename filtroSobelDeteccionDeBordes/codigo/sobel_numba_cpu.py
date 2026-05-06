"""Implementacion Numba paralelo CPU para RGB->gris y Sobel."""

import numpy as np
from numba import get_num_threads, njit, prange, set_num_threads


@njit(cache=True, parallel=True, fastmath=False)  # type: ignore[misc]
def _rgb_to_gray_numba_kernel(rgb: np.ndarray, gray: np.ndarray) -> None:
    height = rgb.shape[0]
    width = rgb.shape[1]
    for row in prange(height):
        for col in range(width):
            r = float(rgb[row, col, 0])
            g = float(rgb[row, col, 1])
            b = float(rgb[row, col, 2])
            value = int(0.299 * r + 0.587 * g + 0.114 * b)
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            gray[row, col] = value


@njit(cache=True, parallel=True, fastmath=False)  # type: ignore[misc]
def _sobel_numba_kernel(gray: np.ndarray, out: np.ndarray) -> None:
    height = gray.shape[0]
    width = gray.shape[1]

    for row in prange(1, height - 1):
        for col in range(1, width - 1):
            p00 = float(gray[row - 1, col - 1])
            p01 = float(gray[row - 1, col])
            p02 = float(gray[row - 1, col + 1])
            p10 = float(gray[row, col - 1])
            p12 = float(gray[row, col + 1])
            p20 = float(gray[row + 1, col - 1])
            p21 = float(gray[row + 1, col])
            p22 = float(gray[row + 1, col + 1])

            gx = -p00 + p02 - 2.0 * p10 + 2.0 * p12 - p20 + p22
            gy = p00 + 2.0 * p01 + p02 - p20 - 2.0 * p21 - p22
            grad = (gx * gx + gy * gy) ** 0.5

            if grad > 255.0:
                out[row, col] = 255
            else:
                out[row, col] = int(grad)


def set_numba_workers(workers: int | None) -> int:
    """Configura hilos de Numba y devuelve la cantidad efectiva."""
    if workers is not None:
        if workers < 1:
            raise ValueError("--workers debe ser >= 1")
        set_num_threads(workers)
    return int(get_num_threads())


def warmup_numba() -> None:
    """Compila kernels con una imagen minima; esta llamada no se mide."""
    rgb = np.zeros((4, 4, 3), dtype=np.uint8)
    gray = np.empty((4, 4), dtype=np.uint8)
    out = np.zeros((4, 4), dtype=np.uint8)
    _rgb_to_gray_numba_kernel(rgb, gray)
    _sobel_numba_kernel(gray, out)


def rgb_to_gray_numba(rgb: np.ndarray) -> np.ndarray:
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("La imagen RGB debe tener forma HxWx3")
    gray = np.empty(rgb.shape[:2], dtype=np.uint8)
    _rgb_to_gray_numba_kernel(rgb, gray)
    return gray


def sobel_numba(gray: np.ndarray) -> np.ndarray:
    if gray.ndim != 2:
        raise ValueError("La imagen en gris debe ser una matriz 2D")
    out = np.zeros(gray.shape, dtype=np.uint8)
    _sobel_numba_kernel(gray, out)
    return out
