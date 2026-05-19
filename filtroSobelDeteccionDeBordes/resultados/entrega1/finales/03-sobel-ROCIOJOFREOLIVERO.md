# Título

Informe de rendimiento: filtro de Sobel para detección de bordes en Python

## Abstract

En este trabajo se implementa y compara el filtro de Sobel para detección de bordes sobre imágenes
RGB de distintas resoluciones. Para la primera entrega se evalúan tres implementaciones:
secuencial pura, vectorizada con NumPy y paralela en CPU con Numba. Los experimentos se ejecutan
con imágenes de `750x750`, `1500x1500`, `3000x3000` y `6000x6000`, realizando 5 corridas por
método y tamaño.

Se registran por separado el tiempo de conversión RGB a escala de grises, el tiempo de aplicación
de Sobel, el tiempo total, el porcentaje de píxeles blancos, el speed-up y la performance. Los
resultados muestran que NumPy mejora fuertemente respecto de la versión secuencial, mientras que
Numba paralelo CPU obtiene los mejores tiempos en todos los tamaños evaluados.

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

Desde el punto de vista del paralelismo, Sobel permite comparar enfoques distintos sobre un mismo
cálculo: bucles secuenciales, vectorización sobre arreglos completos y paralelismo explícito en CPU.

## Metodologías

Se ejecutaron experimentos de benchmarking sobre las imágenes provistas para el trabajo. La carga
de la imagen se realiza fuera del tiempo medido, para registrar solamente el costo de cómputo de la
conversión a gris y la aplicación del filtro Sobel.

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
- Tamaños de imagen: `750x750`, `1500x1500`, `3000x3000` y `6000x6000`.
- Cantidad de corridas por combinación: 5.
- Métodos comparados:
  - secuencial puro;
  - NumPy;
  - Numba paralelo CPU.
- Numba CPU: 6 workers, coincidiendo con los 6 núcleos físicos del procesador.
- Salidas generadas: imágenes Sobel en formato `.png`.

Métricas registradas:

- tiempo de conversión RGB a escala de grises;
- tiempo de aplicación del filtro Sobel;
- tiempo total;
- porcentaje de píxeles blancos (`valor 255`) en la imagen Sobel;
- speed-up respecto de la versión secuencial;
- performance;
- checksum y hash de salida como control.

El speed-up se calcula con:

```text
speed-up = tiempo total secuencial / tiempo total del método
```

La performance se calcula como:

```text
performance (%) = speed-up / unidades usadas * 100
```

Para Numba CPU se usan los 6 workers configurados como unidades. Para secuencial y NumPy se usa
1 unidad explícita, ya que el benchmark no administra manualmente workers en esas versiones.

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

## Experimentos

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

## Resultados

La versión secuencial es la más lenta en todos los tamaños, lo cual resulta esperable porque recorre
los píxeles con bucles Python puros. En `6000x6000`, por ejemplo, tarda 22.663766 s, de los cuales
17.420171 s corresponden a Sobel.

NumPy reduce los tiempos de forma marcada al expresar el cálculo mediante operaciones
vectorizadas. En `750x750`, el tiempo total baja de 0.374334 s a 0.004449 s. En `6000x6000`, baja
de 22.663766 s a 0.411459 s.

Numba paralelo CPU obtiene el mejor rendimiento global. En `6000x6000`, el tiempo total baja a
0.032503 s, con un speed-up de 697.283836 respecto de la versión secuencial.

### Datos de control

| Tamaño | Método | Píxeles blancos | Píxeles totales | Píxeles blancos [%] | Checksum Sobel | Hash salida |
|---:|---|---:|---:|---:|---:|---|
| 750x750 | Secuencial | 1585 | 562500 | 0.281778 | 7145137 | e330e8a405b66425 |
| 750x750 | NumPy | 1585 | 562500 | 0.281778 | 7144991 | d154fb8c8a528b71 |
| 750x750 | Numba CPU | 1585 | 562500 | 0.281778 | 7145137 | e330e8a405b66425 |
| 1500x1500 | Secuencial | 1349 | 2250000 | 0.059956 | 18014291 | 49a177a791d110fb |
| 1500x1500 | NumPy | 1349 | 2250000 | 0.059956 | 18013999 | f905721d22fdb912 |
| 1500x1500 | Numba CPU | 1349 | 2250000 | 0.059956 | 18014291 | 49a177a791d110fb |
| 3000x3000 | Secuencial | 123 | 9000000 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 3000x3000 | NumPy | 123 | 9000000 | 0.001367 | 47883024 | a92d650778fbd8bf |
| 3000x3000 | Numba CPU | 123 | 9000000 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 6000x6000 | Secuencial | 0 | 36000000 | 0.000000 | 109936717 | d8af6b4c711617e3 |
| 6000x6000 | NumPy | 0 | 36000000 | 0.000000 | 109935099 | 58d0001f7448e5ed |
| 6000x6000 | Numba CPU | 0 | 36000000 | 0.000000 | 109936717 | d8af6b4c711617e3 |

Los tres métodos producen el mismo porcentaje de píxeles blancos para cada tamaño. Los checksums
de NumPy presentan pequeñas diferencias respecto de secuencial y Numba CPU, atribuibles a
diferencias de redondeo en el cálculo vectorizado. Para la métrica solicitada por la consigna, las
salidas son equivalentes.

## Análisis

### 1. Diferencias de tiempo entre secuencial, NumPy y Numba CPU

La diferencia de tiempo es muy marcada. La versión secuencial queda limitada por el costo de los
bucles Python. NumPy mejora al usar operaciones vectorizadas sobre arreglos completos, mientras
que Numba CPU compila los bucles y reparte trabajo mediante paralelismo en CPU.

En todos los tamaños, Numba CPU fue el método más rápido. La ventaja se vuelve especialmente
clara en imágenes grandes: para `6000x6000`, secuencial tarda 22.663766 s, NumPy tarda 0.411459 s
y Numba CPU tarda 0.032503 s.

### 2. Evolución del speed-up

| Tamaño | Speed-up NumPy | Speed-up Numba CPU |
|---:|---:|---:|
| 750x750 | 84.132985 | 375.331744 |
| 1500x1500 | 81.817345 | 619.085631 |
| 3000x3000 | 53.540383 | 614.785758 |
| 6000x6000 | 55.081437 | 697.283836 |

El speed-up de NumPy es alto en todos los casos, pero no crece de manera sostenida con el tamaño.
Se mantiene entre aproximadamente 53x y 84x.

El speed-up de Numba CPU es mayor y tiende a ser más favorable en imágenes medianas y grandes.
Esto indica que el costo inicial de usar una versión compilada y paralela se amortiza mejor cuando
hay más píxeles para procesar.

Las performances mayores al 100% no representan eficiencia paralela ideal pura. En este caso, el
baseline es una versión Python secuencial pura, mientras que NumPy y Numba también cambian el
modo de ejecución mediante vectorización, compilación y mejor aprovechamiento del hardware.

### 3. Equivalencia de resultados

Los porcentajes de píxeles blancos coinciden entre los tres métodos en todos los tamaños:

| Tamaño | % blancos |
|---:|---:|
| 750x750 | 0.281778 |
| 1500x1500 | 0.059956 |
| 3000x3000 | 0.001367 |
| 6000x6000 | 0.000000 |

Esto permite comparar los tiempos de manera consistente. Las pequeñas diferencias de checksum en
NumPy no cambian la métrica principal de la consigna ni la salida visual esperada.

En `6000x6000`, el porcentaje de píxeles blancos es 0 porque ningún píxel llega exactamente al
valor 255. Esto no significa que no haya bordes: la imagen Sobel contiene valores de gris, pero no
bordes saturados al blanco puro.

## Conclusiones

La implementación secuencial funciona como línea base y muestra el costo de resolver Sobel con
bucles Python puros. Sus tiempos crecen junto con la cantidad de píxeles de la imagen.

NumPy ofrece una aceleración importante sin administrar workers manualmente. Su ventaja proviene
de la vectorización sobre arreglos completos y de evitar bucles Python explícitos.

Numba paralelo CPU logra el mejor rendimiento de la primera entrega. Al compilar los bucles y
repartir trabajo entre 6 workers, reduce de forma muy significativa el tiempo total frente a las otras
dos implementaciones.

Finalmente, los tres métodos producen resultados equivalentes según el porcentaje de píxeles
blancos solicitado por la consigna. Esto permite atribuir las diferencias observadas al enfoque de
ejecución y optimización, no a un cambio en el objetivo del algoritmo.

## Archivos de resultados usados

- `resultados/entrega1/finales/resultado_final_secuencial.md`
- `resultados/entrega1/finales/resultado_final_numpy.md`
- `resultados/entrega1/finales/resultado_final_numba_cpu.md`
- `resultados/entrega1/resultados_sobel_750x750.csv`
- `resultados/entrega1/resultados_sobel_1500x1500.csv`
- `resultados/entrega1/resultados_sobel_3000x3000.csv`
- `resultados/entrega1/resultados_sobel_6000x6000.csv`
