# Resultados Sobel 3000x3000

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.43 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 1.315055 | 4.403400 | 5.718456 | 0.001367 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 3000x3000 | 5 | 1 | 2026 | 123 | 9000000 | 47883925 | a5989d2f439a9154 | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 1.320443 | 4.341885 | 5.662327 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 2 | 1.327957 | 4.430060 | 5.758017 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 3 | 1.304141 | 4.427218 | 5.731360 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 4 | 1.314348 | 4.422896 | 5.737244 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 5 | 1.308388 | 4.394942 | 5.703330 | 0.001367 | 47883925 | a5989d2f439a9154 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
