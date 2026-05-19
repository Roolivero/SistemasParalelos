# Resultado final parcial - Sobel NumPy

Este documento junta los resultados parciales del metodo **NumPy** para los tamanios disponibles.

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.57 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla consolidada

| tamanio | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | NumPy | 0.001907 | 0.002542 | 0.004449 | 0.281778 | 84.132985 | 8413.298485 |
| 1500x1500 | NumPy | 0.007318 | 0.010708 | 0.018026 | 0.059956 | 81.817345 | 8181.734499 |
| 3000x3000 | NumPy | 0.033103 | 0.073703 | 0.106806 | 0.001367 | 53.540383 | 5354.038287 |
| 6000x6000 | NumPy | 0.130965 | 0.280494 | 0.411459 | 0.000000 | 55.081437 | 5508.143742 |

## Datos de control

| tamanio | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---:|---:|---:|---:|---:|---|---|
| 750x750 | 5 | 1 | 1585 | 562500 | 7144991 | d154fb8c8a528b71 | ok |
| 1500x1500 | 5 | 1 | 1349 | 2250000 | 18013999 | f905721d22fdb912 | ok |
| 3000x3000 | 5 | 1 | 123 | 9000000 | 47883024 | a92d650778fbd8bf | ok |
| 6000x6000 | 5 | 1 | 0 | 36000000 | 109935099 | 58d0001f7448e5ed | ok |

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

El metodo **NumPy** fue ejecutado para 4 tamanios. El tiempo total promedio pasa de 0.004449 s en `750x750` a 0.411459 s en `6000x6000`.

El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.
Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que
los contornos crecen principalmente como lineas.

La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados
quedan cerca del valor base de `750x750`, la deteccion de contornos se mantiene estable
al escalar la imagen.

Los checksums y hashes sirven como control de reproducibilidad: para una misma imagen de entrada, mismo
metodo y mismo tamanio, deberian mantenerse constantes entre corridas.

## Archivos parciales esperados

- `parciales/resultado_parcial_750x750_numpy.md`
- `parciales/resultado_parcial_1500x1500_numpy.md`
- `parciales/resultado_parcial_3000x3000_numpy.md`
- `parciales/resultado_parcial_6000x6000_numpy.md`