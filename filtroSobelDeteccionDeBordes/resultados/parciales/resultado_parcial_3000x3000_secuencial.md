# Resultado parcial Sobel 3000x3000 - secuencial

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.62 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: no disponible
- Numba: no disponible

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 1.306512 | 4.184142 | 5.490655 | 0.080933 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 3000x3000 | 5 | 1 | 2026 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.308854 | 4.190009 | 5.498864 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 2 | 1.324760 | 4.141498 | 5.466258 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 3 | 1.303229 | 4.196832 | 5.500061 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 4 | 1.308398 | 4.112834 | 5.421231 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 5 | 1.287320 | 4.279540 | 5.566860 | 0.080933 | 6233330 | eb3441cc7677b249 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
