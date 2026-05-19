# Resultado parcial Sobel 3000x3000 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.57 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.033103 | 0.073703 | 0.106806 | 0.001367 | 53.540383 | 5354.038307 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 3000x3000 | 5 | 1 | 2026 | 123 | 9000000 | 47883024 | a92d650778fbd8bf | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.035098 | 0.072960 | 0.108057 | 0.001367 | 47883024 | a92d650778fbd8bf |
| 2 | 0.032486 | 0.076452 | 0.108938 | 0.001367 | 47883024 | a92d650778fbd8bf |
| 3 | 0.033175 | 0.070216 | 0.103391 | 0.001367 | 47883024 | a92d650778fbd8bf |
| 4 | 0.032482 | 0.074099 | 0.106581 | 0.001367 | 47883024 | a92d650778fbd8bf |
| 5 | 0.032276 | 0.074788 | 0.107065 | 0.001367 | 47883024 | a92d650778fbd8bf |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
