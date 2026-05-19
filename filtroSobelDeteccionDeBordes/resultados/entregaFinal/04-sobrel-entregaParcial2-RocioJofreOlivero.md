# Título

Informe de rendimiento: filtro de Sobel para detección de bordes en Python

## Abstract

En este trabajo se implementa y compara el filtro de Sobel para detección de bordes sobre imágenes
RGB de distintas resoluciones. Se presentan los resultados de la primera y segunda entrega del
trabajo práctico. En la primera entrega se comparan tres implementaciones: secuencial pura,
vectorizada con NumPy y paralela en CPU con Numba. En la segunda entrega se incorpora una
versión Numba GPU con CUDA y se la compara contra Numba paralelo CPU.

Los experimentos se ejecutan sobre imágenes de `750x750`, `1500x1500`, `3000x3000` y
`6000x6000`, realizando 5 corridas por método y tamaño. Se registran por separado el tiempo de
conversión RGB a escala de grises, el tiempo de aplicación de Sobel, el tiempo total, el porcentaje
de píxeles blancos, el speed-up y la performance. Para GPU se registran además las transferencias
CPU→GPU y GPU→CPU.

Los resultados muestran que NumPy mejora fuertemente respecto de la versión secuencial, Numba
paralelo CPU obtiene los mejores tiempos de la primera entrega, y Numba GPU mejora el tiempo de
cómputo puro frente a Numba CPU. Sin embargo, al sumar las transferencias entre CPU y GPU, la
versión GPU no supera a CPU en estas mediciones.

## Introducción

El procesamiento de imágenes es una carga de trabajo adecuada para estudiar técnicas de
optimización y paralelización, ya que aplica operaciones repetitivas sobre grandes cantidades de
píxeles. En este trabajo se utiliza el operador de Sobel, un filtro clásico para detectar bordes o
contornos en una imagen.

Sobel estima cambios de intensidad en dos direcciones mediante dos máscaras de convolución:

```text
Gx = [-1  0  1]      Gy = [ 1  2  1]
     [-2  0  2]           [ 0  0  0]
     [-1  0  1]           [-1 -2 -1]
```

Para cada píxel interior se toma su vecindad `3x3`, se calculan `gx` y `gy`, y luego se obtiene la
magnitud del gradiente:

```text
|grad| = sqrt(gx^2 + gy^2)
```

El resultado se recorta al rango `[0, 255]`. Los valores cercanos a 0 representan zonas sin borde
fuerte, mientras que valores más altos representan cambios de intensidad más marcados. Como Sobel
trabaja sobre una sola intensidad por píxel, primero se convierte la imagen RGB a escala de grises
mediante luminancia:

```text
I = 0.299R + 0.587G + 0.114B
```

Desde el punto de vista del paralelismo, Sobel permite comparar varios enfoques sobre el mismo
cálculo: bucles secuenciales, vectorización sobre arreglos completos, paralelismo explícito en CPU
y ejecución masiva en GPU mediante CUDA.

## Metodologías

Se ejecutaron experimentos de benchmarking sobre las imágenes provistas para el trabajo. La carga
de imagen y el guardado de la salida quedan fuera de los tiempos medidos, para registrar solamente
el costo de cómputo de la conversión a gris y la aplicación del filtro Sobel.

### Entorno y hardware

- CPU: AMD Ryzen 5 5600X 6-Core Processor
  - 6 núcleos físicos, 12 hilos lógicos
- RAM: 15.52 GiB totales
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build, conda-forge
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

Configuraciones consideradas:

- Imágenes de entrada:
  - `IMG_0358_750x750.jpg`
  - `IMG_0358_1500x1500.jpg`
  - `IMG_0358_3000x3000.jpg`
  - `IMG_0358_6000x6000.jpg`
- Cantidad de corridas por combinación: 5.
- Métodos de la primera entrega:
  - secuencial puro;
  - NumPy;
  - Numba paralelo CPU.
- Método incorporado en la segunda entrega:
  - Numba GPU con CUDA.
- Numba CPU: 6 workers, coincidiendo con los 6 núcleos físicos del procesador.
- Numba GPU: bloques CUDA de `16x16`, es decir, 256 hilos por bloque.
- Salidas generadas: imágenes Sobel en formato `.png`.

Métricas registradas:

- tiempo de conversión RGB a escala de grises;
- tiempo de aplicación del filtro Sobel;
- tiempo total de cómputo;
- porcentaje de píxeles blancos (`valor 255`) en la imagen Sobel;
- speed-up;
- performance;
- checksum y hash de salida como control;
- transferencias CPU↔GPU para Numba GPU.

Para la primera entrega, el speed-up se calcula tomando como referencia a la versión secuencial:

```text
speed-up = tiempo total secuencial / tiempo total del método
```

Para la segunda entrega, el speed-up de GPU se calcula tomando como referencia a Numba CPU para
el mismo tamaño:

```text
speed-up GPU = tiempo total Numba CPU / tiempo total Numba GPU
```

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

## Entrega 1: Secuencial, NumPy y Numba CPU

### Experimento 1: imagen 750x750

| Método | RGB→gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.087378 | 0.286957 | 0.374334 | 0.281778 | 1.000000 | 100.00 |
| NumPy | 0.001907 | 0.002542 | 0.004449 | 0.281778 | 84.132985 | 8413.30 |
| Numba paralelo CPU | 0.000660 | 0.000338 | 0.000997 | 0.281778 | 375.331744 | 6255.53 |

### Experimento 2: imagen 1500x1500

| Método | RGB→gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.329165 | 1.145662 | 1.474827 | 0.059956 | 1.000000 | 100.00 |
| NumPy | 0.007318 | 0.010708 | 0.018026 | 0.059956 | 81.817345 | 8181.73 |
| Numba paralelo CPU | 0.001324 | 0.001058 | 0.002382 | 0.059956 | 619.085631 | 10318.09 |

### Experimento 3: imagen 3000x3000

| Método | RGB→gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 1.315055 | 4.403400 | 5.718456 | 0.001367 | 1.000000 | 100.00 |
| NumPy | 0.033103 | 0.073703 | 0.106806 | 0.001367 | 53.540383 | 5354.04 |
| Numba paralelo CPU | 0.004562 | 0.004740 | 0.009302 | 0.001367 | 614.785758 | 10246.43 |

### Experimento 4: imagen 6000x6000

| Método | RGB→gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 5.243595 | 17.420171 | 22.663766 | 0.000000 | 1.000000 | 100.00 |
| NumPy | 0.130965 | 0.280494 | 0.411459 | 0.000000 | 55.081437 | 5508.14 |
| Numba paralelo CPU | 0.015806 | 0.016697 | 0.032503 | 0.000000 | 697.283836 | 11621.40 |

### Resultados de la entrega 1

La versión secuencial es la más lenta en todos los tamaños, lo cual resulta esperable porque recorre
los píxeles con bucles Python puros. En `6000x6000`, por ejemplo, tarda 22.663766 s, de los cuales
17.420171 s corresponden a Sobel.

NumPy reduce los tiempos de forma marcada al expresar el cálculo mediante operaciones
vectorizadas. En `750x750`, el tiempo total baja de 0.374334 s a 0.004449 s. En `6000x6000`, baja
de 22.663766 s a 0.411459 s.

Numba paralelo CPU obtiene el mejor rendimiento global de la primera entrega. En `6000x6000`,
el tiempo total baja a 0.032503 s, con un speed-up de 697.283836 respecto de la versión
secuencial.

### Análisis de la entrega 1

**Diferencias de tiempo entre métodos.**
La diferencia de tiempo es muy marcada. La versión secuencial queda limitada por el costo de los
bucles Python. NumPy mejora al usar operaciones vectorizadas sobre arreglos completos, mientras
que Numba CPU compila los bucles y reparte trabajo mediante paralelismo en CPU. En todos los
tamaños, Numba CPU fue el método más rápido.

**Evolución del speed-up.**

| Tamaño | Speed-up NumPy | Speed-up Numba CPU |
|---:|---:|---:|
| 750x750 | 84.132985 | 375.331744 |
| 1500x1500 | 81.817345 | 619.085631 |
| 3000x3000 | 53.540383 | 614.785758 |
| 6000x6000 | 55.081437 | 697.283836 |

El speed-up de NumPy es alto en todos los casos, pero no crece de manera sostenida con el tamaño.
El speed-up de Numba CPU es mayor y tiende a ser más favorable en imágenes medianas y grandes.

**Equivalencia de resultados.**
Los porcentajes de píxeles blancos coinciden entre los tres métodos en todos los tamaños:

| Tamaño | % blancos |
|---:|---:|
| 750x750 | 0.281778 |
| 1500x1500 | 0.059956 |
| 3000x3000 | 0.001367 |
| 6000x6000 | 0.000000 |

Esto permite comparar los tiempos de manera consistente. Las pequeñas diferencias de checksum en
NumPy no cambian la métrica principal de la consigna ni la salida visual esperada.

## Entrega 2: Numba GPU

En la segunda entrega se incorpora una versión `numba_gpu` basada en `numba.cuda`. La estructura
sigue el código de referencia compartido por el docente:

- un kernel CUDA para convertir RGB a gris;
- un kernel CUDA para aplicar Sobel;
- grilla bidimensional;
- bloques de `16x16` hilos;
- un hilo CUDA por píxel;
- sincronización explícita con `cuda.synchronize()` antes de cerrar cada medición.

### Experimento 1: imagen 750x750

| Método | RGB→gris [s] | Sobel [s] | Total cómputo [s] | Píxeles blancos [%] | Speed-up vs CPU | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.000571 | 0.000238 | 0.000809 | 0.281778 | 1.000000 | 100.00 |
| Numba GPU | 0.000138 | 0.000303 | 0.000441 | 0.281778 | 1.835928 | 183.59 |

### Experimento 2: imagen 1500x1500

| Método | RGB→gris [s] | Sobel [s] | Total cómputo [s] | Píxeles blancos [%] | Speed-up vs CPU | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.001601 | 0.001397 | 0.002998 | 0.059956 | 1.000000 | 100.00 |
| Numba GPU | 0.000430 | 0.001081 | 0.001511 | 0.059956 | 1.983475 | 198.35 |

### Experimento 3: imagen 3000x3000

| Método | RGB→gris [s] | Sobel [s] | Total cómputo [s] | Píxeles blancos [%] | Speed-up vs CPU | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.003457 | 0.004142 | 0.007598 | 0.001367 | 1.000000 | 100.00 |
| Numba GPU | 0.001099 | 0.004376 | 0.005475 | 0.001367 | 1.387929 | 138.79 |

### Experimento 4: imagen 6000x6000

| Método | RGB→gris [s] | Sobel [s] | Total cómputo [s] | Píxeles blancos [%] | Speed-up vs CPU | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Numba paralelo CPU | 0.012564 | 0.014839 | 0.027403 | 0.000000 | 1.000000 | 100.00 |
| Numba GPU | 0.003973 | 0.017432 | 0.021405 | 0.000000 | 1.280216 | 128.02 |

### Transferencias CPU↔GPU

| Tamaño | Transferencia CPU→GPU [s] | Transferencia GPU→CPU [s] | Transferencia total [s] | Cómputo GPU [s] | GPU con transferencias [s] | Speed-up incluyendo transferencias |
|---:|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000598 | 0.000213 | 0.000811 | 0.000441 | 0.001252 | 0.646284 |
| 1500x1500 | 0.001302 | 0.000682 | 0.001984 | 0.001511 | 0.003495 | 0.857667 |
| 3000x3000 | 0.003251 | 0.001517 | 0.004768 | 0.005475 | 0.010242 | 0.741860 |
| 6000x6000 | 0.011006 | 0.005107 | 0.016113 | 0.021405 | 0.037518 | 0.730399 |

### Análisis de la entrega 2

**Mejora de tiempo entre Numba GPU y Numba paralelo CPU.**
En tiempo de cómputo puro, Numba GPU mejora a Numba CPU en todos los tamaños:

| Tamaño | Tiempo CPU [s] | Tiempo GPU [s] | Mejora GPU |
|---:|---:|---:|---:|
| 750x750 | 0.000809 | 0.000441 | 1.835928x |
| 1500x1500 | 0.002998 | 0.001511 | 1.983475x |
| 3000x3000 | 0.007598 | 0.005475 | 1.387929x |
| 6000x6000 | 0.027403 | 0.021405 | 1.280216x |

La mejora no es igual en todas las etapas. GPU acelera más la conversión RGB→gris que el filtro
Sobel. En Sobel, el acceso a vecinos `3x3` aumenta la presión sobre memoria y reduce parte de la
ventaja esperada.

**Amortización del costo de transferencia CPU↔GPU.**
En estas mediciones, el costo de transferencia no se amortiza completamente si se considera una
ejecución completa que copia la imagen a GPU y devuelve el resultado a CPU para cada corrida.
Sin embargo, el peso relativo de la transferencia baja al crecer la imagen:

| Tamaño | Porcentaje del tiempo GPU total ocupado por transferencias |
|---:|---:|
| 750x750 | 64.80% |
| 1500x1500 | 56.76% |
| 3000x3000 | 46.55% |
| 6000x6000 | 42.95% |

Esto indica que el costo empieza a amortizarse mejor en `3000x3000` y `6000x6000`, aunque todavía
no alcanza para que GPU supere a CPU si se suman transferencias.

**Evolución del speed-up de Numba GPU.**
El speed-up de GPU no crece de forma monótona con la resolución. Sube de `750x750` a `1500x1500`,
pero luego baja en `3000x3000` y `6000x6000`. Esto muestra un cambio de tendencia: la GPU obtiene
ventaja en el cómputo, pero la etapa Sobel no escala tan favorablemente como la conversión a gris.

## Equivalencia de salidas

La métrica solicitada por la consigna es el porcentaje de píxeles blancos. Para las implementaciones
comparadas, ese porcentaje coincide por tamaño:

| Tamaño | Píxeles blancos | % blancos |
|---:|---:|---:|
| 750x750 | 1585 | 0.281778 |
| 1500x1500 | 1349 | 0.059956 |
| 3000x3000 | 123 | 0.001367 |
| 6000x6000 | 0 | 0.000000 |

En `6000x6000`, el porcentaje de píxeles blancos es 0 porque ningún píxel llega exactamente al
valor 255. Esto no significa que no haya bordes: la imagen Sobel contiene valores de gris, pero no
bordes saturados al blanco puro.

Los checksums y hashes pueden presentar pequeñas diferencias entre algunos métodos por diferencias
de redondeo o aritmética entre implementaciones. La salida visual y el porcentaje de píxeles blancos
se mantienen consistentes para el objetivo del trabajo.

## Conclusiones

La implementación secuencial funciona como línea base y muestra el costo de resolver Sobel con
bucles Python puros. Sus tiempos crecen junto con la cantidad de píxeles de la imagen.

NumPy ofrece una aceleración importante sin administrar workers manualmente. Su ventaja proviene
de la vectorización sobre arreglos completos y de evitar bucles Python explícitos.

Numba paralelo CPU logra el mejor rendimiento de la primera entrega. Al compilar los bucles y
repartir trabajo entre 6 workers, reduce de forma muy significativa el tiempo total frente a las
otras implementaciones de CPU.

Numba GPU mejora el tiempo de cómputo puro frente a Numba CPU en todos los tamaños medidos.
La ventaja es más clara en la conversión RGB→gris, donde cada píxel puede procesarse de forma
independiente con poco trabajo adicional.

Al incluir transferencias CPU↔GPU, la versión GPU no supera a Numba CPU en estas mediciones.
Esto confirma lo señalado en la teoría de la materia: usar GPU no garantiza automáticamente menor
tiempo total. La aceleración depende de que el problema tenga suficiente trabajo paralelo y de que
el costo de mover datos no domine la ejecución.

En conjunto, los resultados permiten observar una progresión clara: Python secuencial sirve como
referencia, NumPy mejora al vectorizar, Numba CPU acelera al compilar y paralelizar sobre CPU, y
Numba GPU muestra el potencial del paralelismo masivo, aunque condicionado por las transferencias
entre host y dispositivo.

## Archivos de resultados usados

- `resultados/entrega1/finales/03-sobel-ROCIOJOFREOLIVERO.md`
- `resultados/entrega2/finales/03-sobel-entrega2-ROCIOJOFREOLIVERO.md`
- `resultados/entrega1/resultados_sobel_750x750.csv`
- `resultados/entrega1/resultados_sobel_1500x1500.csv`
- `resultados/entrega1/resultados_sobel_3000x3000.csv`
- `resultados/entrega1/resultados_sobel_6000x6000.csv`
- `resultados/entrega2/resultados_sobel_750x750.csv`
- `resultados/entrega2/resultados_sobel_1500x1500.csv`
- `resultados/entrega2/resultados_sobel_3000x3000.csv`
- `resultados/entrega2/resultados_sobel_6000x6000.csv`
