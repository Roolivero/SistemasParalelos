# Resultado parcial Sobel 3000x3000 - PyTorch CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.26 GiB disponible
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

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| PyTorch CPU | 3000x3000 | 5 | 6 | 2026 | 123 | 9000000 | 47883019 | 2657c695a380cf71 | ok |

## Detalle de corridas

### PyTorch CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.062059 | 0.160877 | 0.222936 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 2 | 0.058498 | 0.157057 | 0.215555 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 3 | 0.057089 | 0.159234 | 0.216323 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 4 | 0.057822 | 0.164933 | 0.222756 | 0.001367 | 47883019 | 2657c695a380cf71 |
| 5 | 0.059069 | 0.165499 | 0.224569 | 0.001367 | 47883019 | 2657c695a380cf71 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU y PyTorch GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de las entregas GPU.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU y PyTorch CPU se usan los hilos configurados; para los demas metodos se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
