# Resultado parcial Sobel 1500x1500 - secuencial

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
| secuencial | 0.334964 | 1.034740 | 1.369705 | 0.161956 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 1500x1500 | 5 | 1 | 2026 | 3644 | 2250000 | 3113394 | 34f7880907cc0e27 | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.340612 | 1.043059 | 1.383671 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 2 | 0.328978 | 1.060149 | 1.389127 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 3 | 0.345020 | 1.020647 | 1.365667 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 4 | 0.329723 | 1.028043 | 1.357767 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 5 | 0.330490 | 1.021804 | 1.352293 | 0.161956 | 3113394 | 34f7880907cc0e27 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
