# Resultado parcial Sobel 1500x1500 - Numba paralelo CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.53 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.001324 | 0.001058 | 0.002382 | 0.059956 | 619.085579 | 10318.092991 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba paralelo CPU | 1500x1500 | 5 | 6 | 2026 | 1349 | 2250000 | 18014291 | 49a177a791d110fb | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.003369 | 0.001135 | 0.004505 | 0.059956 | 18014291 | 49a177a791d110fb |
| 2 | 0.000854 | 0.001025 | 0.001880 | 0.059956 | 18014291 | 49a177a791d110fb |
| 3 | 0.000665 | 0.001032 | 0.001698 | 0.059956 | 18014291 | 49a177a791d110fb |
| 4 | 0.000804 | 0.001007 | 0.001811 | 0.059956 | 18014291 | 49a177a791d110fb |
| 5 | 0.000927 | 0.001091 | 0.002018 | 0.059956 | 18014291 | 49a177a791d110fb |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
