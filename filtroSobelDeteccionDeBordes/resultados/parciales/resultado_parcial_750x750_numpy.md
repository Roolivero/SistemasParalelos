# Resultado parcial Sobel 750x750 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.27 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.001955 | 0.002600 | 0.004555 | 0.323556 | 75.158997 | 7515.899704 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 750x750 | 5 | 1 | 2026 | 1820 | 562500 | 1552402 | 9afeaa122377f409 | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.003557 | 0.005186 | 0.008743 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 2 | 0.001839 | 0.002078 | 0.003917 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 3 | 0.001647 | 0.002080 | 0.003727 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 4 | 0.001623 | 0.001952 | 0.003575 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 5 | 0.001107 | 0.001706 | 0.002812 | 0.323556 | 1552402 | 9afeaa122377f409 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
