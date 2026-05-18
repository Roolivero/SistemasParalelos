# Resultado parcial Sobel 750x750 - secuencial

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.38 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 0.087378 | 0.286957 | 0.374334 | 0.281778 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 750x750 | 5 | 1 | 2026 | 1585 | 562500 | 7145137 | e330e8a405b66425 | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.098658 | 0.289268 | 0.387927 | 0.281778 | 7145137 | e330e8a405b66425 |
| 2 | 0.088007 | 0.287342 | 0.375350 | 0.281778 | 7145137 | e330e8a405b66425 |
| 3 | 0.083017 | 0.280488 | 0.363506 | 0.281778 | 7145137 | e330e8a405b66425 |
| 4 | 0.083480 | 0.288280 | 0.371760 | 0.281778 | 7145137 | e330e8a405b66425 |
| 5 | 0.083726 | 0.289405 | 0.373130 | 0.281778 | 7145137 | e330e8a405b66425 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
