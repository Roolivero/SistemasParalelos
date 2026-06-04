# Resultados Sobel 6000x6000

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.20 GiB disponible
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
| PyTorch CPU | 0.229955 | 0.652591 | 0.882546 | 0.000000 |  |  |
| PyTorch GPU | 0.014273 | 0.014200 | 0.028473 | 0.000000 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| PyTorch CPU | 6000x6000 | 5 | 6 | 2026 | 0 | 36000000 | 109935099 | d863f4ab4aefc06f | ok |
| PyTorch GPU | 6000x6000 | 5 | 1 | 2026 | 0 | 36000000 | 109935099 | d863f4ab4aefc06f | ok |

## Detalle de corridas

### PyTorch GPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.014110 | 0.017298 | 0.031408 | 0.000000 | 109935099 | d863f4ab4aefc06f |
| 2 | 0.014383 | 0.013460 | 0.027843 | 0.000000 | 109935099 | d863f4ab4aefc06f |
| 3 | 0.014469 | 0.013090 | 0.027559 | 0.000000 | 109935099 | d863f4ab4aefc06f |
| 4 | 0.014500 | 0.013420 | 0.027920 | 0.000000 | 109935099 | d863f4ab4aefc06f |
| 5 | 0.013904 | 0.013733 | 0.027637 | 0.000000 | 109935099 | d863f4ab4aefc06f |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo. No se suman en la columna de tiempo total solicitada, que mide solamente conversion RGB->gris y Sobel.

| metodo | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---|---:|---:|---:|---:|---:|
| PyTorch GPU | 0.009766 | 0.005081 | 0.014847 | 0.028473 | 0.043321 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU y PyTorch GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de las entregas GPU.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU y PyTorch CPU se usan los hilos configurados; para los demas metodos se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
