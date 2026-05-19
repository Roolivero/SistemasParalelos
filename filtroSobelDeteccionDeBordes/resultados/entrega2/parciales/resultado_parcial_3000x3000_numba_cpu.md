# Resultado parcial Sobel 3000x3000 - Numba paralelo CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.75 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.003457 | 0.004141 | 0.007598 | 0.001367 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba paralelo CPU | 3000x3000 | 5 | 6 | 2026 | 123 | 9000000 | 47883925 | a5989d2f439a9154 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.005790 | 0.004203 | 0.009992 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 2 | 0.003790 | 0.003858 | 0.007648 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 3 | 0.002547 | 0.004236 | 0.006784 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 4 | 0.002584 | 0.004207 | 0.006791 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 5 | 0.002573 | 0.004203 | 0.006776 | 0.001367 | 47883925 | a5989d2f439a9154 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
