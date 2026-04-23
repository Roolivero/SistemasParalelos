# Informe — Trabajo Práctico de Multiplicación de Matrices

## 1) Entorno y hardware

- **CPU:** Intel(R) Core(TM) Ultra 9 185H  
  - 16 núcleos físicos, 22 hilos lógicos
- **RAM:** 30 GiB totales (18 GiB disponibles al momento del relevamiento)
- **Sistema operativo:** Linux Manjaro 6.12.77-1-MANJARO
- **Versión de Python:** 3.14.3
- **GPU (CUDA/MPS):** no se detecta `nvidia-smi` en el entorno actual, por lo que no se incluyen resultados de PyTorch.

## 2) Metodología

Se analizaron las corridas disponibles en `matrices/v2/resultados` para las combinaciones:

- `--workers 1 --complexity 512`
- `--workers 4 --complexity 512`
- `--workers 4 --complexity 1024`
- `--workers 10 --complexity 1024` (corrida adicional respecto de lo pedido como “N físicos”)

Para cada corrida se registraron tiempos de:

- Producto `A·B`
- Producto `Bᵀ·Aᵀ`

Y se relevaron:

- `checksum` de cada resultado
- `speed-up`
- `eficiencia` (performance relativa por worker)

## 3) Tablas comparativas

> Nota: en todas las tablas el checksum coincide entre métodos para una misma complejidad, validando corrección numérica.

### 3.1) C = 512, workers = 1

| Método | t(A·B) [s] | t(Bᵀ·Aᵀ) [s] | Speed-up A·B | Performance A·B [%] | Speed-up Bᵀ·Aᵀ | Performance Bᵀ·Aᵀ [%] | Checksum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Secuencial (tradicional) | 9.286013 | 9.303695 | 1.000 | 100.00 | 1.000 | 100.00 | -110463704 |
| Secuencial (optimizada / transpuesta) | 6.594259 | 6.329482 | 1.408 | 140.82 | 1.470 | 146.99 | -110463704 |
| ThreadPoolExecutor | 7.070678 | 7.524049 | 1.313 | 131.33 | 1.237 | 123.65 | -110463704 |
| threading | 7.261479 | 7.233229 | 1.279 | 127.88 | 1.286 | 128.62 | -110463704 |
| ProcessPoolExecutor | 6.942384 | 6.634457 | 1.338 | 133.76 | 1.402 | 140.23 | -110463704 |
| numba (njit) | 0.580156 | 0.610545 | 16.006 | 1600.61 | 15.238 | 1523.83 | -110463704 |

### 3.2) C = 512, workers = 4

| Método | t(A·B) [s] | t(Bᵀ·Aᵀ) [s] | Speed-up A·B | Performance A·B [%] | Speed-up Bᵀ·Aᵀ | Performance Bᵀ·Aᵀ [%] | Checksum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Secuencial (tradicional) | 9.933010 | 9.935754 | 1.000 | 100.00 | 1.000 | 100.00 | -110463704 |
| Secuencial (optimizada / transpuesta) | 6.589254 | 6.361890 | 1.507 | 150.75 | 1.562 | 156.18 | -110463704 |
| ThreadPoolExecutor | 4.083622 | 4.696354 | 2.432 | 60.81 | 2.116 | 52.89 | -110463704 |
| threading | 4.145853 | 4.461545 | 2.396 | 59.90 | 2.227 | 55.67 | -110463704 |
| ProcessPoolExecutor | 3.148144 | 3.066812 | 3.155 | 78.88 | 3.240 | 80.99 | -110463704 |
| numba (njit) | 0.536763 | 0.544091 | 18.505 | 462.63 | 18.261 | 456.53 | -110463704 |

### 3.3) C = 1024, workers = 4

| Método | t(A·B) [s] | t(Bᵀ·Aᵀ) [s] | Speed-up A·B | Performance A·B [%] | Speed-up Bᵀ·Aᵀ | Performance Bᵀ·Aᵀ [%] | Checksum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Secuencial (tradicional) | 241.177753 | 202.201683 | 1.000 | 100.00 | 1.000 | 100.00 | 34818311 |
| Secuencial (optimizada / transpuesta) | 62.864523 | 56.041876 | 3.836 | 383.65 | 3.608 | 360.80 | 34818311 |
| ThreadPoolExecutor | 31.794210 | 35.050143 | 7.586 | 189.64 | 5.769 | 144.22 | 34818311 |
| threading | 35.203877 | 34.519706 | 6.851 | 171.27 | 5.858 | 146.44 | 34818311 |
| ProcessPoolExecutor | 26.970618 | 27.427959 | 8.942 | 223.56 | 7.372 | 184.30 | 34818311 |
| numba (njit) | 2.495315 | 2.658940 | 96.652 | 2416.31 | 76.046 | 1901.15 | 34818311 |

### 3.4) C = 1024, workers = 10

| Método | t(A·B) [s] | t(Bᵀ·Aᵀ) [s] | Speed-up A·B | Performance A·B [%] | Speed-up Bᵀ·Aᵀ | Performance Bᵀ·Aᵀ [%] | Checksum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Secuencial (tradicional) | 238.791204 | 167.554144 | 1.000 | 100.00 | 1.000 | 100.00 | 34818311 |
| Secuencial (optimizada / transpuesta) | 63.178100 | 58.877171 | 3.780 | 377.97 | 2.846 | 284.58 | 34818311 |
| ThreadPoolExecutor | 18.996816 | 25.321023 | 12.570 | 125.70 | 6.617 | 66.17 | 34818311 |
| threading | 23.905233 | 24.927668 | 9.989 | 99.89 | 6.722 | 67.22 | 34818311 |
| ProcessPoolExecutor | 20.399256 | 20.461559 | 11.706 | 117.06 | 8.189 | 81.89 | 34818311 |
| numba (njit) | 2.457141 | 2.359226 | 97.183 | 971.83 | 71.021 | 710.21 | 34818311 |

## 4) Análisis (respuestas breves a la consigna)

### 4.1) ¿Por qué `threading` no mejora en esta carga de trabajo?

Porque la multiplicación de matrices en Python puro es **CPU-bound** y está limitada por el **GIL** (Global Interpreter Lock). Aunque se lancen varios hilos, no ejecutan bytecode Python en paralelo real dentro de un mismo proceso, por lo que la mejora es baja o nula frente al costo extra de coordinación de hilos.

### 4.2) ¿Qué explica la mejora de las versiones con matriz transpuesta?

La transposición mejora la **localidad de memoria**: en vez de acceder columnas con saltos grandes (cache-unfriendly), se recorren filas contiguas en memoria. Eso reduce fallos de caché y mejora el throughput del CPU, lo que se observa en menores tiempos respecto al secuencial tradicional.

### 4.3) ¿El speed-up de `multiprocessing` es lineal con los workers? ¿Por qué?

No es lineal. Aumentar workers mejora tiempos, pero aparecen costos de:

- creación y sincronización de procesos,
- serialización/copia de datos entre procesos,
- competencia por memoria/caché/ancho de banda.

Además, según Amdahl, siempre hay parte secuencial no paralelizable, por lo que el escalado perfecto no se mantiene.

### 4.4) ¿Qué aporta `numba.njit` incluso sin paralelismo (`parallel=False`)?

`numba.njit` compila el código numérico a código máquina (evitando gran parte del overhead del intérprete de Python), aplica optimizaciones de bajo nivel y opera de forma mucho más eficiente sobre bucles intensivos. Por eso logra mejoras muy grandes incluso sin paralelismo explícito.

### 4.5) ¿Se puede superar una eficiencia del 100%? ¿Cómo se interpreta eso?

Sí, puede aparecer una “eficiencia > 100%” según cómo se defina el baseline. En estas tablas, el speed-up se calcula contra el **secuencial tradicional**; por lo tanto, métodos que además de paralelizar también **optimizan el algoritmo/implementación** (transposición, JIT, mejor uso de caché) pueden superar ese 100%.

No implica “más de un core por core”, sino que la métrica mezcla **paralelismo + optimización algorítmica/implementación**.

## 5) Conclusiones

- Se verifica corrección numérica: para cada complejidad, todos los métodos producen el mismo checksum.
- `threading`/`ThreadPoolExecutor` muestran mejoras limitadas para CPU-bound en Python puro.
- `multiprocessing` mejora de forma consistente y supera a threading, pero con escalado sublineal.
- La versión transpuesta mejora al secuencial tradicional por acceso a memoria más favorable.
- `numba (njit)` es el método con mejor desempeño global por amplio margen.

## 6) Observaciones para cierre de entrega

- La consigna pide una corrida con `--workers N físicos --complexity 1024`; en este set aparece `workers = 10`, mientras que el CPU detectado tiene 16 núcleos físicos. Conviene agregar esa corrida para cumplir estrictamente.
- Verificar y dejar explícito en el informe final que las corridas se ejecutaron con `--seed 2026`.
- Si el entorno no dispone de GPU/PyTorch, dejar aclarado (como se hizo arriba) que no se reportan esos resultados y por qué.

