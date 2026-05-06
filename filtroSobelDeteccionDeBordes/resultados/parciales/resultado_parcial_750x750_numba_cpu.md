# Resultado parcial Sobel 750x750 - Numba paralelo CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.64 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.048503 | 0.000313 | 0.048816 | 0.323556 | 7.012784 | 87.659799 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba paralelo CPU | 750x750 | 5 | 8 | 2026 | 1820 | 562500 | 1552402 | 9afeaa122377f409 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.241550 | 0.000359 | 0.241909 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 2 | 0.000316 | 0.000394 | 0.000711 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 3 | 0.000257 | 0.000304 | 0.000561 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 4 | 0.000196 | 0.000256 | 0.000452 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 5 | 0.000195 | 0.000252 | 0.000448 | 0.323556 | 1552402 | 9afeaa122377f409 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
