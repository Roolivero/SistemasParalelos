# Titulo

Informe de rendimiento: multiplicacion de matrices y estrategias de paralelizacion en Python

## Abstract

En este trabajo se evalua el desempeno de distintas implementaciones de multiplicacion de matrices cuadradas en Python: secuencial tradicional, secuencial optimizada por transposicion, `threading`, `ThreadPoolExecutor`, `ProcessPoolExecutor` y `numba (njit)`. Los experimentos se ejecutaron con complejidades `C=512` y `C=1024`, variando la cantidad de workers (`1`, `4`, `10` y `16`) para analizar tiempos de ejecucion, speed-up y eficiencia. Los resultados muestran que `threading` presenta mejoras limitadas en cargas CPU-bound, mientras que `multiprocessing` ofrece una aceleracion mas consistente. La estrategia con mejor rendimiento global fue `numba (njit)`, que redujo los tiempos en uno o dos ordenes de magnitud respecto al secuencial tradicional.

## Introduccion

La multiplicacion de matrices es un problema clasico de alto costo computacional, con complejidad temporal cubica en su forma tradicional. Debido a su intensidad de calculo y a su relevancia en simulacion numerica, inteligencia artificial y procesamiento cientifico, constituye un caso adecuado para estudiar tecnicas de optimizacion y paralelizacion.

En Python, el rendimiento de este tipo de tareas depende tanto del algoritmo como del modelo de concurrencia utilizado. Por ello, este informe compara alternativas basadas en hilos, procesos y compilacion JIT, con el objetivo de identificar cual ofrece mejor compromiso entre aceleracion y eficiencia para diferentes tamanos de problema.

## Metodologias

Se trabajaron experimentos de benchmarking sobre multiplicacion de matrices cuadradas con valores enteros pseudoaleatorios, manteniendo el mismo criterio de verificacion numerica mediante checksum para cada corrida.

### Entorno y hardware

- CPU: Intel(R) Core(TM) Ultra 9 185H
  - 16 nucleos fisicos, 22 hilos logicos
- RAM: 30 GiB totales (18 GiB disponibles al momento del relevamiento)
- Sistema operativo: Linux Manjaro 6.12.77-1-MANJARO
- Version de Python: 3.14.3
- GPU (CUDA/MPS): no se detecta `nvidia-smi` en el entorno actual, por lo que no se incluyen resultados de PyTorch.

Configuraciones consideradas:

- Complejidad de matriz: `C=512` y `C=1024`.
- Cantidad de workers evaluada: `1`, `4`, `10` y `16`.
- Semilla de reproducibilidad utilizada en las corridas: `--seed 2026`.
- Metodos comparados:
  - secuencial tradicional,
  - secuencial optimizada (uso de matriz transpuesta),
  - `threading`,
  - `concurrent.futures.ThreadPoolExecutor`,
  - `concurrent.futures.ProcessPoolExecutor`,
  - `numba (njit)`.

Metricas registradas:

- tiempo de ejecucion para `A*B`,
- tiempo de ejecucion para `B^T*A^T`,
- speed-up (respecto al secuencial tradicional),
- eficiencia (speed-up dividido por workers),
- checksum de resultados para validar correctitud.

Link al repositorio: 

## Experimentos

En esta seccion se presentan los resultados crudos de las corridas disponibles.

### Experimento 1: C = 512, workers = 1

| Metodo | t(A*B) [s] | t(B^T*A^T) [s] | Checksum A*B | Checksum B^T*A^T | Speed-up A*B | Performance A*B [%] | Speed-up B^T*A^T | Performance B^T*A^T [%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Secuencial tradicional | 9.286013 | 9.303695 | -110463704 | -110463704 | 1.000 | 100.00 | 1.000 | 100.00 |
| Secuencial optimizada (transpuesta) | 6.594259 | 6.329482 | -110463704 | -110463704 | 1.408 | 140.82 | 1.470 | 146.99 |
| ThreadPoolExecutor | 7.070678 | 7.524049 | -110463704 | -110463704 | 1.313 | 131.33 | 1.237 | 123.65 |
| threading | 7.261479 | 7.233229 | -110463704 | -110463704 | 1.279 | 127.88 | 1.286 | 128.62 |
| ProcessPoolExecutor | 6.942384 | 6.634457 | -110463704 | -110463704 | 1.338 | 133.76 | 1.402 | 140.23 |
| numba (njit) | 0.580156 | 0.610545 | -110463704 | -110463704 | 16.006 | 1600.61 | 15.238 | 1523.83 |

### Experimento 2: C = 512, workers = 4

| Metodo | t(A*B) [s] | t(B^T*A^T) [s] | Checksum A*B | Checksum B^T*A^T | Speed-up A*B | Performance A*B [%] | Speed-up B^T*A^T | Performance B^T*A^T [%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Secuencial tradicional | 9.933010 | 9.935754 | -110463704 | -110463704 | 1.000 | 100.00 | 1.000 | 100.00 |
| Secuencial optimizada (transpuesta) | 6.589254 | 6.361890 | -110463704 | -110463704 | 1.507 | 150.75 | 1.562 | 156.18 |
| ThreadPoolExecutor | 4.083622 | 4.696354 | -110463704 | -110463704 | 2.432 | 60.81 | 2.116 | 52.89 |
| threading | 4.145853 | 4.461545 | -110463704 | -110463704 | 2.396 | 59.90 | 2.227 | 55.67 |
| ProcessPoolExecutor | 3.148144 | 3.066812 | -110463704 | -110463704 | 3.155 | 78.88 | 3.240 | 80.99 |
| numba (njit) | 0.536763 | 0.544091 | -110463704 | -110463704 | 18.505 | 462.63 | 18.261 | 456.53 |

### Experimento 3: C = 1024, workers = 4

| Metodo | t(A*B) [s] | t(B^T*A^T) [s] | Checksum A*B | Checksum B^T*A^T | Speed-up A*B | Performance A*B [%] | Speed-up B^T*A^T | Performance B^T*A^T [%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Secuencial tradicional | 241.177753 | 202.201683 | 34818311 | 34818311 | 1.000 | 100.00 | 1.000 | 100.00 |
| Secuencial optimizada (transpuesta) | 62.864523 | 56.041876 | 34818311 | 34818311 | 3.836 | 383.65 | 3.608 | 360.80 |
| ThreadPoolExecutor | 31.794210 | 35.050143 | 34818311 | 34818311 | 7.586 | 189.64 | 5.769 | 144.22 |
| threading | 35.203877 | 34.519706 | 34818311 | 34818311 | 6.851 | 171.27 | 5.858 | 146.44 |
| ProcessPoolExecutor | 26.970618 | 27.427959 | 34818311 | 34818311 | 8.942 | 223.56 | 7.372 | 184.30 |
| numba (njit) | 2.495315 | 2.658940 | 34818311 | 34818311 | 96.652 | 2416.31 | 76.046 | 1901.15 |

### Experimento 4: C = 1024, workers = 10

| Metodo | t(A*B) [s] | t(B^T*A^T) [s] | Checksum A*B | Checksum B^T*A^T | Speed-up A*B | Performance A*B [%] | Speed-up B^T*A^T | Performance B^T*A^T [%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Secuencial tradicional | 238.791204 | 167.554144 | 34818311 | 34818311 | 1.000 | 100.00 | 1.000 | 100.00 |
| Secuencial optimizada (transpuesta) | 63.178100 | 58.877171 | 34818311 | 34818311 | 3.780 | 377.97 | 2.846 | 284.58 |
| ThreadPoolExecutor | 18.996816 | 25.321023 | 34818311 | 34818311 | 12.570 | 125.70 | 6.617 | 66.17 |
| threading | 23.905233 | 24.927668 | 34818311 | 34818311 | 9.989 | 99.89 | 6.722 | 67.22 |
| ProcessPoolExecutor | 20.399256 | 20.461559 | 34818311 | 34818311 | 11.706 | 117.06 | 8.189 | 81.89 |
| numba (njit) | 2.457141 | 2.359226 | 34818311 | 34818311 | 97.183 | 971.83 | 71.021 | 710.21 |

### Experimento 5: C = 1024, workers = 16

| Metodo | t(A*B) [s] | t(B^T*A^T) [s] | Checksum A*B | Checksum B^T*A^T | Speed-up A*B | Performance A*B [%] | Speed-up B^T*A^T | Performance B^T*A^T [%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Secuencial tradicional | 216.238226 | 176.607797 | 34818311 | 34818311 | 1.000 | 100.00 | 1.000 | 100.00 |
| Secuencial optimizada (transpuesta) | 69.697017 | 57.396771 | 34818311 | 34818311 | 3.103 | 310.25 | 3.077 | 307.70 |
| ThreadPoolExecutor | 18.180905 | 25.259255 | 34818311 | 34818311 | 11.894 | 74.34 | 6.992 | 43.70 |
| threading | 23.817357 | 23.784791 | 34818311 | 34818311 | 9.079 | 56.74 | 7.425 | 46.41 |
| ProcessPoolExecutor | 18.492709 | 18.103380 | 34818311 | 34818311 | 11.693 | 73.08 | 9.756 | 60.97 |
| numba (njit) | 2.391426 | 3.608904 | 34818311 | 34818311 | 90.422 | 565.14 | 48.937 | 305.85 |

## Resultados

Los valores de las tablas muestran que la version secuencial optimizada por transposicion mejora de forma sostenida al secuencial tradicional en todas las corridas. Para `C=512` baja de ~9.3 s a ~6.6 s, y para `C=1024` pasa de rangos entre ~216 y ~241 s a rangos entre ~62 y ~70 s.

En los metodos con hilos (`threading` y `ThreadPoolExecutor`) se observa mejora en tiempo absoluto, pero con degradacion de performance relativa al aumentar workers. Esto se acentua en `C=1024` con `workers=10` y `workers=16`, lo cual es consistente con una carga CPU-bound limitada por GIL y por overhead de coordinacion.

`ProcessPoolExecutor` mejora sobre los metodos con hilos en la mayoria de escenarios de `C=1024`, con mejor aprovechamiento del paralelismo al usar procesos separados. Aun asi, el speed-up no crece linealmente con workers debido a costos de creacion/sincronizacion, transferencia de datos y contencion de memoria/cache.

`numba (njit)` mantiene el mejor desempeno global en todos los experimentos. En `C=1024` obtiene tiempos cercanos a 2.4-3.6 s frente a mas de 160 s del baseline secuencial tradicional, logrando los speed-ups mas altos del conjunto.

La correctitud numerica queda validada porque los checksums coinciden entre metodos dentro de cada complejidad: `-110463704` para `C=512` y `34818311` para `C=1024`.

