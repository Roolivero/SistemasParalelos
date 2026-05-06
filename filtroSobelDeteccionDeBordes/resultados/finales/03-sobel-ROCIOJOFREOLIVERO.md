# Titulo

Informe de rendimiento: filtro de Sobel para deteccion de bordes en Python

## Abstract

En este trabajo se implementa y compara el filtro de Sobel para deteccion de bordes sobre imagenes
RGB sinteticas de distintas resoluciones. Para la primera entrega se evaluan tres implementaciones:
secuencial pura, vectorizada con NumPy y paralela en CPU con Numba. Los experimentos se ejecutan
con imagenes de `750x750`, `1500x1500`, `3000x3000` y `6000x6000`, realizando 5 corridas por
metodo y tamano. Se registran por separado el tiempo de conversion RGB->gris, el tiempo de Sobel,
el tiempo total, el porcentaje de pixeles blancos, el speed-up y la performance. Los resultados
muestran que NumPy acelera fuertemente respecto de la version secuencial, mientras que Numba
paralelo CPU logra el mejor rendimiento en imagenes medianas y grandes. Las salidas obtenidas
son equivalentes entre metodos segun porcentaje de pixeles blancos, checksum y hash.

## Introduccion

El procesamiento de imagenes es una carga de trabajo adecuada para estudiar tecnicas de
optimizacion y paralelizacion, ya que aplica operaciones repetitivas sobre grandes cantidades de
pixeles. En este trabajo se utiliza el operador de Sobel, un filtro clasico para detectar bordes o
contornos en una imagen.

Sobel estima cambios de intensidad en dos direcciones mediante dos mascaras de convolucion:

```text
Gx = [-1  0  1]      Gy = [ 1  2  1]
     [-2  0  2]           [ 0  0  0]
     [-1  0  1]           [-1 -2 -1]
```

Para cada pixel interior se toma su vecindad `3x3`, se calculan `gx` y `gy`, y luego se obtiene la
magnitud del gradiente:

```text
|grad| = sqrt(gx^2 + gy^2)
```

El resultado se recorta al rango `[0, 255]`. Los valores cercanos a 0 representan zonas sin borde
fuerte, mientras que el valor 255 representa bordes fuertes. Como Sobel trabaja sobre una sola
intensidad por pixel, antes se convierte la imagen RGB a escala de grises mediante luminancia:

```text
I = 0.299R + 0.587G + 0.114B
```

Desde el punto de vista del paralelismo, Sobel permite comparar enfoques distintos sobre un mismo
calculo: bucles secuenciales, vectorizacion sobre arreglos completos y paralelismo explicito en CPU.

## Metodologias

Se trabajaron experimentos de benchmarking sobre una imagen RGB sintetica y reproducible, usando
la misma semilla (`--seed 2026`) para todos los metodos. La generacion de la imagen no se incluye
en los tiempos medidos, ya que la consigna solicita medir solamente computo.

### Entorno y hardware

- CPU: AMD Ryzen 5 5600X 6-Core Processor
  - 6 nucleos fisicos, 12 hilos logicos
- RAM: 15.52 GiB totales, aproximadamente 8.2-8.6 GiB disponibles durante las corridas
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Version de Python: 3.14.4 free-threading build, conda-forge
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU: no se utiliza en esta entrega

Configuraciones consideradas:

- Tamanos de imagen: `750x750`, `1500x1500`, `3000x3000` y `6000x6000`.
- Cantidad de corridas por combinacion: 5.
- Semilla de reproducibilidad: `2026`.
- Metodos comparados:
  - secuencial puro,
  - NumPy,
  - Numba paralelo CPU.
- Workers en Numba CPU: 8 hilos.

Metricas registradas:

- tiempo de conversion RGB->gris;
- tiempo de aplicacion del filtro Sobel;
- tiempo total;
- porcentaje de pixeles blancos (`valor 255`) en la imagen Sobel;
- speed-up respecto de la version secuencial;
- performance (%);
- checksum y hash de salida como control de equivalencia.

El speed-up se calcula con:

```text
speed-up = tiempo total secuencial / tiempo total del metodo
```

La performance se calcula como:

```text
performance (%) = speed-up / unidades usadas * 100
```

Para Numba CPU se usan los 8 hilos configurados como unidades. Para secuencial y NumPy se usa 1
unidad explicita, ya que el benchmark no administra manualmente workers en esas versiones.

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

## Experimentos

En esta seccion se presentan los resultados crudos de las corridas disponibles. Cada tabla
corresponde a un tamano de imagen, como solicita la consigna.

### Experimento 1: imagen 750x750

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.083825 | 0.258512 | 0.342338 | 0.323556 | 1.000000 | 100.000000 |
| NumPy | 0.001955 | 0.002600 | 0.004555 | 0.323556 | 75.158994 | 7515.899374 |
| Numba paralelo CPU | 0.048503 | 0.000313 | 0.048816 | 0.323556 | 7.012784 | 87.659800 |

### Experimento 2: imagen 1500x1500

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.334964 | 1.034740 | 1.369705 | 0.161956 | 1.000000 | 100.000000 |
| NumPy | 0.008867 | 0.012354 | 0.021221 | 0.161956 | 64.543893 | 6454.389334 |
| Numba paralelo CPU | 0.001393 | 0.001238 | 0.002632 | 0.161956 | 520.445518 | 6505.568979 |

### Experimento 3: imagen 3000x3000

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 1.306512 | 4.184142 | 5.490655 | 0.080933 | 1.000000 | 100.000000 |
| NumPy | 0.035172 | 0.074253 | 0.109426 | 0.080933 | 50.177077 | 5017.707664 |
| Numba paralelo CPU | 0.004670 | 0.004492 | 0.009161 | 0.080933 | 599.329247 | 7491.615591 |

### Experimento 4: imagen 6000x6000

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 5.280667 | 17.075369 | 22.356036 | 0.040467 | 1.000000 | 100.000000 |
| NumPy | 0.147766 | 0.293736 | 0.441502 | 0.040467 | 50.636269 | 5063.626945 |
| Numba paralelo CPU | 0.014490 | 0.015880 | 0.030370 | 0.040467 | 736.119688 | 9201.496104 |

## Resultados

La version secuencial es la mas lenta en todos los tamanos, lo cual resulta esperable porque recorre
los pixeles con bucles Python puros. En `6000x6000`, por ejemplo, tarda 22.356036 s, de los cuales
17.075369 s corresponden a Sobel.

NumPy reduce los tiempos de forma marcada al expresar el calculo mediante operaciones
vectorizadas. En `750x750` el tiempo total baja de 0.342338 s a 0.004555 s, y en `6000x6000` baja
de 22.356036 s a 0.441502 s.

Numba paralelo CPU obtiene el mejor rendimiento en `1500x1500`, `3000x3000` y `6000x6000`. En
el tamano mayor alcanza 0.030370 s de tiempo total, con un speed-up de 736.119688 respecto de la
version secuencial.

La correctitud de las salidas se valida mediante pixeles blancos, checksum y hash. Para cada tamano,
los tres metodos producen los mismos valores:

| Tamano | Pixeles blancos | Pixeles totales | Pixeles blancos [%] | Checksum Sobel | Hash salida |
|---:|---:|---:|---:|---:|---|
| 750x750 | 1820 | 562500 | 0.323556 | 1552402 | 9afeaa122377f409 |
| 1500x1500 | 3644 | 2250000 | 0.161956 | 3113394 | 34f7880907cc0e27 |
| 3000x3000 | 7284 | 9000000 | 0.080933 | 6233330 | eb3441cc7677b249 |
| 6000x6000 | 14568 | 36000000 | 0.040467 | 12474230 | f1b0875ac49b9f7d |

Tambien se observo que el porcentaje de pixeles blancos disminuye al aumentar la resolucion. Esto
no implica peor deteccion, porque el total de pixeles crece como area, mientras que los contornos
crecen principalmente como lineas. Para comparar de forma mas equitativa se normalizo la cantidad
de pixeles blancos por el crecimiento del lado de la imagen respecto de `750x750`:

| Tamano | Factor de lado vs 750 | Pixeles blancos | Blancos normalizados | Indice vs 750 [%] |
|---:|---:|---:|---:|---:|
| 750x750 | 1.00 | 1820 | 1820.00 | 100.00 |
| 1500x1500 | 2.00 | 3644 | 1822.00 | 100.11 |
| 3000x3000 | 4.00 | 7284 | 1821.00 | 100.05 |
| 6000x6000 | 8.00 | 14568 | 1821.00 | 100.05 |

Estos valores muestran que la deteccion de contornos se mantiene estable al escalar la imagen.

## Analisis

### Diferencias de tiempo entre metodos

La diferencia principal se observa entre la version secuencial y las versiones optimizadas. La
secuencial queda limitada por el costo de ejecutar bucles Python sobre cada pixel. NumPy evita esa
sobrecarga al trabajar con arreglos completos, mientras que Numba compila las funciones y reparte
el trabajo con `prange`.

En imagenes chicas, NumPy puede ser mas conveniente que Numba CPU por tener menos costo fijo. En
`750x750`, NumPy tarda 0.004555 s y Numba CPU 0.048816 s. Sin embargo, en imagenes medianas y
grandes Numba CPU pasa a ser el metodo mas rapido: en `6000x6000`, NumPy tarda 0.441502 s y
Numba CPU 0.030370 s.

### Evolucion del speed-up

El speed-up de NumPy se mantiene alto en todos los tamanos, aunque disminuye desde 75.158994 en
`750x750` hasta 50.636269 en `6000x6000`. Esto indica que la vectorizacion mejora mucho respecto
del secuencial, pero su aceleracion relativa no crece con la resolucion.

El speed-up de Numba CPU aumenta con el tamano de imagen: 7.012784 en `750x750`, 520.445518 en
`1500x1500`, 599.329247 en `3000x3000` y 736.119688 en `6000x6000`. Esto muestra que el costo
fijo de la ejecucion paralela pesa mas en tamanos chicos, pero se amortiza cuando aumenta la
cantidad de pixeles.

Las performances mayores al 100 % no representan una eficiencia paralela ideal pura. En este caso
el baseline es una version Python secuencial pura, mientras que NumPy y Numba tambien cambian el
modo de ejecucion: vectorizacion, codigo compilado y mejor aprovechamiento de memoria.

### Equivalencia de resultados

Las salidas son equivalentes entre metodos. Para cada tamano se obtiene el mismo porcentaje de
pixeles blancos, el mismo checksum y el mismo hash. Por lo tanto, las diferencias de tiempo no se
deben a cambios en el resultado del algoritmo, sino al enfoque de implementacion.

La disminucion del porcentaje de blancos al aumentar la resolucion no indica perdida de calidad.
Al normalizar por el crecimiento del lado de la imagen, la cantidad de blancos queda alrededor de
1820-1822 en todos los tamanos. Esto confirma que la proporcion de contornos detectados se
mantiene estable.

### Observacion sobre Numba en 750x750

En `750x750`, la primera corrida de Numba CPU tuvo un tiempo de conversion RGB->gris mucho mas
alto que las corridas siguientes. Aunque los kernels se calientan antes de medir, puede quedar un
costo inicial asociado al arranque de ejecucion paralela, cache o preparacion interna. Como la
consigna pide promediar las corridas realizadas, ese valor se mantuvo en el promedio. En tamanos
mayores el efecto queda amortizado y Numba pasa a ser el metodo mas rapido.

## Conclusiones

La implementacion secuencial funciona como linea base y muestra el costo de resolver Sobel con
bucles Python puros. Sus tiempos crecen de manera coherente con el area de la imagen: al duplicar
el lado, se cuadruplica la cantidad de pixeles a procesar.

NumPy ofrece una aceleracion importante sin administrar hilos manualmente. Su ventaja proviene de
la vectorizacion sobre arreglos completos y de evitar bucles Python explicitos.

Numba paralelo CPU logra el mejor rendimiento en imagenes medianas y grandes. Su ventaja se
vuelve mas clara a medida que crece la resolucion, porque el trabajo por pixel permite amortizar
mejor los costos fijos del paralelismo.

Finalmente, las tres implementaciones producen resultados equivalentes. Esto permite comparar los
tiempos de manera consistente: las diferencias observadas corresponden al enfoque de ejecucion y
optimizacion, no a cambios en la salida del algoritmo.

## Archivos de resultados usados

- `resultados/finales/resultado_final_secuencial.md`
- `resultados/finales/resultado_final_numpy.md`
- `resultados/finales/resultado_final_numba_cpu.md`
- `resultados/resultados_sobel_750x750.csv`
- `resultados/resultados_sobel_1500x1500.csv`
- `resultados/resultados_sobel_3000x3000.csv`
- `resultados/resultados_sobel_6000x6000.csv`
