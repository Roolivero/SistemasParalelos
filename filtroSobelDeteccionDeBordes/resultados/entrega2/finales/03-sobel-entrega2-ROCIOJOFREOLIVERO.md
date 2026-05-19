# Título

Informe de rendimiento: filtro de Sobel con Numba GPU

## Abstract

En esta segunda entrega se incorpora una implementación del filtro de Sobel usando Numba GPU
con CUDA. El objetivo es comparar su rendimiento contra la versión Numba paralelo CPU, utilizando
las mismas imágenes de entrada de `750x750`, `1500x1500`, `3000x3000` y `6000x6000`.

Para cada tamaño se realizaron 5 corridas. Se midieron por separado el tiempo de conversión
RGB a escala de grises, el tiempo de aplicación de Sobel y el tiempo total de cómputo. Además,
para la versión GPU se registraron aparte las transferencias CPU→GPU y GPU→CPU, porque la
consigna pide analizar en qué casos ese costo se amortiza.

Los resultados muestran que Numba GPU mejora el tiempo de cómputo puro respecto de Numba
CPU en todos los tamaños medidos. Sin embargo, si se suman las transferencias entre CPU y GPU,
la versión GPU no llega a superar a Numba CPU en estas corridas.

## Introducción

El operador de Sobel detecta bordes calculando cambios de intensidad en una imagen. Primero se
convierte la imagen RGB a escala de grises mediante luminancia:

```text
I = 0.299R + 0.587G + 0.114B
```

Luego se aplican dos máscaras de convolución, `Gx` y `Gy`, para estimar cambios horizontales y
verticales:

```text
Gx = [-1  0  1]      Gy = [ 1  2  1]
     [-2  0  2]           [ 0  0  0]
     [-1  0  1]           [-1 -2 -1]
```

La magnitud del gradiente se calcula como:

```text
|grad| = sqrt(gx^2 + gy^2)
```

Desde el punto de vista del paralelismo, Sobel es adecuado para GPU porque tiene paralelismo de
datos: muchos píxeles pueden procesarse de forma independiente. Según el enfoque visto en el
libro de la materia, en CUDA el trabajo se organiza mediante `grid`, `blocks` y `threads`: cada
hilo ejecuta el mismo kernel sobre una parte del problema.

## Metodologías

Se implementó una versión `numba_gpu` basada en `numba.cuda`. La estructura sigue el código de
referencia compartido por el docente:

- un kernel CUDA para convertir RGB a gris;
- un kernel CUDA para aplicar Sobel;
- grilla bidimensional;
- bloques de `16x16` hilos;
- un hilo CUDA por píxel;
- sincronización explícita con `cuda.synchronize()` antes de cerrar cada medición.

La carga de imagen y el guardado de la salida quedan fuera de los tiempos medidos. Para GPU,
las transferencias CPU↔GPU se registran en una tabla separada.

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
- Métodos comparados:
  - Numba paralelo CPU;
  - Numba GPU.
- Numba CPU: 6 workers, coincidiendo con los 6 núcleos físicos del procesador.
- Numba GPU: bloques CUDA de `16x16`, es decir, 256 hilos por bloque.
- Corridas por combinación: 5.

En esta entrega, el speed-up se calcula tomando como referencia a Numba CPU para el mismo tamaño:

```text
speed-up GPU = tiempo total Numba CPU / tiempo total Numba GPU
```

La columna de performance se informa como rendimiento relativo porcentual contra Numba CPU:

```text
performance relativa (%) = speed-up * 100
```

No se divide por la cantidad de hilos CUDA porque los hilos de GPU no equivalen directamente a
workers de CPU.

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

## Experimentos

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

## Resultados

La versión GPU mejora el tiempo total de cómputo puro en todos los tamaños. La mayor mejora se
observa en `1500x1500`, donde el speed-up llega a `1.983475`. En `6000x6000` también hay mejora,
pero es menor: `1.280216`.

La conversión RGB→gris es claramente más rápida en GPU para todos los tamaños. En cambio, la
etapa Sobel no siempre mejora frente a Numba CPU: en `750x750`, `3000x3000` y `6000x6000`, el
tiempo de Sobel GPU queda cerca o por encima del tiempo CPU. Aun así, el total de cómputo GPU
resulta menor porque la conversión a gris se acelera bastante.

### Transferencias CPU↔GPU

| Tamaño | Transferencia CPU→GPU [s] | Transferencia GPU→CPU [s] | Transferencia total [s] | Cómputo GPU [s] | GPU con transferencias [s] | Speed-up incluyendo transferencias |
|---:|---:|---:|---:|---:|---:|---:|
| 750x750 | 0.000598 | 0.000213 | 0.000811 | 0.000441 | 0.001252 | 0.646284 |
| 1500x1500 | 0.001302 | 0.000682 | 0.001984 | 0.001511 | 0.003495 | 0.857667 |
| 3000x3000 | 0.003251 | 0.001517 | 0.004768 | 0.005475 | 0.010242 | 0.741860 |
| 6000x6000 | 0.011006 | 0.005107 | 0.016113 | 0.021405 | 0.037518 | 0.730399 |

Cuando se incluyen transferencias, la GPU no supera a Numba CPU en estas corridas. Esto muestra
un punto importante mencionado en la teoría: una GPU puede ejecutar kernels muy rápido, pero el
costo de mover datos entre host y dispositivo puede reducir o anular la mejora si el cálculo no
permanece suficiente tiempo en GPU.

## Análisis

### 1. Mejora de tiempo entre Numba GPU y Numba paralelo CPU

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

### 2. Amortización del costo de transferencia CPU↔GPU

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

### 3. Evolución del speed-up de Numba GPU

El speed-up de GPU no crece de forma monótona con la resolución. Sube de `750x750` a `1500x1500`,
pero luego baja en `3000x3000` y `6000x6000`.

Esto muestra un cambio de tendencia: la GPU obtiene ventaja en el cómputo, pero la etapa Sobel
no escala tan favorablemente como la conversión a gris. Además, al considerar transferencias, el
beneficio total queda limitado por el costo de mover datos entre CPU y GPU.

### Equivalencia de salidas

Los métodos producen el mismo porcentaje de píxeles blancos en todos los tamaños:

| Tamaño | Píxeles blancos CPU | Píxeles blancos GPU | Porcentaje |
|---:|---:|---:|---:|
| 750x750 | 1585 | 1585 | 0.281778 |
| 1500x1500 | 1349 | 1349 | 0.059956 |
| 3000x3000 | 123 | 123 | 0.001367 |
| 6000x6000 | 0 | 0 | 0.000000 |

Los checksums y hashes no son idénticos entre CPU y GPU, aunque los porcentajes de blancos sí
coinciden. Esto se atribuye a diferencias mínimas de aritmética y redondeo entre CPU y GPU. La
salida visual se mantiene equivalente para el objetivo del trabajo: detección de bordes.

## Conclusiones

Numba GPU logra mejorar el tiempo de cómputo puro frente a Numba paralelo CPU en todos los
tamaños evaluados. La ventaja es más clara en la conversión RGB→gris, donde cada píxel puede
procesarse de forma independiente con poco trabajo adicional.

El filtro Sobel también se paraleliza por píxel, pero al depender de una vecindad `3x3` tiene más
accesos a memoria. Por eso, en esta implementación, la mejora de GPU sobre CPU no crece de forma
lineal con el tamaño de la imagen.

Al incluir transferencias CPU↔GPU, la versión GPU no supera a Numba CPU en estas mediciones.
Esto confirma lo señalado en la teoría: usar GPU no garantiza automáticamente menor tiempo total.
La aceleración depende de que el problema tenga suficiente trabajo paralelo y de que el costo de
mover datos no domine la ejecución.

Para este caso, la GPU resulta útil para observar el modelo de paralelismo masivo con CUDA y
obtiene mejores tiempos de cómputo, pero el beneficio total queda condicionado por las
transferencias entre CPU y GPU.

## Archivos de resultados usados

- `resultados/entrega2/finales/resultado_final_numba_cpu.md`
- `resultados/entrega2/finales/resultado_final_numba_gpu.md`
- `resultados/entrega2/resultados_sobel_750x750.csv`
- `resultados/entrega2/resultados_sobel_1500x1500.csv`
- `resultados/entrega2/resultados_sobel_3000x3000.csv`
- `resultados/entrega2/resultados_sobel_6000x6000.csv`
- `resultados/entrega2/imagenes_sobel/sobel_750x750_numba_gpu.png`
- `resultados/entrega2/imagenes_sobel/sobel_1500x1500_numba_gpu.png`
- `resultados/entrega2/imagenes_sobel/sobel_3000x3000_numba_gpu.png`
- `resultados/entrega2/imagenes_sobel/sobel_6000x6000_numba_gpu.png`
