# Resultados Sobel 750x750

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.49 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 0.087378 | 0.286957 | 0.374334 | 0.281778 | 1.000000 | 100.000000 |
| NumPy | 0.001907 | 0.002542 | 0.004449 | 0.281778 | 84.132985 | 8413.298485 |
| Numba paralelo CPU | 0.000660 | 0.000338 | 0.000997 | 0.281778 | 375.331820 | 6255.530328 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 750x750 | 5 | 1 | 2026 | 1585 | 562500 | 7145137 | e330e8a405b66425 | ok |
| NumPy | 750x750 | 5 | 1 | 2026 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |
| Numba paralelo CPU | 750x750 | 5 | 6 | 2026 | 1585 | 562500 | 7145137 | e330e8a405b66425 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.002236 | 0.000374 | 0.002611 | 0.281778 | 7145137 | e330e8a405b66425 |
| 2 | 0.000310 | 0.000338 | 0.000648 | 0.281778 | 7145137 | e330e8a405b66425 |
| 3 | 0.000250 | 0.000337 | 0.000587 | 0.281778 | 7145137 | e330e8a405b66425 |
| 4 | 0.000253 | 0.000322 | 0.000575 | 0.281778 | 7145137 | e330e8a405b66425 |
| 5 | 0.000248 | 0.000319 | 0.000567 | 0.281778 | 7145137 | e330e8a405b66425 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
