# Resultado parcial Sobel 6000x6000 - Numba GPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.67 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba GPU | 0.003973 | 0.017432 | 0.021405 | 0.000000 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba GPU | 6000x6000 | 5 | 256 | 2026 | 0 | 36000000 | 109937633 | 72c64699d639c009 | ok |

## Detalle de corridas

### Numba GPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.003993 | 0.017401 | 0.021394 | 0.000000 | 109937633 | 72c64699d639c009 |
| 2 | 0.004070 | 0.017670 | 0.021740 | 0.000000 | 109937633 | 72c64699d639c009 |
| 3 | 0.004045 | 0.017033 | 0.021078 | 0.000000 | 109937633 | 72c64699d639c009 |
| 4 | 0.003698 | 0.017387 | 0.021085 | 0.000000 | 109937633 | 72c64699d639c009 |
| 5 | 0.004058 | 0.017668 | 0.021726 | 0.000000 | 109937633 | 72c64699d639c009 |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo. No se suman en la columna de tiempo total solicitada, que mide solamente conversion RGB->gris y Sobel.

| metodo | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---|---:|---:|---:|---:|---:|
| Numba GPU | 0.011006 | 0.005107 | 0.016113 | 0.021405 | 0.037518 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
