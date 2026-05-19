# Resultados Sobel 6000x6000

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.47 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 5.243595 | 17.420171 | 22.663766 | 0.000000 | 1.000000 | 100.000000 |
| NumPy | 0.130965 | 0.280494 | 0.411459 | 0.000000 | 55.081437 | 5508.143742 |
| Numba paralelo CPU | 0.015806 | 0.016697 | 0.032503 | 0.000000 | 697.283841 | 11621.397342 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 6000x6000 | 5 | 1 | 2026 | 0 | 36000000 | 109936717 | d8af6b4c711617e3 | ok |
| NumPy | 6000x6000 | 5 | 1 | 2026 | 0 | 36000000 | 109935099 | 58d0001f7448e5ed | ok |
| Numba paralelo CPU | 6000x6000 | 5 | 6 | 2026 | 0 | 36000000 | 109936717 | d8af6b4c711617e3 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.014300 | 0.012934 | 0.027233 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 2 | 0.016472 | 0.021504 | 0.037975 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 3 | 0.015762 | 0.017439 | 0.033201 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 4 | 0.016448 | 0.013929 | 0.030377 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 5 | 0.016049 | 0.017678 | 0.033728 | 0.000000 | 109936717 | d8af6b4c711617e3 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
