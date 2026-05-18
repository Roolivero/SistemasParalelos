# Titulo

Informe de rendimiento: filtro de Sobel para deteccion de bordes en Python

## Abstract

En este trabajo se implementa el filtro de Sobel para deteccion de bordes sobre imagenes RGB de
distintas resoluciones. Para esta entrega se presentan los resultados consolidados de la version
secuencial, usando imagenes de `750x750`, `1500x1500`, `3000x3000` y `6000x6000`. En cada caso se
realizan 5 corridas y se registran por separado el tiempo de conversion RGB a escala de grises, el
tiempo de aplicacion del filtro Sobel, el tiempo total, el porcentaje de pixeles blancos, checksum
y hash de salida.

Los resultados muestran que el costo computacional aumenta al crecer el tamaño de la imagen. Esto
es esperable porque el algoritmo debe recorrer los pixeles interiores y aplicar una operacion sobre
una vecindad `3x3` para cada uno de ellos. Las salidas generadas se guardan como imagenes `.png`
para permitir la inspeccion visual del filtro aplicado.

## Introduccion

El procesamiento de imagenes es una carga de trabajo adecuada para estudiar rendimiento, porque
aplica operaciones repetitivas sobre grandes cantidades de pixeles. En este trabajo se utiliza el
operador de Sobel, un filtro clasico para detectar bordes o contornos en una imagen.

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
fuerte, mientras que valores mas altos representan cambios de intensidad mas marcados. Como Sobel
trabaja sobre una sola intensidad por pixel, antes se convierte la imagen RGB a escala de grises
mediante luminancia:

```text
I = 0.299R + 0.587G + 0.114B
```

## Metodologias

Se ejecutaron experimentos de benchmarking sobre las imagenes provistas para el trabajo. La carga
de la imagen se realiza fuera del tiempo medido, para registrar solamente el costo de computo de la
conversion a gris y la aplicacion del filtro Sobel.

### Entorno y hardware

- CPU: AMD Ryzen 5 5600X 6-Core Processor
  - 6 nucleos fisicos, 12 hilos logicos
- RAM: 15.52 GiB totales, aproximadamente 8.38 GiB disponibles durante las corridas
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Version de Python: 3.14.4 free-threading build, conda-forge
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU: no se utiliza en esta entrega

Configuraciones consideradas:

- Imagenes de entrada:
  - `IMG_0358_750x750.jpg`
  - `IMG_0358_1500x1500.jpg`
  - `IMG_0358_3000x3000.jpg`
  - `IMG_0358_6000x6000.jpg`
- Tamaños de imagen: `750x750`, `1500x1500`, `3000x3000` y `6000x6000`.
- Cantidad de corridas por tamaño: 5.
- Metodo medido: secuencial puro.
- Salidas generadas: imagenes Sobel en formato `.png`.

Metricas registradas:

- tiempo de conversion RGB a escala de grises;
- tiempo de aplicacion del filtro Sobel;
- tiempo total;
- porcentaje de pixeles blancos (`valor 255`) en la imagen Sobel;
- checksum y hash de salida como control de reproducibilidad.

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

## Experimentos

En esta seccion se presentan los resultados crudos de las corridas disponibles. Cada tabla
corresponde a un tamaño de imagen.

### Experimento 1: imagen 750x750

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.087378 | 0.286957 | 0.374334 | 0.281778 | 1.000000 | 100.000000 |

### Experimento 2: imagen 1500x1500

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 0.329165 | 1.145662 | 1.474827 | 0.059956 | 1.000000 | 100.000000 |

### Experimento 3: imagen 3000x3000

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 1.315055 | 4.403400 | 5.718456 | 0.001367 | 1.000000 | 100.000000 |

### Experimento 4: imagen 6000x6000

| Metodo | RGB->gris [s] | Sobel [s] | Total [s] | Pixeles blancos [%] | Speed-up | Performance [%] |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 5.243595 | 17.420171 | 22.663766 | 0.000000 | 1.000000 | 100.000000 |

## Resultados

La version secuencial funciona como linea base del trabajo. En este enfoque, tanto la conversion
RGB a escala de grises como la aplicacion de Sobel se resuelven con bucles Python puros, recorriendo
los pixeles de la imagen.

El tiempo total aumenta junto con el tamaño de la imagen:

| Tamano | Tiempo RGB->gris [s] | Tiempo Sobel [s] | Tiempo total [s] |
|---:|---:|---:|---:|
| 750x750 | 0.087378 | 0.286957 | 0.374334 |
| 1500x1500 | 0.329165 | 1.145662 | 1.474827 |
| 3000x3000 | 1.315055 | 4.403400 | 5.718456 |
| 6000x6000 | 5.243595 | 17.420171 | 22.663766 |

El filtro Sobel es la parte mas costosa del procesamiento. Esto se debe a que para cada pixel
interior se revisa una vecindad de 9 posiciones y se calculan dos gradientes, uno horizontal y otro
vertical.

Los datos de control obtenidos fueron:

| Tamano | Pixeles blancos | Pixeles totales | Pixeles blancos [%] | Checksum Sobel | Hash salida |
|---:|---:|---:|---:|---:|---|
| 750x750 | 1585 | 562500 | 0.281778 | 7145137 | e330e8a405b66425 |
| 1500x1500 | 1349 | 2250000 | 0.059956 | 18014291 | 49a177a791d110fb |
| 3000x3000 | 123 | 9000000 | 0.001367 | 47883925 | a5989d2f439a9154 |
| 6000x6000 | 0 | 36000000 | 0.000000 | 109936717 | d8af6b4c711617e3 |

La columna de pixeles blancos cuenta solamente los pixeles cuyo valor final es exactamente `255`.
Por eso, en la imagen de `6000x6000` el valor es 0: la salida Sobel contiene bordes en tonos de
gris, pero ningun pixel llega al blanco puro. Esto no significa que la salida este vacia; el checksum
distinto de cero confirma que existen valores de intensidad en la imagen resultante.

## Analisis

### Crecimiento del tiempo

Al duplicar el lado de la imagen, la cantidad total de pixeles se multiplica por cuatro. Por eso el
tiempo crece de forma cercana al crecimiento del area. La imagen `6000x6000` tiene 64 veces mas
pixeles que la imagen `750x750`, y el tiempo total pasa de 0.374334 s a 22.663766 s.

La relacion entre tamaño y costo se observa con claridad en la etapa Sobel:

| Tamano | Pixeles totales | Tiempo Sobel [s] |
|---:|---:|---:|
| 750x750 | 562500 | 0.286957 |
| 1500x1500 | 2250000 | 1.145662 |
| 3000x3000 | 9000000 | 4.403400 |
| 6000x6000 | 36000000 | 17.420171 |

### Conversion RGB a gris

La conversion RGB a escala de grises tambien crece con el tamaño de la imagen. Esta etapa toma los
canales rojo, verde y azul de cada pixel y calcula una sola intensidad usando la formula de
luminancia. Aunque es menos costosa que Sobel, tambien debe recorrer todos los pixeles.

### Pixeles blancos y deteccion de bordes

El porcentaje de pixeles blancos no mide todos los bordes detectados, sino solo los puntos donde la
magnitud del gradiente alcanza el valor maximo `255`. Una imagen puede tener bordes visibles en la
salida Sobel aunque el conteo de blancos puros sea bajo o incluso cero.

Por este motivo, el porcentaje de blancos se usa como dato de control, pero no como unica medida de
calidad visual. Los archivos `.png` generados permiten verificar la salida del filtro de manera
directa.

## Conclusiones

La implementacion secuencial permite establecer una linea base clara para el filtro de Sobel. El
tiempo de ejecucion aumenta al crecer la cantidad de pixeles, lo cual coincide con la naturaleza del
algoritmo: se realiza trabajo por cada pixel interior de la imagen.

La etapa Sobel representa la mayor parte del tiempo total, porque requiere aplicar las mascaras `Gx`
y `Gy` sobre una vecindad `3x3`. La conversion RGB a gris tambien escala con el tamaño, pero tiene
menor costo relativo.

Los resultados muestran que el algoritmo produce salidas reproducibles para cada tamaño. Los
checksums y hashes se registran como control para poder comparar futuras implementaciones, como
versiones vectorizadas con NumPy o paralelas con Numba, contra la misma salida de referencia.

## Archivos de resultados usados

- `resultados/entrega1/finales/resultado_final_secuencial.md`
- `resultados/entrega1/resultados_sobel_750x750.csv`
- `resultados/entrega1/resultados_sobel_1500x1500.csv`
- `resultados/entrega1/resultados_sobel_3000x3000.csv`
- `resultados/entrega1/resultados_sobel_6000x6000.csv`
- `resultados/entrega1/imagenes_sobel/sobel_750x750_secuencial.png`
- `resultados/entrega1/imagenes_sobel/sobel_1500x1500_secuencial.png`
- `resultados/entrega1/imagenes_sobel/sobel_3000x3000_secuencial.png`
- `resultados/entrega1/imagenes_sobel/sobel_6000x6000_secuencial.png`
