# Resultado parcial Sobel 6000x6000 - secuencial

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.57 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: no disponible
- Numba: no disponible

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| secuencial | 5.280667 | 17.075369 | 22.356036 | 0.040467 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 6000x6000 | 5 | 1 | 2026 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 5.229105 | 16.901570 | 22.130674 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 2 | 5.325815 | 17.125615 | 22.451430 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 3 | 5.287397 | 16.874376 | 22.161773 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 4 | 5.281956 | 17.133922 | 22.415878 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 5 | 5.279064 | 17.341361 | 22.620425 | 0.040467 | 12474230 | f1b0875ac49b9f7d |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
