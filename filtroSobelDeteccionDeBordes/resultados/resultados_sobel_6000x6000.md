# Resultados Sobel 6000x6000

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.54 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 5.280667 | 17.075369 | 22.356036 | 0.040467 | 1.000000 | 100.000000 |
| NumPy | 0.147766 | 0.293736 | 0.441502 | 0.040467 | 50.636269 | 5063.626945 |
| Numba paralelo CPU | 0.014490 | 0.015880 | 0.030370 | 0.040467 | 736.119679 | 9201.495983 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 6000x6000 | 5 | 1 | 2026 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |
| NumPy | 6000x6000 | 5 | 1 | 2026 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |
| Numba paralelo CPU | 6000x6000 | 5 | 8 | 2026 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |

## Detalle de corridas

### Numba paralelo CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.016358 | 0.015615 | 0.031973 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 2 | 0.013780 | 0.016120 | 0.029900 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 3 | 0.013728 | 0.015807 | 0.029535 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 4 | 0.014067 | 0.015897 | 0.029964 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 5 | 0.014518 | 0.015960 | 0.030478 | 0.040467 | 12474230 | f1b0875ac49b9f7d |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
