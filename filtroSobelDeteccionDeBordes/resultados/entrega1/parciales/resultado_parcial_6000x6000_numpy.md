# Resultado parcial Sobel 6000x6000 - NumPy

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.48 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| NumPy | 0.130965 | 0.280494 | 0.411459 | 0.000000 | 55.081437 | 5508.143745 |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| NumPy | 6000x6000 | 5 | 1 | 2026 | 0 | 36000000 | 109935099 | 58d0001f7448e5ed | ok |

## Detalle de corridas

### NumPy

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.130571 | 0.279798 | 0.410370 | 0.000000 | 109935099 | 58d0001f7448e5ed |
| 2 | 0.129481 | 0.283455 | 0.412936 | 0.000000 | 109935099 | 58d0001f7448e5ed |
| 3 | 0.132061 | 0.277585 | 0.409646 | 0.000000 | 109935099 | 58d0001f7448e5ed |
| 4 | 0.132435 | 0.278746 | 0.411182 | 0.000000 | 109935099 | 58d0001f7448e5ed |
| 5 | 0.130277 | 0.282886 | 0.413163 | 0.000000 | 109935099 | 58d0001f7448e5ed |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
