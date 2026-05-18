# Resultados Sobel 6000x6000

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
| secuencial | 5.243595 | 17.420171 | 22.663766 | 0.000000 | 1.000000 | 100.000000 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| secuencial | 6000x6000 | 5 | 1 | 2026 | 0 | 36000000 | 109936717 | d8af6b4c711617e3 | ok |

## Detalle de corridas

### secuencial

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 5.179304 | 17.640743 | 22.820047 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 2 | 5.230006 | 17.441060 | 22.671066 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 3 | 5.232929 | 17.341469 | 22.574398 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 4 | 5.270700 | 17.432827 | 22.703527 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 5 | 5.305038 | 17.244755 | 22.549793 | 0.000000 | 109936717 | d8af6b4c711617e3 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
