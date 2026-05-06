"""Implementacion vectorizada con NumPy para RGB->gris y Sobel."""

import numpy as np


def rgb_to_gray_numpy(rgb: np.ndarray) -> np.ndarray:
    """Convierte una imagen RGB HxWx3 a gris uint8 con operaciones NumPy."""
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("La imagen RGB debe tener forma HxWx3")

    acc = np.empty(rgb.shape[:2], dtype=np.float32)
    tmp = np.empty_like(acc)

    np.multiply(rgb[:, :, 0], 0.299, out=acc, casting="unsafe")
    np.multiply(rgb[:, :, 1], 0.587, out=tmp, casting="unsafe")
    acc += tmp
    np.multiply(rgb[:, :, 2], 0.114, out=tmp, casting="unsafe")
    acc += tmp
    np.clip(acc, 0.0, 255.0, out=acc)
    return acc.astype(np.uint8)


def sobel_numpy(gray: np.ndarray) -> np.ndarray:
    """Aplica Sobel usando cortes de NumPy para las 9 posiciones de la vecindad 3x3."""
    if gray.ndim != 2:
        raise ValueError("La imagen en gris debe ser una matriz 2D")

    image = gray.astype(np.float32)
    height, width = image.shape
    out = np.zeros((height, width), dtype=np.uint8)
    if height < 3 or width < 3:
        return out

    top_left = image[:-2, :-2]
    top = image[:-2, 1:-1]
    top_right = image[:-2, 2:]
    left = image[1:-1, :-2]
    right = image[1:-1, 2:]
    bottom_left = image[2:, :-2]
    bottom = image[2:, 1:-1]
    bottom_right = image[2:, 2:]

    gx = np.empty_like(top)
    gy = np.empty_like(top)

    # Gx = -TL + TR - 2L + 2R - BL + BR
    np.subtract(top_right, top_left, out=gx)
    gx -= left
    gx -= left
    gx += right
    gx += right
    gx -= bottom_left
    gx += bottom_right

    # Gy = TL + 2T + TR - BL - 2B - BR
    np.add(top_left, top_right, out=gy)
    gy += top
    gy += top
    gy -= bottom_left
    gy -= bottom
    gy -= bottom
    gy -= bottom_right

    np.multiply(gx, gx, out=gx)
    np.multiply(gy, gy, out=gy)
    gx += gy
    np.sqrt(gx, out=gx)
    np.clip(gx, 0.0, 255.0, out=gx)

    out[1:-1, 1:-1] = gx.astype(np.uint8)
    return out
