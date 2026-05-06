# Resultado parcial Sobel 1500x1500 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.28 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.008867 | 0.012354 | 0.021221 | 0.161956 | 64.543893 | 6454.389274 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 1500x1500 | 5 | 1 | 2026 | 3644 | 2250000 | 3113394 | 34f7880907cc0e27 | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.011068 | 0.016560 | 0.027628 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 2 | 0.007325 | 0.009396 | 0.016721 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 3 | 0.010901 | 0.015762 | 0.026663 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 4 | 0.008159 | 0.009325 | 0.017483 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 5 | 0.006884 | 0.010727 | 0.017611 | 0.161956 | 3113394 | 34f7880907cc0e27 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
