# Resultados Sobel 3000x3000

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.58 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 1.306512 | 4.184142 | 5.490655 | 0.080933 | 1.000000 | 100.000000 |
| NumPy | 0.035172 | 0.074253 | 0.109426 | 0.080933 | 50.177077 | 5017.707664 |
| Numba paralelo CPU | 0.004670 | 0.004492 | 0.009161 | 0.080933 | 599.329234 | 7491.615428 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 3000x3000 | 5 | 1 | 2026 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |
| NumPy | 3000x3000 | 5 | 1 | 2026 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |
| Numba paralelo CPU | 3000x3000 | 5 | 8 | 2026 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.006644 | 0.004344 | 0.010988 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 2 | 0.004657 | 0.004650 | 0.009307 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 3 | 0.004663 | 0.004344 | 0.009007 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 4 | 0.003684 | 0.004498 | 0.008182 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 5 | 0.003701 | 0.004622 | 0.008323 | 0.080933 | 6233330 | eb3441cc7677b249 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
