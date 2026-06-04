# Informe de rendimiento: filtro de Sobel para detección de bordes en Python

## Abstract

En este trabajo se implementa y compara el filtro de Sobel para detección de bordes sobre imágenes
RGB de distintas resoluciones. El informe integra las tres entregas del trabajo práctico: la primera
entrega incluye las versiones secuencial pura, NumPy y Numba paralelo CPU; la segunda incorpora
Numba GPU con CUDA; y la tercera agrega PyTorch CPU y PyTorch GPU.

Los experimentos se ejecutan sobre imágenes de `750x750`, `1500x1500`, `3000x3000` y
`6000x6000`, realizando 5 corridas por método y tamaño. Se registran por separado el tiempo de
conversión RGB a escala de grises, el tiempo de aplicación de Sobel, el tiempo total, el porcentaje
de píxeles blancos, el speed-up y la performance. Para las versiones GPU se registran además las
transferencias CPU->GPU y GPU->CPU.

Para que la comparación principal sea consistente en todo el documento, las tablas globales calculan
el speed-up de todos los métodos respecto de la versión secuencial. Luego, en los análisis específicos,
se agregan comparaciones directas entre Numba GPU y Numba CPU, y entre PyTorch GPU y PyTorch CPU,
para observar con más detalle qué ocurre dentro de cada familia de implementación.

Los resultados muestran una progresión clara: la versión secuencial funciona como línea base,
NumPy acelera al reformular el cálculo sobre arreglos completos, Numba CPU mejora al compilar
y paralelizar los bucles en CPU, Numba GPU reduce aún más el tiempo de cómputo puro frente a la
referencia secuencial, y PyTorch permite expresar el mismo problema con tensores en CPU y GPU.
PyTorch GPU mejora claramente a PyTorch CPU, aunque en estas mediciones Numba GPU conserva los
mejores tiempos de cómputo entre las implementaciones evaluadas.

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
cálculo: bucles secuenciales, vectorización sobre arreglos completos, paralelismo explícito en CPU,
ejecución masiva en GPU mediante CUDA y operaciones sobre tensores con PyTorch.

## Metodología

Se ejecutaron experimentos de benchmarking sobre las imágenes provistas para el trabajo. La carga
de imagen y el guardado de la salida quedan fuera de los tiempos medidos, para registrar solamente
el costo de cómputo de la conversión a gris y la aplicación del filtro Sobel.

### Entorno y hardware

Para las entregas 1 y 2 se utilizó el entorno Python usado previamente para NumPy y Numba:

- CPU: AMD Ryzen 5 5600X 6-Core Processor
  - 6 núcleos físicos, 12 hilos lógicos
- RAM: 15.52 GiB total, entre 8.38 y 10.79 GiB disponible durante las mediciones
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build, conda-forge
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

Para la entrega 3 se utilizó un entorno CPython estándar compatible con PyTorch:

- CPU: AMD Ryzen 5 5600X 6-Core Processor
  - 6 núcleos físicos, 12 hilos lógicos
- RAM: 15.52 GiB total, entre 10.19 y 10.37 GiB disponible durante las mediciones
- Sistema operativo: Linux-6.18.33-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.12.13, conda-forge
- NumPy: 2.4.6
- PyTorch: 2.10.0
- PyTorch CUDA: NVIDIA GeForce RTX 2060 (CUDA 13.0)

El cambio de entorno para PyTorch se debe a que PyTorch no estaba disponible para el ABI
free-threading del entorno Python 3.14 usado en las entregas anteriores. Esto no invalida la
comparación, porque las operaciones medidas en PyTorch se ejecutan sobre tensores mediante
bibliotecas internas optimizadas y, en GPU, mediante CUDA.

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
- Métodos incorporados en la tercera entrega:
  - PyTorch CPU;
  - PyTorch GPU.
- Numba CPU y PyTorch CPU: 6 workers, coincidiendo con los 6 núcleos físicos del procesador.
- Numba GPU: bloques CUDA de `16x16`, es decir, 256 hilos por bloque.
- PyTorch GPU: tensores en `cuda` y operaciones de convolución 2D.
- Salidas generadas: imágenes Sobel en formato `.png`.

Métricas registradas:

- tiempo de conversión RGB a escala de grises;
- tiempo de aplicación del filtro Sobel;
- tiempo total de cómputo;
- porcentaje de píxeles blancos (`valor 255`) en la imagen Sobel;
- speed-up;
- performance;
- checksum y hash de salida como control;
- transferencias CPU<->GPU para Numba GPU y PyTorch GPU.

### Criterio de comparación

En todas las tablas principales se usa la misma referencia:

```text
speed-up = tiempo total secuencial / tiempo total del método
```

La performance se calcula como:

```text
performance (%) = speed-up / unidades usadas * 100
```

Para Numba CPU y PyTorch CPU se usan 6 unidades, correspondientes a los workers configurados.
Para secuencial, NumPy y las versiones GPU se usa 1 unidad explícita. En GPU no se divide por la
cantidad de hilos CUDA, porque esos hilos no son equivalentes a núcleos CPU ni a workers
configurables del mismo modo.

Para responder preguntas específicas de cada entrega, se incluyen además comparaciones secundarias:

```text
mejora Numba GPU vs Numba CPU = tiempo total Numba CPU / tiempo total Numba GPU
mejora PyTorch GPU vs PyTorch CPU = tiempo total PyTorch CPU / tiempo total PyTorch GPU
```

Esas comparaciones no reemplazan a las tablas principales; solo se usan dentro de los análisis
específicos de GPU.

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

## Resultados globales por tamaño

Las siguientes tablas integran los métodos de las tres entregas. De este modo, cada implementación
queda conectada con la misma línea base secuencial.

Para `secuencial`, `numpy` y `numba_cpu` se usan los resultados de la entrega 1. Para `numba_gpu`
se usan los resultados de la entrega 2. Para `pytorch_cpu` y `pytorch_gpu` se usan los resultados
de la entrega 3.

El porcentaje de píxeles blancos se mantiene igual para todos los métodos dentro de cada tamaño,
por eso aparece repetido en las filas. En `6000x6000` queda en 0.000000 porque ningún píxel llega
exactamente al valor 255; esto no significa que no haya bordes, sino que la imagen Sobel contiene
valores de gris sin saturar al blanco puro. Los checksums y hashes pueden variar levemente entre
algunas implementaciones por diferencias de redondeo u orden de operaciones, pero la salida visual
y el porcentaje de píxeles blancos se mantienen consistentes para comparar los métodos.

### Imagen 750x750

| Método | RGB->gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up vs secuencial | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.087378 | 0.286957 | 0.374334 | 0.281778 | 1.000000 | 100.00 |
| NumPy | 0.001907 | 0.002542 | 0.004449 | 0.281778 | 84.132985 | 8413.30 |
| Numba paralelo CPU | 0.000660 | 0.000338 | 0.000997 | 0.281778 | 375.331744 | 6255.53 |
| Numba GPU | 0.000138 | 0.000303 | 0.000441 | 0.281778 | 849.191126 | 84919.11 |
| PyTorch CPU | 0.001091 | 0.006944 | 0.008035 | 0.281778 | 46.588447 | 776.47 |
| PyTorch GPU | 0.000263 | 0.000935 | 0.001199 | 0.281778 | 312.289446 | 31228.94 |

### Imagen 1500x1500

| Método | RGB->gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up vs secuencial | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.329165 | 1.145662 | 1.474827 | 0.059956 | 1.000000 | 100.00 |
| NumPy | 0.007318 | 0.010708 | 0.018026 | 0.059956 | 81.817345 | 8181.73 |
| Numba paralelo CPU | 0.001324 | 0.001058 | 0.002382 | 0.059956 | 619.085631 | 10318.09 |
| Numba GPU | 0.000430 | 0.001081 | 0.001511 | 0.059956 | 975.774969 | 97577.50 |
| PyTorch CPU | 0.012191 | 0.032779 | 0.044970 | 0.059956 | 32.795916 | 546.60 |
| PyTorch GPU | 0.000978 | 0.001502 | 0.002481 | 0.059956 | 594.486578 | 59448.66 |

### Imagen 3000x3000

| Método | RGB->gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up vs secuencial | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 1.315055 | 4.403400 | 5.718456 | 0.001367 | 1.000000 | 100.00 |
| NumPy | 0.033103 | 0.073703 | 0.106806 | 0.001367 | 53.540383 | 5354.04 |
| Numba paralelo CPU | 0.004562 | 0.004740 | 0.009302 | 0.001367 | 614.785758 | 10246.43 |
| Numba GPU | 0.001099 | 0.004376 | 0.005475 | 0.001367 | 1044.539074 | 104453.91 |
| PyTorch CPU | 0.058908 | 0.161520 | 0.220428 | 0.001367 | 25.942556 | 432.38 |
| PyTorch GPU | 0.003475 | 0.004065 | 0.007539 | 0.001367 | 758.504381 | 75850.44 |

### Imagen 6000x6000

| Método | RGB->gris [s] | Sobel [s] | Total [s] | Píxeles blancos [%] | Speed-up vs secuencial | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 5.243595 | 17.420171 | 22.663766 | 0.000000 | 1.000000 | 100.00 |
| NumPy | 0.130965 | 0.280494 | 0.411459 | 0.000000 | 55.081437 | 5508.14 |
| Numba paralelo CPU | 0.015806 | 0.016697 | 0.032503 | 0.000000 | 697.283836 | 11621.40 |
| Numba GPU | 0.003973 | 0.017432 | 0.021405 | 0.000000 | 1058.816812 | 105881.68 |
| PyTorch CPU | 0.229955 | 0.652591 | 0.882546 | 0.000000 | 25.679986 | 428.00 |
| PyTorch GPU | 0.014273 | 0.014200 | 0.028473 | 0.000000 | 795.962099 | 79596.21 |

## Análisis de la entrega 1

La entrega 1 compara las versiones secuencial, NumPy y Numba paralelo CPU.

### 1. Diferencias de tiempo entre secuencial, NumPy y Numba CPU

La versión secuencial es la más lenta en todos los tamaños, lo cual resulta esperable porque recorre
los píxeles con bucles Python puros. En `6000x6000`, por ejemplo, tarda 22.663766 s, de los cuales
17.420171 s corresponden a Sobel.

NumPy reduce los tiempos de forma marcada al expresar el cálculo mediante operaciones vectorizadas.
En `750x750`, el tiempo total baja de 0.374334 s a 0.004449 s. En `6000x6000`, baja de
22.663766 s a 0.411459 s.

Numba paralelo CPU obtiene el mejor rendimiento de la primera entrega. En `6000x6000`, el tiempo
total baja a 0.032503 s, con un speed-up de 697.283836 respecto de la versión secuencial.

### 2. Evolución del speed-up de NumPy y Numba CPU respecto de secuencial

| Tamaño | Speed-up NumPy | Speed-up Numba CPU |
|---:|---:|---:|
| 750x750 | 84.132985 | 375.331744 |
| 1500x1500 | 81.817345 | 619.085631 |
| 3000x3000 | 53.540383 | 614.785758 |
| 6000x6000 | 55.081437 | 697.283836 |

El speed-up de NumPy es alto en todos los casos, pero no crece de manera sostenida con el tamaño.
NumPy depende de operaciones vectorizadas sobre arreglos completos y evita bucles Python, pero no
se configuró un paralelismo explícito controlado por workers.

El speed-up de Numba CPU es mayor y tiende a ser más favorable en imágenes medianas y grandes.
La mejora se explica por la combinación de compilación JIT y paralelismo explícito sobre filas de
la imagen mediante `prange`.

### 3. Equivalencia de resultados en la entrega 1

Los porcentajes de píxeles blancos coinciden entre los tres métodos en todos los tamaños:

| Tamaño | % blancos |
|---:|---:|
| 750x750 | 0.281778 |
| 1500x1500 | 0.059956 |
| 3000x3000 | 0.001367 |
| 6000x6000 | 0.000000 |

Esto permite comparar los tiempos de manera consistente. Las pequeñas diferencias de checksum en
NumPy no cambian la métrica principal de la consigna ni la salida visual esperada. Esas diferencias
pueden aparecer por detalles de redondeo o por el orden de operaciones en cada implementación.

## Entrega 2: Numba GPU

En la segunda entrega se incorpora una versión `numba_gpu` basada en `numba.cuda`. La estructura
sigue el código de referencia compartido por el docente:

- un kernel CUDA para convertir RGB a gris;
- un kernel CUDA para aplicar Sobel;
- grilla bidimensional;
- bloques de `16x16` hilos;
- un hilo CUDA por píxel;
- sincronización explícita con `cuda.synchronize()` antes de cerrar cada medición.

En las tablas globales anteriores, Numba GPU ya fue comparado contra la versión secuencial. En esta
sección se mira con más detalle su relación con Numba paralelo CPU y el costo de transferir datos
entre CPU y GPU.

### Comparación específica Numba GPU vs Numba CPU

| Tamaño | Numba CPU total [s] | Numba GPU cómputo [s] | Mejora GPU vs CPU | GPU con transferencias [s] | Mejora GPU vs CPU con transferencias |
|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000809 | 0.000441 | 1.835928x | 0.001252 | 0.646284x |
| 1500x1500 | 0.002998 | 0.001511 | 1.983475x | 0.003495 | 0.857667x |
| 3000x3000 | 0.007598 | 0.005475 | 1.387929x | 0.010242 | 0.741860x |
| 6000x6000 | 0.027403 | 0.021405 | 1.280216x | 0.037518 | 0.730399x |

Esta tabla separa dos lecturas. Si se mira solo el cómputo, Numba GPU mejora a Numba CPU en todos
los tamaños. Pero si se suman las transferencias CPU->GPU y GPU->CPU, Numba GPU queda por detrás
de Numba CPU en estas mediciones: los valores de la última columna son menores que 1.

La mejora de cómputo tampoco es igual en todas las etapas. GPU acelera más la conversión RGB->gris
que el filtro Sobel. En Sobel, el acceso a vecinos `3x3` aumenta la presión sobre memoria y reduce
parte de la ventaja esperada.

### Detalle de transferencias CPU-GPU de Numba GPU

| Tamaño | Transferencia CPU->GPU [s] | Transferencia GPU->CPU [s] | Transferencia total [s] | Cómputo GPU [s] | GPU con transferencias [s] | Speed-up vs secuencial con transferencias | Speed-up vs Numba CPU con transferencias |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000598 | 0.000213 | 0.000811 | 0.000441 | 0.001252 | 298.932382 | 0.646284 |
| 1500x1500 | 0.001302 | 0.000682 | 0.001984 | 0.001511 | 0.003495 | 421.931227 | 0.857667 |
| 3000x3000 | 0.003251 | 0.001517 | 0.004768 | 0.005475 | 0.010242 | 558.314632 | 0.741860 |
| 6000x6000 | 0.011006 | 0.005107 | 0.016113 | 0.021405 | 0.037518 | 604.084616 | 0.730399 |

Esta tabla abre el costo de transferencia. Frente a la versión secuencial, Numba GPU sigue siendo
mucho más rápido incluso incluyendo copias de datos. Frente a Numba CPU, en cambio, ese costo
de transferencia es suficiente para perder la ventaja que aparecía al mirar solo el cómputo.

### 1. Mejora de tiempo entre Numba GPU y Numba paralelo CPU

En cómputo puro, la mejora GPU vs CPU va de 1.835928x en `750x750` a 1.280216x en `6000x6000`.
La mejor relación se observa en `1500x1500`, con 1.983475x. A partir de `3000x3000`, la ventaja
disminuye porque la etapa Sobel pesa más y no escala tan favorablemente como la conversión
RGB->gris.

### 2. Amortización del costo de transferencia CPU-GPU

En estas mediciones, el costo de transferencia no se amortiza completamente si se compara GPU
contra Numba CPU. Sin embargo, el peso relativo de la transferencia baja al crecer la imagen:

| Tamaño | Porcentaje del tiempo GPU total ocupado por transferencias |
|---:|---:|
| 750x750 | 64.80% |
| 1500x1500 | 56.76% |
| 3000x3000 | 46.55% |
| 6000x6000 | 42.95% |

Esto indica que el costo empieza a amortizarse mejor en `3000x3000` y `6000x6000`, aunque todavía
no alcanza para que GPU supere a Numba CPU si se suman transferencias. Si se compara contra la
línea base secuencial, la GPU sí mantiene una mejora amplia incluso con transferencias.

### 3. Evolución del speed-up de Numba GPU

Tomando como referencia la versión secuencial, el speed-up de Numba GPU crece en las imágenes
grandes:

| Tamaño | Speed-up Numba GPU vs secuencial |
|---:|---:|
| 750x750 | 849.191126 |
| 1500x1500 | 975.774969 |
| 3000x3000 | 1044.539074 |
| 6000x6000 | 1058.816812 |

Si se compara GPU contra Numba CPU mirando solo el cómputo, es decir, sin sumar transferencias,
el comportamiento no es monótono:

| Tamaño | Mejora GPU vs Numba CPU sin transferencias |
|---:|---:|
| 750x750 | 1.835928x |
| 1500x1500 | 1.983475x |
| 3000x3000 | 1.387929x |
| 6000x6000 | 1.280216x |

Las dos tablas muestran aspectos distintos del rendimiento. La referencia secuencial permite ubicar
a todos los métodos en una misma escala, mientras que la comparación directa GPU vs Numba CPU
sin transferencias sirve para analizar si el paso a GPU mejora el cómputo de la mejor versión CPU
disponible.

## Entrega 3: PyTorch CPU y PyTorch GPU

En la tercera entrega se incorporan `pytorch_cpu` y `pytorch_gpu`. En lugar de escribir kernels CUDA
manualmente, PyTorch expresa el cálculo mediante tensores y operaciones de alto nivel. La conversión
RGB->gris se resuelve con operaciones sobre tensores y Sobel se formula como una convolución 2D
con las máscaras `Gx` y `Gy`.

En las tablas globales anteriores, PyTorch CPU y PyTorch GPU ya fueron comparados contra la versión
secuencial. Esta sección agrega la comparación específica entre ambos métodos y los compara frente
a las mejores implementaciones previas.

### Comparación específica PyTorch CPU vs PyTorch GPU

| Tamaño | PyTorch CPU total [s] | PyTorch GPU cómputo [s] | Mejora GPU vs CPU | GPU con transferencias [s] | Mejora GPU vs CPU con transferencias |
|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.008035 | 0.001199 | 6.703152x | 0.001651 | 4.867165x |
| 1500x1500 | 0.044970 | 0.002481 | 18.126848x | 0.003869 | 11.623329x |
| 3000x3000 | 0.220428 | 0.007539 | 29.237843x | 0.011764 | 18.738020x |
| 6000x6000 | 0.882546 | 0.028473 | 30.995426x | 0.043321 | 20.372441x |

PyTorch GPU mejora a PyTorch CPU en todos los tamaños. La diferencia crece con la resolución:
en `750x750` la mejora de cómputo es 6.703152x, mientras que en `6000x6000` llega a 30.995426x.
Incluso sumando transferencias, PyTorch GPU sigue siendo más rápido que PyTorch CPU.

### Transferencias CPU-GPU de PyTorch GPU

| Tamaño | H2D CPU->GPU [s] | D2H GPU->CPU [s] | Transferencia total [s] | Cómputo GPU [s] | Total con transferencias [s] | Porcentaje de transferencias |
|---:|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000255 | 0.000197 | 0.000452 | 0.001199 | 0.001651 | 27.39% |
| 1500x1500 | 0.000742 | 0.000646 | 0.001388 | 0.002481 | 0.003869 | 35.88% |
| 3000x3000 | 0.002698 | 0.001527 | 0.004225 | 0.007539 | 0.011764 | 35.91% |
| 6000x6000 | 0.009766 | 0.005081 | 0.014847 | 0.028473 | 0.043321 | 34.27% |

En PyTorch GPU, las transferencias representan una parte importante del tiempo total, pero no anulan
la ventaja frente a PyTorch CPU. Esto marca una diferencia con el caso Numba GPU vs Numba CPU:
para PyTorch, la versión CPU es mucho más lenta que la GPU, por lo que la transferencia queda
amortizada incluso en la imagen más chica.

### Comparación de PyTorch contra el mejor método

En estas mediciones, el mejor método en cómputo puro fue Numba GPU para los cuatro tamaños. Por
eso se lo usa como referencia directa para ubicar los resultados de PyTorch.
Las columnas `PyTorch CPU / mejor método` y `PyTorch GPU / mejor método` indican cuántas veces
más lentas fueron las versiones de PyTorch frente a Numba GPU.

| Tamaño | Mejor método | Total mejor método [s] | PyTorch CPU / mejor método | PyTorch GPU / mejor método |
|---:|---|---:|---:|---:|
| 750x750 | Numba GPU | 0.000441 | 18.227505 | 2.719244 |
| 1500x1500 | Numba GPU | 0.001511 | 29.752941 | 1.641374 |
| 3000x3000 | Numba GPU | 0.005475 | 40.263538 | 1.377104 |
| 6000x6000 | Numba GPU | 0.021405 | 41.231207 | 1.330235 |

PyTorch CPU queda por detrás del mejor método en todos los tamaños. PyTorch GPU se acerca más,
especialmente en imágenes grandes, pero sigue siendo más lento que Numba GPU en estas mediciones
de cómputo puro.

También se observa que PyTorch CPU queda por detrás de Numba paralelo CPU. Esto es esperable
porque Numba CPU compila bucles ajustados al problema y reparte el trabajo con `prange`, mientras
que PyTorch CPU usa operaciones generales sobre tensores y una convolución pensada como primitiva
de alto nivel. Para este filtro pequeño y una sola imagen, el overhead de PyTorch CPU puede pesar
más que la ventaja de expresar el cálculo con tensores.

Este resultado es razonable para este caso puntual. Numba GPU usa kernels CUDA específicos para
Sobel: un kernel convierte RGB->gris y otro aplica el filtro con una estrategia de un hilo por píxel.
PyTorch GPU, en cambio, expresa Sobel con operaciones generales sobre tensores, especialmente
`conv2d`. Esa primitiva está optimizada para muchos escenarios, pero también incluye overhead de
framework, preparación de tensores, formato `N, C, H, W` y dos convoluciones separadas para `Gx`
y `Gy`. Para una única imagen y un filtro pequeño `3x3`, ese costo adicional puede hacer que una
implementación CUDA específica con Numba sea más rápida.

### 1. Diferencias de rendimiento entre PyTorch CPU y PyTorch GPU

PyTorch GPU es más rápido que PyTorch CPU para todos los tamaños. La mejora aumenta con la
resolución porque la GPU aprovecha mejor el paralelismo de datos cuando hay más píxeles para
procesar. Además, el uso de `conv2d` permite delegar el cálculo a primitivas optimizadas de PyTorch.

### 2. Comparación frente a las mejores implementaciones anteriores

Frente a Numba GPU, PyTorch GPU es más lento en los cuatro tamaños, aunque la diferencia disminuye
al crecer la imagen: PyTorch GPU tarda 2.719244 veces el tiempo de Numba GPU en `750x750`, y
1.330235 veces en `6000x6000`. PyTorch CPU queda más lejos porque, aunque trabaja sobre tensores,
no aprovecha el acelerador CUDA.

La comparación con Numba CPU muestra una idea similar en CPU: PyTorch CPU no supera a Numba
paralelo CPU en estas mediciones porque Numba compila una implementación más específica del
algoritmo, mientras que PyTorch CPU opera mediante primitivas generales de tensores.

Esto no indica un error en PyTorch GPU. La comparación muestra dos niveles de abstracción distintos:
Numba CUDA permite escribir kernels ajustados al problema, mientras que PyTorch delega el cálculo
a operaciones generales de alto nivel. En problemas más grandes, con batches o con más operaciones
encadenadas dentro de GPU, PyTorch puede amortizar mejor ese overhead.

## Conclusiones

La implementación secuencial funciona como línea base y muestra el costo de resolver Sobel con
bucles Python puros. Sus tiempos crecen junto con la cantidad de píxeles de la imagen.

NumPy ofrece una aceleración importante sin administrar workers manualmente. Su ventaja proviene
de la vectorización sobre arreglos completos y de evitar bucles Python explícitos.

Numba paralelo CPU logra el mejor rendimiento de la primera entrega. Al compilar los bucles y
repartir trabajo entre 6 workers, reduce de forma muy significativa el tiempo total frente a las
otras implementaciones de CPU.

Numba GPU se integra al análisis global comparándolo contra la misma referencia secuencial que los
demás métodos. Con ese criterio, obtiene speed-ups entre 849.191126 y 1058.816812 según el
tamaño de imagen.

En el análisis específico de la entrega 2, Numba GPU mejora el cómputo puro frente a Numba CPU,
pero no supera a Numba CPU cuando se suman las transferencias CPU<->GPU. Esto confirma lo señalado
en la teoría de la materia: usar GPU no garantiza automáticamente menor tiempo total. La aceleración
depende de que el problema tenga suficiente trabajo paralelo y de que el costo de mover datos no
domine la ejecución.

PyTorch CPU y PyTorch GPU muestran otra forma de expresar el mismo problema: tensores y
operaciones de alto nivel. PyTorch GPU mejora claramente a PyTorch CPU, incluso incluyendo
transferencias, pero en estas mediciones no supera a Numba GPU. Esto permite diferenciar dos
niveles de abstracción: Numba CUDA se acerca más al control explícito del kernel, mientras que
PyTorch delega el cálculo a primitivas optimizadas sobre tensores.

Que PyTorch GPU sea más lento que Numba GPU en este caso no contradice la aceleración por GPU:
PyTorch GPU sí mejora a PyTorch CPU. La diferencia frente a Numba GPU se explica por el overhead
de usar primitivas generales como `conv2d` para una sola imagen y un filtro Sobel pequeño, mientras
que Numba ejecuta kernels específicos para esta tarea.

De manera análoga, PyTorch CPU no supera a Numba paralelo CPU porque Numba CPU combina
compilación JIT, bucles específicos y paralelismo explícito para este algoritmo. PyTorch CPU mantiene
una interfaz de alto nivel sobre tensores, útil como puente conceptual hacia GPU, pero no necesariamente
como la opción CPU más rápida para este caso.

En conjunto, los resultados permiten observar una progresión clara: Python secuencial sirve como
referencia, NumPy mejora al vectorizar, Numba CPU acelera al compilar y paralelizar sobre CPU,
Numba GPU muestra el potencial del paralelismo masivo controlado con CUDA, y PyTorch muestra
una alternativa de alto nivel para trabajar sobre tensores en CPU y GPU.
