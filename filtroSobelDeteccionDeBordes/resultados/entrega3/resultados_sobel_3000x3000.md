# Resultados Sobel 3000x3000

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.24 GiB disponible
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
| PyTorch CPU | 0.058908 | 0.161520 | 0.220428 | 0.001367 |  |  |
| PyTorch GPU | 0.003475 | 0.004065 | 0.007539 | 0.001367 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| PyTorch CPU | 3000x3000 | 5 | 6 | 2026 | 123 | 9000000 | 47883019 | 2657c695a380cf71 | ok |
| PyTorch GPU | 3000x3000 | 5 | 1 | 2026 | 123 | 9000000 | 47883019 | 2657c695a380cf71 | ok |

## Detalle de corridas

### PyTorch GPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.003499 | 0.007241 | 0.010740 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 2 | 0.003451 | 0.003268 | 0.006719 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 3 | 0.003448 | 0.003271 | 0.006719 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 4 | 0.003459 | 0.003274 | 0.006733 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 5 | 0.003516 | 0.003269 | 0.006785 | 0.001367 | 47883019 | 2657c695a380cf71 |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo. No se suman en la columna de tiempo total solicitada, que mide solamente conversion RGB->gris y Sobel.

| metodo | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---|---:|---:|---:|---:|---:|
| PyTorch GPU | 0.002698 | 0.001527 | 0.004225 | 0.007539 | 0.011764 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU y PyTorch GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de las entregas GPU.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU y PyTorch CPU se usan los hilos configurados; para los demas metodos se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
