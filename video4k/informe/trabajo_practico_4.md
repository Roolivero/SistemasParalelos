# Informe de rendimiento: procesamiento de video 4K con PyTorch

## Abstract

En este trabajo se procesa un video 4K vertical de aproximadamente 31.5 segundos mediante un
filtro posterize pop-art. El objetivo es comparar una linea base secuencial en Python con dos
implementaciones basadas en PyTorch: una sobre CPU y otra sobre GPU CUDA.

El video utilizado tiene resolucion `2160x3840`, 944 frames y una tasa de reproduccion de
29.970 FPS. El procesamiento se realiza frame por frame para evitar cargar el video completo en
memoria. Para cada metodo se registran tiempos de lectura/decodificacion, filtrado, escritura/
codificacion, tiempo total del pipeline, FPS efectivos, memoria aproximada y speed-up respecto de
la version secuencial.

Los resultados muestran que PyTorch acelera de forma clara el procesamiento. La version
secuencial alcanza 0.594 FPS efectivos, PyTorch CPU alcanza 6.734 FPS efectivos y PyTorch GPU
alcanza 9.519 FPS efectivos. PyTorch GPU obtiene el mejor tiempo total, con un speed-up de 16.021
respecto de la version secuencial. Aun asi, el pipeline no llega a tiempo real porque el video
original se reproduce a 29.970 FPS y el procesamiento GPU queda limitado por transferencias
CPU-GPU y por la escritura del video final.

## Introduccion

El procesamiento de video puede verse como una extension natural del procesamiento de imagenes:
cada frame se trata como una imagen estatica, se aplica una transformacion y luego se reconstruye
la secuencia de salida. En videos 4K, el volumen de datos vuelve importante la forma de medir y de
administrar memoria.

En este trabajo se utiliza un filtro **posterize pop-art**. Este filtro reduce la cantidad de colores
posibles y reemplaza cada pixel por un color de una paleta fija segun su luminancia. La eleccion
permite obtener una salida visual clara, mantener una implementacion equivalente entre metodos y
concentrar el analisis en el costo de procesar video 4K con CPU y GPU.

La comparacion principal incluye tres implementaciones:

- una version secuencial pura en Python, usada como linea base;
- una version PyTorch sobre CPU;
- una version PyTorch sobre GPU CUDA.

## Metodologia

El video se proceso completo en cada corrida. Se hicieron 3 corridas por metodo y los valores
informados corresponden al promedio.

La lectura y escritura del video se realizaron con OpenCV (`VideoCapture` y `VideoWriter`). El codec
utilizado para reconstruir los videos procesados fue `mp4v`.

Link al repositorio:

```bash
https://github.com/Roolivero/SistemasParalelos
```

### Entorno y hardware

Los benchmarks se ejecutaron en el siguiente entorno:

| componente | valor |
|---|---|
| CPU | AMD Ryzen 5 5600X 6-Core Processor |
| nucleos fisicos | 6 |
| nucleos logicos | 12 |
| RAM | 15.52 GiB |
| sistema operativo | Linux 6.18.33-1-MANJARO x86_64 |
| Python | 3.12.13, conda-forge |
| NumPy | 2.4.6 |
| OpenCV | 4.13.0 |
| PyTorch | 2.11.0+cu128 |
| GPU | NVIDIA GeForce RTX 2060 |
| PyTorch CUDA | CUDA 12.8 |

Se uso un entorno Conda con CPython estandar, compatible con PyTorch, OpenCV y CUDA.

### Video de entrada

El video de entrada utilizado fue:

```text
video4k/15785079_2160_3840_30fps.mp4
```

Caracteristicas del video:

| dato | valor |
|---|---:|
| resolucion | 2160x3840 |
| orientacion | vertical |
| duracion | 31.498 s |
| FPS original | 29.970 |
| frames procesados | 944 |

La resolucion `2160x3840` corresponde a video 4K en orientacion vertical. En formato horizontal
equivaldria a `3840x2160`.

### Filtro posterize

El filtro clasifica cada pixel por luminancia y lo reemplaza por uno de cuatro colores. La paleta
utilizada fue:

| rango de luminancia | color | RGB |
|---|---|---|
| 0-63 | verde | `(27, 127, 58)` |
| 64-127 | fucsia | `(232, 62, 140)` |
| 128-191 | amarillo | `(255, 216, 77)` |
| 192-255 | blanco | `(255, 255, 255)` |

La luminancia se calcula con el criterio usual:

```text
luminancia = 0.299R + 0.587G + 0.114B
```

En el codigo se usa la forma entera equivalente:

```text
luminancia = (299R + 587G + 114B) // 1000
```

Esta forma reduce diferencias por redondeo entre implementaciones. El mismo pixel cae en el mismo
rango de luminancia tanto en la version secuencial como en PyTorch.

### Implementaciones evaluadas

La version secuencial recorre cada frame pixel por pixel con bucles Python. Para cada pixel calcula
la luminancia, elige el rango correspondiente y escribe el color de salida. La parte medida del filtro
no utiliza PyTorch ni vectorizacion NumPy. OpenCV se usa solamente para entrada y salida de video.

La version PyTorch CPU convierte cada frame a tensor y aplica la misma clasificacion de luminancia
con operaciones tensoriales sobre CPU. Se configuraron 6 workers, coincidiendo con la cantidad de
nucleos fisicos del procesador.

La version PyTorch GPU transfiere cada frame actual a CUDA, aplica el filtro con tensores en GPU,
sincroniza con `torch.cuda.synchronize()` antes de cerrar los tiempos y devuelve el frame resultante
a CPU para escribirlo en el video de salida.

### Criterio de comparacion

En la tabla principal se usa la version secuencial como referencia:

```text
speed-up = tiempo total secuencial / tiempo total del metodo
```

Tambien se informa el rendimiento en FPS efectivos:

```text
FPS efectivos = cantidad de frames procesados / tiempo total del pipeline
```

La columna **FPS original** representa la velocidad de reproduccion del video de entrada. La columna
**FPS efectivos** representa la velocidad a la que cada metodo pudo procesar los frames. Si los FPS
efectivos son menores que los FPS originales, el procesamiento no llega a tiempo real.

Para PyTorch GPU se registra ademas el detalle de transferencia CPU->GPU, computo en GPU y
transferencia GPU->CPU. El tiempo de filtrado GPU incluye esas tres partes, porque el frame se lee
desde CPU y debe volver a CPU para escribirse en el video.

### Manejo de memoria

El video no se carga completo en memoria. Se procesa como flujo:

```text
leer frame -> aplicar filtro -> escribir frame -> liberar referencias -> continuar
```

Un frame 4K `2160x3840` con tres canales `uint8` ocupa aproximadamente 25 MB sin compresion.
El video completo tiene 944 frames, por lo que almacenar todos los frames y sus tensores
intermedios requeriria decenas de GB. En GPU se mantiene el mismo criterio: solo se transfiere el
frame actual y no se conserva el video completo en memoria del dispositivo.

## Resultados

### Resultados globales

| metodo | frames | resolucion | FPS original | lectura/decodif. (s) | filtrado (s) | escritura/codif. (s) | total pipeline (s) | FPS efectivos | speed-up | memoria pico (MB) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| secuencial | 944 | 2160x3840 | 29.970 | 5.535 | 1526.404 | 56.961 | 1588.900 | 0.594 | 1.000 | 1321.81 |
| PyTorch CPU | 944 | 2160x3840 | 29.970 | 5.594 | 75.610 | 59.014 | 140.217 | 6.734 | 11.332 | 1518.56 |
| PyTorch GPU | 944 | 2160x3840 | 29.970 | 5.560 | 34.777 | 58.838 | 99.175 | 9.519 | 16.021 | 1592.24 |

### Detalle de PyTorch GPU

| etapa GPU | tiempo promedio (s) |
|---|---:|
| transferencia CPU -> GPU | 25.415 |
| computo GPU | 3.671 |
| transferencia GPU -> CPU | 5.691 |
| transferencia total | 31.106 |
| filtrado total GPU | 34.777 |

El computo del filtro en GPU tomo solo 3.671 s para todo el video. El tiempo total de filtrado GPU
sube a 34.777 s porque cada frame debe transferirse desde CPU a GPU y luego volver a CPU para ser
escrito por OpenCV.

### Equivalencia de salidas

Los tres metodos generaron el mismo checksum y el mismo hash de salida:

| metodo | checksum | hash |
|---|---:|---|
| secuencial | 3753312782835 | `e81551eaad55d3c5` |
| PyTorch CPU | 3753312782835 | `e81551eaad55d3c5` |
| PyTorch GPU | 3753312782835 | `e81551eaad55d3c5` |

Esto indica que las tres implementaciones aplicaron el mismo filtro y produjeron frames
equivalentes. La comparacion visual de los videos generados muestra el mismo efecto posterize con
la paleta verde, fucsia, amarillo y blanco. La diferencia entre metodos esta en el tiempo necesario
para producir la misma salida.

## Analisis

### 1. Diferencias de tiempo entre secuencial, PyTorch CPU y PyTorch GPU

La version secuencial fue la mas lenta: el pipeline completo tomo 1588.900 s, es decir, unos 26.5
minutos por corrida completa. La causa principal es que el filtrado recorre pixel por pixel en Python
puro. El tiempo de filtrado secuencial fue 1526.404 s, practicamente todo el costo del pipeline.

PyTorch CPU redujo el tiempo total a 140.217 s, con un speed-up de 11.332 respecto de la version
secuencial. En este caso, el filtrado bajo a 75.610 s. La mejora se explica porque PyTorch trabaja con
operaciones tensoriales en lugar de bucles Python por pixel.

PyTorch GPU fue el metodo mas rapido entre los tres medidos. El pipeline completo tomo 99.175 s,
con un speed-up de 16.021 respecto de la version secuencial. Tambien fue 1.41 veces mas rapido que
PyTorch CPU en tiempo total de pipeline.

### 2. FPS efectivos y tiempo real

El video original se reproduce a 29.970 FPS, es decir, casi 30 frames por segundo. Ese valor describe
la velocidad de reproduccion del archivo de entrada, no la velocidad del programa.

Los FPS efectivos indican cuantos frames por segundo pudo procesar cada metodo. Para PyTorch GPU:

```text
944 frames / 99.175 s = 9.519 FPS efectivos
```

Por lo tanto, aunque PyTorch GPU fue el metodo mas rapido, no alcanza procesamiento en tiempo real.
Para eso deberia acercarse a los 29.970 FPS del video original. En esta medicion, el pipeline GPU
quedo aproximadamente 3.15 veces por debajo de la velocidad de reproduccion del video.

### 3. Limites observados del pipeline

El limite principal de PyTorch GPU no fue el computo del filtro. El computo GPU tomo 3.671 s, pero
las transferencias CPU-GPU y GPU-CPU sumaron 31.106 s. Ademas, la escritura/codificacion del video
tomo 58.838 s, un valor mayor que todo el filtrado GPU.

Estos resultados muestran que PyTorch GPU reduce de forma fuerte el costo computacional del filtro,
pero el pipeline completo queda condicionado por decodificacion, transferencias y codificacion. En
otras palabras, acelerar el filtro no elimina automaticamente el costo de mover y escribir frames 4K.

### 4. Reconstruccion del video

Se genero un video procesado por cada metodo:

```text
video4k/resultados/videos/posterize_secuencial_sin_audio.mp4
video4k/resultados/videos/posterize_pytorch_cpu_sin_audio.mp4
video4k/resultados/videos/posterize_pytorch_gpu_sin_audio.mp4
```

El video original no tenia una pista de audio audible/detectable, por lo que se conservaron las
versiones procesadas sin audio.

## Alcance de la comparacion

El analisis principal se centro en tres implementaciones: secuencial, PyTorch CPU y PyTorch GPU.
Estas versiones permiten comparar una linea base directa contra ejecuciones tensoriales sobre CPU
y GPU.

Como extension futura, se podria agregar una comparacion adicional con NumPy y Numba para
contrastar PyTorch contra otras estrategias vistas durante la materia. Esa comparacion deberia
mantener la misma metodologia de medicion para que los resultados sean comparables.

## Conclusiones

El filtro posterize se implemento de forma equivalente en las tres versiones evaluadas. Los hashes
de salida coinciden, por lo que las diferencias medidas corresponden al rendimiento y no a cambios
en el resultado visual.

La version secuencial sirve como linea base, pero no es adecuada para procesar video 4K completo:
alcanzo solo 0.594 FPS efectivos. PyTorch CPU mejora notablemente el rendimiento y alcanza 6.734
FPS efectivos. PyTorch GPU fue la estrategia mas rapida, con 9.519 FPS efectivos y un speed-up de
16.021 respecto de la version secuencial.

Aun asi, el procesamiento completo no llega a tiempo real. En GPU, el calculo del filtro es muy
rapido, pero el costo de transferir cada frame y escribir el video final limita el resultado. Para este
caso, PyTorch GPU es la estrategia mas adecuada, especialmente si se busca reducir el tiempo de
filtrado, pero el rendimiento final del pipeline queda condicionado por la decodificacion, las
transferencias y la codificacion del video.
