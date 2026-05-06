# Resultado final parcial - Sobel NumPy

Este documento junta los resultados parciales del metodo **NumPy** para los tamaños disponibles.

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 8.27 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1

## Tabla consolidada

| tamaño | metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 750x750 | NumPy | 0.001955 | 0.002600 | 0.004555 | 0.323556 | 75.158994 | 7515.899374 |
| 1500x1500 | NumPy | 0.008867 | 0.012354 | 0.021221 | 0.161956 | 64.543893 | 6454.389334 |
| 3000x3000 | NumPy | 0.035172 | 0.074253 | 0.109426 | 0.080933 | 50.177077 | 5017.707664 |
| 6000x6000 | NumPy | 0.147766 | 0.293736 | 0.441502 | 0.040467 | 50.636269 | 5063.626945 |

## Datos de control

| tamaño | corridas | workers/hilos | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---:|---:|---:|---:|---:|---:|---|---|
| 750x750 | 5 | 1 | 1820 | 562500 | 1552402 | 9afeaa122377f409 | ok |
| 1500x1500 | 5 | 1 | 3644 | 2250000 | 3113394 | 34f7880907cc0e27 | ok |
| 3000x3000 | 5 | 1 | 7284 | 9000000 | 6233330 | eb3441cc7677b249 | ok |
| 6000x6000 | 5 | 1 | 14568 | 36000000 | 12474230 | f1b0875ac49b9f7d | ok |

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

El metodo **NumPy** fue ejecutado para 4 tamaños. El tiempo total promedio pasa de 0.004555 s en `750x750` a 0.441502 s en `6000x6000`.

El porcentaje de pixeles blancos sobre el total de la imagen puede disminuir cuando aumenta la resolucion.
Esa baja no significa necesariamente peor deteccion: el total de pixeles crece como area, mientras que
los contornos crecen principalmente como lineas.

La tabla de blancos normalizados permite comparar de forma mas equitativa. Si los valores normalizados
quedan cerca del valor base de `750x750`, la deteccion de contornos se mantiene estable
al escalar la imagen.

Los checksums y hashes sirven como control de reproducibilidad: para una misma entrada sintetica, mismo
metodo y mismo tamaño, deberian mantenerse constantes entre corridas.

## Archivos parciales esperados

- `parciales/resultado_parcial_750x750_numpy.md`
- `parciales/resultado_parcial_1500x1500_numpy.md`
- `parciales/resultado_parcial_3000x3000_numpy.md`
- `parciales/resultado_parcial_6000x6000_numpy.md`