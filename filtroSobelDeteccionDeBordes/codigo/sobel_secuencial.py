"""Implementacion secuencial pura del filtro de Sobel.

La entrada RGB se recibe como bytes planos en orden H x W x 3.
No usa NumPy ni vectorizacion dentro de la conversion ni dentro de Sobel.
"""


def rgb_to_gray_sequential(rgb: bytes | bytearray, height: int, width: int) -> bytearray:
    """Convierte RGB a gris con luminancia, usando bucles Python."""
    total_pixels = height * width
    expected_len = total_pixels * 3
    if len(rgb) != expected_len:
        raise ValueError(f"RGB invalido: se esperaban {expected_len} bytes y llegaron {len(rgb)}")

    gray = bytearray(total_pixels)
    src_index = 0
    for pixel_index in range(total_pixels):
        r = rgb[src_index]
        g = rgb[src_index + 1]
        b = rgb[src_index + 2]
        value = int(0.299 * r + 0.587 * g + 0.114 * b)
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        gray[pixel_index] = value
        src_index += 3
    return gray


def sobel_sequential(gray: bytes | bytearray, height: int, width: int) -> bytearray:
    """Aplica Sobel con sqrt(gx^2 + gy^2), recorriendo solo pixeles interiores."""
    total_pixels = height * width
    if len(gray) != total_pixels:
        raise ValueError(f"Gris invalido: se esperaban {total_pixels} bytes y llegaron {len(gray)}")

    out = bytearray(total_pixels)

    for row in range(1, height - 1):
        prev_row = (row - 1) * width
        curr_row = row * width
        next_row = (row + 1) * width

        for col in range(1, width - 1):
            p00 = gray[prev_row + col - 1]
            p01 = gray[prev_row + col]
            p02 = gray[prev_row + col + 1]
            p10 = gray[curr_row + col - 1]
            p12 = gray[curr_row + col + 1]
            p20 = gray[next_row + col - 1]
            p21 = gray[next_row + col]
            p22 = gray[next_row + col + 1]

            gx = -p00 + p02 - 2 * p10 + 2 * p12 - p20 + p22
            gy = p00 + 2 * p01 + p02 - p20 - 2 * p21 - p22
            grad = (gx * gx + gy * gy) ** 0.5

            if grad > 255.0:
                out[curr_row + col] = 255
            else:
                out[curr_row + col] = int(grad)

    return out
