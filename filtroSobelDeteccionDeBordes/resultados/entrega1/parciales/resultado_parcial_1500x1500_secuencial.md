# Resultado parcial Sobel 1500x1500 - secuencial

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.36 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 0.329165 | 1.145662 | 1.474827 | 0.059956 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 1500x1500 | 5 | 1 | 2026 | 1349 | 2250000 | 18014291 | 49a177a791d110fb | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.341017 | 1.141896 | 1.482912 | 0.059956 | 18014291 | 49a177a791d110fb |
| 2 | 0.323868 | 1.121810 | 1.445678 | 0.059956 | 18014291 | 49a177a791d110fb |
| 3 | 0.324519 | 1.156107 | 1.480626 | 0.059956 | 18014291 | 49a177a791d110fb |
| 4 | 0.331295 | 1.184406 | 1.515701 | 0.059956 | 18014291 | 49a177a791d110fb |
| 5 | 0.325128 | 1.124091 | 1.449219 | 0.059956 | 18014291 | 49a177a791d110fb |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
