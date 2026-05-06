# Resultado final parcial - Sobel Numba paralelo CPU

Este documento junta los resultados parciales del metodo **Numba paralelo CPU** para los tamaños disponibles.

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.64 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla consolidada

| tamaño | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | Numba paralelo CPU | 0.048503 | 0.000313 | 0.048816 | 0.323556 | 7.012784 | 87.659800 |
| 1500x1500 | Numba paralelo CPU | 0.001393 | 0.001238 | 0.002632 | 0.161956 | 520.445518 | 6505.568979 |
| 3000x3000 | Numba paralelo CPU | 0.004670 | 0.004492 | 0.009161 | 0.080933 | 599.329247 | 7491.615591 |
| 6000x6000 | Numba paralelo CPU | 0.014490 | 0.015880 | 0.030370 | 0.040467 | 736.119688 | 9201.496104 |

## Datos de control

| tamaño | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---:|---:|---:|---:|---:|---|---|
| 750x750 | 5 | 8 | 1820 | 562500 | 1552402 | 9afeaa122377f409 | ok |
| 1500x1500 | 5 | 8 | 3644 | 2250000 | 3113394 | 34f7880907cc0e27 | ok |
| 3000x3000 | 5 | 8 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |
| 6000x6000 | 5 | 8 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |

## Blancos normalizados por escala

Esta tabla compara la cantidad de pixeles blancos teniendo en cuenta que los contornos crecen
principalmente como lineas. Por eso se normaliza por el crecimiento del lado de la imagen respecto
de `750x750`.

| tamaño | factor de lado vs 750 | pixeles blancos | blancos normalizados | indice vs 750 (%) |
|---:|---:|---:|---:|---:|
| 750x750 | 1.00 | 1820 | 1820.00 | 100.00 |
| 1500x1500 | 2.00 | 3644 | 1822.00 | 100.11 |
| 3000x3000 | 4.00 | 7284 | 1821.00 | 100.05 |
| 6000x6000 | 8.00 | 14568 | 1821.00 | 100.05 |

## Conclusiones

El metodo **Numba paralelo CPU** fue ejecutado para 4 tamaños. El tiempo total promedio pasa de 0.048816 s en `750x750` a 0.030370 s en `6000x6000`.

El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.
Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que
los contornos crecen principalmente como lineas.

La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados
quedan cerca del valor base de `750x750`, la deteccion de contornos se mantiene estable
al escalar la imagen.

Los checksums y hashes sirven como control de reproducibilidad: para una misma entrada sintetica, mismo
metodo y mismo tamaño, deberian mantenerse constantes entre corridas.

## Archivos parciales esperados

- `parciales/resultado_parcial_750x750_numba_cpu.md`
- `parciales/resultado_parcial_1500x1500_numba_cpu.md`
- `parciales/resultado_parcial_3000x3000_numba_cpu.md`
- `parciales/resultado_parcial_6000x6000_numba_cpu.md`