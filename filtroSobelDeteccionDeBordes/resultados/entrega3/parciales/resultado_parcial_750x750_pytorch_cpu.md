# Resultado parcial Sobel 750x750 - PyTorch CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.37 GiB disponible
- Sistema operativo: Linux-6.18.33-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.12.13 | packaged by conda-forge | (main, Mar  5 2026, 16:50:00) [GCC 14.3.0]
- GIL habilitado: sin dato
- NumPy: 2.4.6
- Numba: no disponible
- PyTorch: 2.10.0
- GPU CUDA: no detectada (No module named 'numba')
- PyTorch CUDA: NVIDIA GeForce RTX 2060 (CUDA 13.0)

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| PyTorch CPU | 0.001091 | 0.006944 | 0.008035 | 0.281778 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| PyTorch CPU | 750x750 | 5 | 6 | 2026 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |

## Detalle de corridas

### PyTorch CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.001784 | 0.023421 | 0.025205 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 2 | 0.001135 | 0.002142 | 0.003277 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 3 | 0.000829 | 0.002166 | 0.002996 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 4 | 0.000874 | 0.003717 | 0.004591 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 5 | 0.000832 | 0.003274 | 0.004106 | 0.281778 | 7144991 | d154fb8c8a528b71 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU y PyTorch GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de las entregas GPU.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU y PyTorch CPU se usan los hilos configurados; para los demas metodos se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
