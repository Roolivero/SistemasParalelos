# Resultado parcial Sobel 6000x6000 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.25 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.147766 | 0.293736 | 0.441502 | 0.040467 | 50.636269 | 5063.626943 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 6000x6000 | 5 | 1 | 2026 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.207585 | 0.357205 | 0.564790 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 2 | 0.134127 | 0.285929 | 0.420056 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 3 | 0.132810 | 0.274597 | 0.407406 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 4 | 0.132129 | 0.277426 | 0.409555 | 0.040467 | 12474230 | f1b0875ac49b9f7d |
| 5 | 0.132181 | 0.273523 | 0.405705 | 0.040467 | 12474230 | f1b0875ac49b9f7d |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada es sintetica y reproducible: mismo tamanio y seed producen los mismos pixeles.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
