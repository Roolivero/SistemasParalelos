# Resultado parcial Sobel 1500x1500 - Numba GPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.76 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba GPU | 0.000430 | 0.001081 | 0.001511 | 0.059956 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba GPU | 1500x1500 | 5 | 256 | 2026 | 1349 | 2250000 | 18014475 | 82629d16e7e25f5c | ok |

## Detalle de corridas

### Numba GPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.000523 | 0.001087 | 0.001609 | 0.059956 | 18014475 | 82629d16e7e25f5c |
| 2 | 0.000413 | 0.001082 | 0.001495 | 0.059956 | 18014475 | 82629d16e7e25f5c |
| 3 | 0.000414 | 0.001078 | 0.001492 | 0.059956 | 18014475 | 82629d16e7e25f5c |
| 4 | 0.000407 | 0.001079 | 0.001486 | 0.059956 | 18014475 | 82629d16e7e25f5c |
| 5 | 0.000396 | 0.001080 | 0.001475 | 0.059956 | 18014475 | 82629d16e7e25f5c |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo. No se suman en la columna de tiempo total solicitada, que mide solamente conversion RGB->gris y Sobel.

| metodo | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---|---:|---:|---:|---:|---:|
| Numba GPU | 0.001302 | 0.000682 | 0.001984 | 0.001511 | 0.003495 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
