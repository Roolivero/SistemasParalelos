"""Implementacion Numba GPU para RGB->gris y Sobel.

Esta version sigue el modelo CUDA visto en la consigna: una grilla 2D de
bloques/hilos y un hilo por pixel.
"""

import math

import numpy as np
from numba import cuda


THREADS_PER_BLOCK = (16, 16)


@cuda.jit
def rgb_to_gray_cuda(rgb: np.ndarray, gray: np.ndarray) -> None:
    row, col = cuda.grid(2)
    height = rgb.shape[0]
    width = rgb.shape[1]
    if row >= height or col >= width:
        return

    r = float(rgb[row, col, 0])
    g = float(rgb[row, col, 1])
    b = float(rgb[row, col, 2])
    value = int(0.299 * r + 0.587 * g + 0.114 * b)

    if value < 0:
        value = 0
    elif value > 255:
        value = 255
    gray[row, col] = value


@cuda.jit
def sobel_cuda(gray: np.ndarray, out: np.ndarray) -> None:
    row, col = cuda.grid(2)
    height = gray.shape[0]
    width = gray.shape[1]
    if row >= height or col >= width:
        return
    if row == 0 or col == 0 or row == height - 1 or col == width - 1:
        out[row, col] = 0
        return

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
    mag = int(math.sqrt(gx * gx + gy * gy))

    out[row, col] = 255 if mag > 255 else mag


def blocks_per_grid(height: int, width: int) -> tuple[int, int]:
    threads_y, threads_x = THREADS_PER_BLOCK
    blocks_y = (height + threads_y - 1) // threads_y
    blocks_x = (width + threads_x - 1) // threads_x
    return blocks_y, blocks_x


def ensure_cuda_available() -> None:
    if not cuda.is_available():
        raise RuntimeError("CUDA no esta disponible para Numba en este entorno")


def warmup_numba_gpu() -> None:
    """Compila kernels y ejecuta una prueba minima fuera de la medicion."""
    ensure_cuda_available()
    rgb_host = np.zeros((4, 4, 3), dtype=np.uint8)
    rgb_device = cuda.to_device(rgb_host)
    gray_device = cuda.device_array((4, 4), dtype=np.uint8)
    sobel_device = cuda.device_array((4, 4), dtype=np.uint8)
    blocks = blocks_per_grid(4, 4)
    rgb_to_gray_cuda[blocks, THREADS_PER_BLOCK](rgb_device, gray_device)
    sobel_cuda[blocks, THREADS_PER_BLOCK](gray_device, sobel_device)
    cuda.synchronize()
