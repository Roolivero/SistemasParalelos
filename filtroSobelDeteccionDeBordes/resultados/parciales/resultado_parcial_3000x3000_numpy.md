# Resultado parcial Sobel 3000x3000 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.29 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.035172 | 0.074253 | 0.109426 | 0.080933 | 50.177077 | 5017.707673 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 3000x3000 | 5 | 1 | 2026 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.041653 | 0.098215 | 0.139868 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 2 | 0.033564 | 0.067780 | 0.101344 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 3 | 0.034750 | 0.068225 | 0.102976 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 4 | 0.032834 | 0.068923 | 0.101757 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 5 | 0.033059 | 0.068124 | 0.101183 | 0.080933 | 6233330 | eb3441cc7677b249 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
