# Resultado parcial Sobel 750x750 - NumPy

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
| NumPy | 0.001907 | 0.002542 | 0.004449 | 0.281778 | 84.132981 | 8413.298106 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 750x750 | 5 | 1 | 2026 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.002864 | 0.002699 | 0.005563 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 2 | 0.001748 | 0.002433 | 0.004181 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 3 | 0.001843 | 0.002757 | 0.004600 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 4 | 0.001830 | 0.002488 | 0.004318 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 5 | 0.001251 | 0.002334 | 0.003585 | 0.281778 | 7144991 | d154fb8c8a528b71 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
