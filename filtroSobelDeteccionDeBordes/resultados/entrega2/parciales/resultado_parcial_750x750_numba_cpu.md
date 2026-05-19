# Resultado parcial Sobel 750x750 - Numba paralelo CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.51 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: CUDA no disponible
- GPU CUDA: CUDA no disponible

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.000571 | 0.000238 | 0.000809 | 0.281778 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba paralelo CPU | 750x750 | 5 | 6 | 2026 | 1585 | 562500 | 7145137 | e330e8a405b66425 | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.002114 | 0.000312 | 0.002426 | 0.281778 | 7145137 | e330e8a405b66425 |
| 2 | 0.000274 | 0.000260 | 0.000534 | 0.281778 | 7145137 | e330e8a405b66425 |
| 3 | 0.000147 | 0.000204 | 0.000351 | 0.281778 | 7145137 | e330e8a405b66425 |
| 4 | 0.000151 | 0.000202 | 0.000353 | 0.281778 | 7145137 | e330e8a405b66425 |
| 5 | 0.000170 | 0.000212 | 0.000383 | 0.281778 | 7145137 | e330e8a405b66425 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
