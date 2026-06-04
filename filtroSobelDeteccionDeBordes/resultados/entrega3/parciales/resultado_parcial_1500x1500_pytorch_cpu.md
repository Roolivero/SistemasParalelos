# Resultado parcial Sobel 1500x1500 - PyTorch CPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.27 GiB disponible
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
| PyTorch CPU | 0.012191 | 0.032779 | 0.044970 | 0.059956 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| PyTorch CPU | 1500x1500 | 5 | 6 | 2026 | 1349 | 2250000 | 18014004 | 15e92bfe73d7d960 | ok |

## Detalle de corridas

### PyTorch CPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.012806 | 0.047003 | 0.059809 | 0.059956 | 18014004 | 15e92bfe73d7d960 |
| 2 | 0.012268 | 0.031107 | 0.043375 | 0.059956 | 18014004 | 15e92bfe73d7d960 |
| 3 | 0.012269 | 0.027460 | 0.039729 | 0.059956 | 18014004 | 15e92bfe73d7d960 |
| 4 | 0.011589 | 0.029023 | 0.040612 | 0.059956 | 18014004 | 15e92bfe73d7d960 |
| 5 | 0.012023 | 0.029302 | 0.041324 | 0.059956 | 18014004 | 15e92bfe73d7d960 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU y PyTorch GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de las entregas GPU.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU y PyTorch CPU se usan los hilos configurados; para los demas metodos se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
