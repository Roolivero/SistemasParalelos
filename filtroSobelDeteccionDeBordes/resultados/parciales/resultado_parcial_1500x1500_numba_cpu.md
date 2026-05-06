# Resultado parcial Sobel 1500x1500 - Numba paralelo CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.61 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.001393 | 0.001238 | 0.002632 | 0.161956 | 520.445479 | 6505.568483 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba paralelo CPU | 1500x1500 | 5 | 8 | 2026 | 3644 | 2250000 | 3113394 | 34f7880907cc0e27 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.002655 | 0.001010 | 0.003665 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 2 | 0.001240 | 0.001428 | 0.002668 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 3 | 0.001203 | 0.001293 | 0.002496 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 4 | 0.000937 | 0.001248 | 0.002185 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 5 | 0.000931 | 0.001214 | 0.002146 | 0.161956 | 3113394 | 34f7880907cc0e27 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
