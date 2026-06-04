# Resultado final parcial - Sobel PyTorch CPU

Este documento junta los resultados parciales del metodo **PyTorch CPU** para los tamanios disponibles.

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

## Tabla consolidada

| tamanio | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | PyTorch CPU | 0.001091 | 0.006944 | 0.008035 | 0.281778 |  |  |
| 1500x1500 | PyTorch CPU | 0.012191 | 0.032779 | 0.044970 | 0.059956 |  |  |
| 3000x3000 | PyTorch CPU | 0.058908 | 0.161520 | 0.220428 | 0.001367 |  |  |
| 6000x6000 | PyTorch CPU | 0.229955 | 0.652591 | 0.882546 | 0.000000 |  |  |

## Datos de control

| tamanio | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---:|---:|---:|---:|---:|---|---|
| 750x750 | 5 | 6 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |
| 1500x1500 | 5 | 6 | 1349 | 2250000 | 18014004 | 15e92bfe73d7d960 | ok |
| 3000x3000 | 5 | 6 | 123 | 9000000 | 47883019 | 2657c695a380cf71 | ok |
| 6000x6000 | 5 | 6 | 0 | 36000000 | 109935099 | d863f4ab4aefc06f | ok |

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

El metodo **PyTorch CPU** fue ejecutado para 4 tamanios. El tiempo total promedio pasa de 0.008035 s en `750x750` a 0.882546 s en `6000x6000`.

El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.
Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que
los contornos crecen principalmente como lineas.

La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados
quedan cerca del valor base de `750x750`, la deteccion de contornos se mantiene estable
al escalar la imagen.

Los checksums y hashes sirven como control de reproducibilidad: para una misma imagen de entrada, mismo
metodo y mismo tamanio, deberian mantenerse constantes entre corridas.

## Archivos parciales esperados

- `parciales/resultado_parcial_750x750_pytorch_cpu.md`
- `parciales/resultado_parcial_1500x1500_pytorch_cpu.md`
- `parciales/resultado_parcial_3000x3000_pytorch_cpu.md`
- `parciales/resultado_parcial_6000x6000_pytorch_cpu.md`