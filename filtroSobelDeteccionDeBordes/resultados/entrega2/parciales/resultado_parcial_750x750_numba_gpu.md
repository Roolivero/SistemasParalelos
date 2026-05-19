# Resultado parcial Sobel 750x750 - Numba GPU

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
| Numba GPU | 0.000138 | 0.000303 | 0.000441 | 0.281778 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba GPU | 750x750 | 5 | 256 | 2026 | 1585 | 562500 | 7145141 | 5d84e47f0fe8922a | ok |

## Detalle de corridas

### Numba GPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.000148 | 0.000302 | 0.000450 | 0.281778 | 7145141 | 5d84e47f0fe8922a |
| 2 | 0.000108 | 0.000327 | 0.000436 | 0.281778 | 7145141 | 5d84e47f0fe8922a |
| 3 | 0.000226 | 0.000295 | 0.000521 | 0.281778 | 7145141 | 5d84e47f0fe8922a |
| 4 | 0.000106 | 0.000295 | 0.000401 | 0.281778 | 7145141 | 5d84e47f0fe8922a |
| 5 | 0.000103 | 0.000294 | 0.000397 | 0.281778 | 7145141 | 5d84e47f0fe8922a |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo. No se suman en la columna de tiempo total solicitada, que mide solamente conversion RGB->gris y Sobel.

| metodo | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---|---:|---:|---:|---:|---:|
| Numba GPU | 0.000598 | 0.000213 | 0.000811 | 0.000441 | 0.001252 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
