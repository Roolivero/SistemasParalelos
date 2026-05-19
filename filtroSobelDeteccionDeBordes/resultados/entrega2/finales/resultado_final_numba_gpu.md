# Resultado final parcial - Sobel Numba GPU

Este documento junta los resultados parciales del metodo **Numba GPU** para los tamanios disponibles.

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.76 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla consolidada

| tamanio | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | Numba GPU | 0.000138 | 0.000303 | 0.000441 | 0.281778 |  |  |
| 1500x1500 | Numba GPU | 0.000430 | 0.001081 | 0.001511 | 0.059956 |  |  |
| 3000x3000 | Numba GPU | 0.001099 | 0.004376 | 0.005475 | 0.001367 |  |  |
| 6000x6000 | Numba GPU | 0.003973 | 0.017432 | 0.021405 | 0.000000 |  |  |

## Datos de control

| tamanio | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---:|---:|---:|---:|---:|---|---|
| 750x750 | 5 | 256 | 1585 | 562500 | 7145141 | 5d84e47f0fe8922a | ok |
| 1500x1500 | 5 | 256 | 1349 | 2250000 | 18014475 | 82629d16e7e25f5c | ok |
| 3000x3000 | 5 | 256 | 123 | 9000000 | 47884245 | 56d292135dc0414f | ok |
| 6000x6000 | 5 | 256 | 0 | 36000000 | 109937633 | 72c64699d639c009 | ok |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo.

| tamanio | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000598 | 0.000213 | 0.000811 | 0.000441 | 0.001252 |
| 1500x1500 | 0.001302 | 0.000682 | 0.001984 | 0.001511 | 0.003495 |
| 3000x3000 | 0.003251 | 0.001517 | 0.004768 | 0.005475 | 0.010242 |
| 6000x6000 | 0.011006 | 0.005107 | 0.016113 | 0.021405 | 0.037518 |

## Blancos normalizados por escala

Esta tabla compara la cantidad de pixeles blancos teniendo en cuenta que los contornos crecen
principalmente como lineas. Por eso se normaliza por el crecimiento del lado de la imagen respecto
de `750x750`.

| tamanio | factor de lado vs 750 | pixeles blancos | blancos normalizados | indice vs 750 (%) |
|---:|---:|---:|---:|---:|
| 750x750 | 1.00 | 1585 | 1585.00 | 100.00 |
| 1500x1500 | 2.00 | 1349 | 674.50 | 42.56 |
| 3000x3000 | 4.00 | 123 | 30.75 | 1.94 |
| 6000x6000 | 8.00 | 0 | 0.00 | 0.00 |

## Conclusiones

El metodo **Numba GPU** fue ejecutado para 4 tamanios. El tiempo total promedio pasa de 0.000441 s en `750x750` a 0.021405 s en `6000x6000`.

El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.
Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que
los contornos crecen principalmente como lineas.

La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados
quedan cerca del valor base de `750x750`, la deteccion de contornos se mantiene estable
al escalar la imagen.

Los checksums y hashes sirven como control de reproducibilidad: para una misma imagen de entrada, mismo
metodo y mismo tamanio, deberian mantenerse constantes entre corridas.

## Archivos parciales esperados

- `parciales/resultado_parcial_750x750_numba_gpu.md`
- `parciales/resultado_parcial_1500x1500_numba_gpu.md`
- `parciales/resultado_parcial_3000x3000_numba_gpu.md`
- `parciales/resultado_parcial_6000x6000_numba_gpu.md`