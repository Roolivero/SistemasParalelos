# Resultado parcial Sobel 1500x1500 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.52 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.007318 | 0.010708 | 0.018026 | 0.059956 | 81.817344 | 8181.734408 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 1500x1500 | 5 | 1 | 2026 | 1349 | 2250000 | 18013999 | f905721d22fdb912 | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.010245 | 0.011246 | 0.021491 | 0.059956 | 18013999 | f905721d22fdb912 |
| 2 | 0.007184 | 0.010518 | 0.017702 | 0.059956 | 18013999 | f905721d22fdb912 |
| 3 | 0.006025 | 0.011257 | 0.017282 | 0.059956 | 18013999 | f905721d22fdb912 |
| 4 | 0.006872 | 0.010683 | 0.017555 | 0.059956 | 18013999 | f905721d22fdb912 |
| 5 | 0.006266 | 0.009833 | 0.016099 | 0.059956 | 18013999 | f905721d22fdb912 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
