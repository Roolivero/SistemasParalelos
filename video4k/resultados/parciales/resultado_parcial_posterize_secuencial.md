# Resultado parcial TP4 posterize - secuencial

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.26 GiB disponible
- Sistema operativo: Linux-6.18.33-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.12.13 | packaged by conda-forge | (main, Mar  5 2026, 16:50:00) [GCC 14.3.0]
- NumPy: 2.4.6
- OpenCV: 4.13.0
- PyTorch: 2.11.0+cu128
- PyTorch CUDA: NVIDIA GeForce RTX 2060 (CUDA 12.8)

## Filtro

Filtro elegido: posterize pop-art por luminancia con paleta fija.

| rango de luminancia | color | RGB |
|---|---|---|
| 0-63 | verde | `(27, 127, 58)` |
| 64-127 | fucsia | `(232, 62, 140)` |
| 128-191 | amarillo | `(255, 216, 77)` |
| 192-255 | blanco | `(255, 255, 255)` |

## Tabla de benchmark

| metodo | frames | resolucion | fps original | lectura/decodif. (s) | filtrado (s) | escritura/codif. (s) | total pipeline (s) | FPS efectivos | speed-up | memoria pico (MB) | estado |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| secuencial | 944 | 2160x3840 | 29.970 | 5.535483 | 1526.403864 | 56.960685 | 1588.900032 | 0.594127 | 1.000000 | 1321.81 | ok |

## Datos de control

| metodo | corridas | workers | duracion video (s) | codec | max_frames | checksum | hash salida | video sin audio | video con audio |
|---|---:|---:|---:|---|---:|---:|---|---|---|
| secuencial | 3 | 1 | 31.498133 | mp4v |  | 3753312782835 | e81551eaad55d3c5 | /home/ro/Desktop/facu/SistemasParalelos/video4k/resultados/videos/posterize_secuencial_sin_audio.mp4 |  |

## Notas metodologicas

- El video se procesa como flujo: no se carga completo en memoria.
- El tiempo de pipeline es lectura/decodificacion + filtrado + escritura/codificacion.
- El video original no tiene una pista de audio detectable; se conserva la salida procesada sin audio.
- Speed-up = tiempo total del pipeline secuencial / tiempo total del pipeline del metodo.
- Si falta la fila secuencial, el speed-up queda vacio porque falta la linea base.
