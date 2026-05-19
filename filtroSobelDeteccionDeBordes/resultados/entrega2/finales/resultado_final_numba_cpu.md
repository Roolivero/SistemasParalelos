# Resultado final parcial - Sobel Numba paralelo CPU

Este documento junta los resultados parciales del metodo **Numba paralelo CPU** para los tamanios disponibles.

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.51 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: CUDA no disponible
- GPU CUDA: CUDA no disponible

## Tabla consolidada

| tamanio | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | Numba paralelo CPU | 0.000571 | 0.000238 | 0.000809 | 0.281778 |  |  |
| 1500x1500 | Numba paralelo CPU | 0.001601 | 0.001397 | 0.002998 | 0.059956 |  |  |
| 3000x3000 | Numba paralelo CPU | 0.003457 | 0.004142 | 0.007598 | 0.001367 |  |  |
| 6000x6000 | Numba paralelo CPU | 0.012564 | 0.014839 | 0.027403 | 0.000000 |  |  |

## Datos de control

| tamanio | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---:|---:|---:|---:|---:|---|---|
| 750x750 | 5 | 6 | 1585 | 562500 | 7145137 | e330e8a405b66425 | ok |
| 1500x1500 | 5 | 6 | 1349 | 2250000 | 18014291 | 49a177a791d110fb | ok |
| 3000x3000 | 5 | 6 | 123 | 9000000 | 47883925 | a5989d2f439a9154 | ok |
| 6000x6000 | 5 | 6 | 0 | 36000000 | 109936717 | d8af6b4c711617e3 | ok |

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

El metodo **Numba paralelo CPU** fue ejecutado para 4 tamanios. El tiempo total promedio pasa de 0.000809 s en `750x750` a 0.027403 s en `6000x6000`.

El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.
Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que
los contornos crecen principalmente como lineas.

La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados
quedan cerca del valor base de `750x750`, la deteccion de contornos se mantiene estable
al escalar la imagen.

Los checksums y hashes sirven como control de reproducibilidad: para una misma imagen de entrada, mismo
metodo y mismo tamanio, deberian mantenerse constantes entre corridas.

## Archivos parciales esperados

- `parciales/resultado_parcial_750x750_numba_cpu.md`
- `parciales/resultado_parcial_1500x1500_numba_cpu.md`
- `parciales/resultado_parcial_3000x3000_numba_cpu.md`
- `parciales/resultado_parcial_6000x6000_numba_cpu.md`