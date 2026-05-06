# Resultado parcial Sobel 750x750 - secuencial

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.48 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: no disponible
- Numba: no disponible

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 0.083825 | 0.258512 | 0.342338 | 0.323556 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 750x750 | 5 | 1 | 2026 | 1820 | 562500 | 1552402 | 9afeaa122377f409 | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.088916 | 0.259314 | 0.348230 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 2 | 0.083478 | 0.264561 | 0.348039 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 3 | 0.082801 | 0.256321 | 0.339123 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 4 | 0.081404 | 0.257865 | 0.339269 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 5 | 0.082528 | 0.254499 | 0.337028 | 0.323556 | 1552402 | 9afeaa122377f409 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
