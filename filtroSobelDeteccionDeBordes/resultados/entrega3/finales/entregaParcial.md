# Entrega parcial 3 - Sobel PyTorch CPU y PyTorch GPU

Este documento unifica los resultados finales de:

- `resultado_final_pytorch_cpu.md`
- `resultado_final_pytorch_gpu.md`

No se eliminan datos de los finales individuales: se combinan las tablas para facilitar la comparacion
entre PyTorch CPU y PyTorch GPU.

## Entorno registrado

| dato | PyTorch CPU | PyTorch GPU |
|---|---|---|
| CPU | AMD Ryzen 5 5600X 6-Core Processor | AMD Ryzen 5 5600X 6-Core Processor |
| Nucleos fisicos | 6 | 6 |
| Nucleos logicos | 12 | 12 |
| RAM | 15.52 GiB total, 10.37 GiB disponible | 15.52 GiB total, 10.19 GiB disponible |
| Sistema operativo | Linux-6.18.33-1-MANJARO-x86_64-with-glibc2.43 | Linux-6.18.33-1-MANJARO-x86_64-with-glibc2.43 |
| Python | 3.12.13 \| packaged by conda-forge \| (main, Mar  5 2026, 16:50:00) [GCC 14.3.0] | 3.12.13 \| packaged by conda-forge \| (main, Mar  5 2026, 16:50:00) [GCC 14.3.0] |
| GIL habilitado | sin dato | sin dato |
| NumPy | 2.4.6 | 2.4.6 |
| Numba | no disponible | no disponible |
| PyTorch | 2.10.0 | 2.10.0 |
| GPU CUDA | no detectada (No module named 'numba') | no detectada (No module named 'numba') |
| PyTorch CUDA | NVIDIA GeForce RTX 2060 (CUDA 13.0) | NVIDIA GeForce RTX 2060 (CUDA 13.0) |

## Tabla consolidada combinada

| tamanio | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | PyTorch CPU | 0.001091 | 0.006944 | 0.008035 | 0.281778 |  |  |
| 750x750 | PyTorch GPU | 0.000263 | 0.000935 | 0.001199 | 0.281778 |  |  |
| 1500x1500 | PyTorch CPU | 0.012191 | 0.032779 | 0.044970 | 0.059956 |  |  |
| 1500x1500 | PyTorch GPU | 0.000978 | 0.001502 | 0.002481 | 0.059956 |  |  |
| 3000x3000 | PyTorch CPU | 0.058908 | 0.161520 | 0.220428 | 0.001367 |  |  |
| 3000x3000 | PyTorch GPU | 0.003475 | 0.004065 | 0.007539 | 0.001367 |  |  |
| 6000x6000 | PyTorch CPU | 0.229955 | 0.652591 | 0.882546 | 0.000000 |  |  |
| 6000x6000 | PyTorch GPU | 0.014273 | 0.014200 | 0.028473 | 0.000000 |  |  |

## Comparacion directa CPU vs GPU

| tamanio | total PyTorch CPU (s) | total PyTorch GPU computo (s) | speed-up GPU vs CPU | total GPU con transferencias (s) | speed-up GPU vs CPU con transferencias |
|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.008035 | 0.001199 | 6.701418 | 0.001651 | 4.866747 |
| 1500x1500 | 0.044970 | 0.002481 | 18.125756 | 0.003869 | 11.623158 |
| 3000x3000 | 0.220428 | 0.007539 | 29.238361 | 0.011764 | 18.737504 |
| 6000x6000 | 0.882546 | 0.028473 | 30.995891 | 0.043321 | 20.372244 |

## Datos de control combinados

| tamanio | metodo | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 750x750 | PyTorch CPU | 5 | 6 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |
| 750x750 | PyTorch GPU | 5 | 1 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |
| 1500x1500 | PyTorch CPU | 5 | 6 | 1349 | 2250000 | 18014004 | 15e92bfe73d7d960 | ok |
| 1500x1500 | PyTorch GPU | 5 | 1 | 1349 | 2250000 | 18014004 | 15e92bfe73d7d960 | ok |
| 3000x3000 | PyTorch CPU | 5 | 6 | 123 | 9000000 | 47883019 | 2657c695a380cf71 | ok |
| 3000x3000 | PyTorch GPU | 5 | 1 | 123 | 9000000 | 47883019 | 2657c695a380cf71 | ok |
| 6000x6000 | PyTorch CPU | 5 | 6 | 0 | 36000000 | 109935099 | d863f4ab4aefc06f | ok |
| 6000x6000 | PyTorch GPU | 5 | 1 | 0 | 36000000 | 109935099 | d863f4ab4aefc06f | ok |

## Transferencias CPU-GPU

Estos tiempos provienen del resultado final de **PyTorch GPU** y se registran aparte para analizar
el costo de mover datos entre host y dispositivo.

| tamanio | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000255 | 0.000197 | 0.000452 | 0.001199 | 0.001651 |
| 1500x1500 | 0.000742 | 0.000646 | 0.001388 | 0.002481 | 0.003869 |
| 3000x3000 | 0.002698 | 0.001527 | 0.004225 | 0.007539 | 0.011764 |
| 6000x6000 | 0.009766 | 0.005081 | 0.014847 | 0.028473 | 0.043321 |

## Blancos normalizados por escala

Los valores de PyTorch CPU y PyTorch GPU coinciden en pixeles blancos, checksum y hash para cada
tamanio, por lo que la tabla normalizada es comun a ambos metodos.

| tamanio | factor de lado vs 750 | pixeles blancos | blancos normalizados | indice vs 750 (%) |
|---:|---:|---:|---:|---:|
| 750x750 | 1.00 | 1585 | 1585.00 | 100.00 |
| 1500x1500 | 2.00 | 1349 | 674.50 | 42.56 |
| 3000x3000 | 4.00 | 123 | 30.75 | 1.94 |
| 6000x6000 | 8.00 | 0 | 0.00 | 0.00 |

## Conclusiones combinadas

El metodo **PyTorch CPU** fue ejecutado para 4 tamanios. El tiempo total promedio pasa de
0.008035 s en `750x750` a 0.882546 s en `6000x6000`.

El metodo **PyTorch GPU** fue ejecutado para 4 tamanios. El tiempo total promedio de computo pasa
de 0.001199 s en `750x750` a 0.028473 s en `6000x6000`.

En computo puro, PyTorch GPU mejora a PyTorch CPU en todos los tamanios. La mejora crece al
aumentar la resolucion: pasa de 6.701418x en `750x750` a 30.995891x en `6000x6000`.

Al incluir transferencias CPU-GPU, la mejora sigue siendo positiva en todos los tamanios, aunque
menor: pasa de 4.866747x en `750x750` a 20.372244x en `6000x6000`.

Las salidas de PyTorch CPU y PyTorch GPU son consistentes entre si: para cada tamanio coinciden
el porcentaje de blancos, los pixeles blancos, el checksum y el hash de salida.

## Archivos parciales esperados

### PyTorch CPU

- `parciales/resultado_parcial_750x750_pytorch_cpu.md`
- `parciales/resultado_parcial_1500x1500_pytorch_cpu.md`
- `parciales/resultado_parcial_3000x3000_pytorch_cpu.md`
- `parciales/resultado_parcial_6000x6000_pytorch_cpu.md`

### PyTorch GPU

- `parciales/resultado_parcial_750x750_pytorch_gpu.md`
- `parciales/resultado_parcial_1500x1500_pytorch_gpu.md`
- `parciales/resultado_parcial_3000x3000_pytorch_gpu.md`
- `parciales/resultado_parcial_6000x6000_pytorch_gpu.md`

## Fuentes internas combinadas

- `finales/resultado_final_pytorch_cpu.md`
- `finales/resultado_final_pytorch_gpu.md`
