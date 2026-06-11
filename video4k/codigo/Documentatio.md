# Documentatio - TP4 video 4K con PyTorch

## Que pide la consigna

El trabajo practico 4 pide procesar un video 4K de aproximadamente 30 segundos con un filtro
elegido. El procesamiento debe hacerse frame por frame o en lotes chicos, sin cargar el video
completo en memoria.

Las versiones requeridas son:

- version secuencial en Python, usada como linea base;
- version PyTorch CPU;
- version PyTorch GPU, si el hardware disponible lo permite.

Tambien se debe reconstruir el video final y reincorporar el audio original si el video de entrada
lo tiene. En este caso, `ffprobe` no detecto una pista de audio en el video original, por lo que se
entregan los videos procesados sin audio.

## Video de entrada

El video elegido para el TP esta ubicado en:

```text
video4k/15785079_2160_3840_30fps.mp4
```

El script detecta resolucion, FPS, cantidad de frames y duracion usando OpenCV.

## Filtro elegido

El filtro elegido es **posterize filter** con estilo pop-art.

La idea es convertir cada pixel a una luminancia y reemplazarlo por uno de cuatro colores fijos.
No se detectan objetos como "leon" o "selva"; cada pixel se clasifica solamente por su intensidad.
Esto mantiene el filtro simple, reproducible y equivalente entre implementaciones.

Paleta elegida:

```text
0   a 63   -> verde    RGB (27, 127, 58)
64  a 127  -> fucsia   RGB (232, 62, 140)
128 a 191  -> amarillo RGB (255, 216, 77)
192 a 255  -> blanco   RGB (255, 255, 255)
```

La luminancia se calcula con la formula estandar:

```text
luminancia = 0.299R + 0.587G + 0.114B
```

En el codigo se usa la forma entera equivalente:

```text
luminancia = (299R + 587G + 114B) // 1000
```

Se eligio esta forma para que la version secuencial y PyTorch clasifiquen igual los pixeles que
caen cerca de los limites entre rangos.

## Archivos implementados

```text
video4k/codigo/posterize_filter.py
video4k/codigo/video_lib.py
video4k/codigo/benchmark_video4k.py
video4k/codigo/generar_resumen_video4k.py
video4k/codigo/Documentatio.md
```

### posterize_filter.py

Contiene el filtro y las tres implementaciones:

- `SequentialPosterize`: recorre cada pixel con bucles Python.
- `TorchPosterizeCPU`: usa tensores PyTorch en CPU.
- `TorchPosterizeGPU`: usa tensores PyTorch en CUDA si esta disponible.

OpenCV lee los frames en formato BGR, no RGB. Por eso la paleta se define en RGB para explicar
el filtro, pero internamente se guarda tambien en BGR para escribir el video correctamente.

### video_lib.py

Contiene funciones compartidas:

- deteccion de informacion del video;
- datos del entorno de ejecucion;
- calculo de speed-up;
- escritura de CSV;
- escritura de Markdown parcial y agregado;
- reincorporacion opcional de audio con `ffmpeg`.

### benchmark_video4k.py

Procesa el video como flujo:

```text
leer frame
aplicar filtro
escribir frame filtrado
liberar referencias
continuar con el siguiente frame
```

No guarda todos los frames en memoria.

Cada ejecucion corresponde a un solo metodo. Esto mantiene los resultados parciales separados,
como venimos haciendo en los trabajos anteriores.

### generar_resumen_video4k.py

No procesa video. Solo lee el CSV existente y genera un resumen Markdown con todos los metodos
que ya fueron ejecutados.

## Que se mide

Para cada metodo se registra:

- tiempo de lectura o decodificacion de frames;
- tiempo de filtrado;
- tiempo de escritura o codificacion;
- tiempo total del pipeline;
- cantidad de frames procesados;
- resolucion;
- FPS del video original;
- FPS efectivos del procesamiento;
- codec usado para reconstruir el video;
- memoria pico aproximada del proceso;
- speed-up respecto de la version secuencial;
- checksum y hash de salida como control de reproducibilidad.

En PyTorch GPU, ademas se registra:

- transferencia CPU -> GPU;
- computo en GPU;
- transferencia GPU -> CPU.

La columna `filtrado` de la tabla principal incluye transferencia, computo y vuelta a CPU, porque
el frame se lee desde CPU y se escribe desde CPU. El detalle GPU queda separado para el analisis.

## Como ejecutar los benchmarks

Desde la carpeta:

```bash
cd /home/ro/Desktop/facu/SistemasParalelos/video4k/codigo
```

Primero conviene hacer una prueba corta para verificar que todo funciona:

```bash
python benchmark_video4k.py --method secuencial --runs 1 --max-frames 60
python benchmark_video4k.py --method pytorch_cpu --runs 1 --max-frames 60 --workers 6
python benchmark_video4k.py --method pytorch_gpu --runs 1 --max-frames 60
```

Para el benchmark final, ejecutar sin `--max-frames`:

```bash
python benchmark_video4k.py --method secuencial --runs 3
python benchmark_video4k.py --method pytorch_cpu --runs 3 --workers 6
python benchmark_video4k.py --method pytorch_gpu --runs 3
```

Si no hay GPU compatible, ejecutar solo:

```bash
python benchmark_video4k.py --method secuencial --runs 3
python benchmark_video4k.py --method pytorch_cpu --runs 3 --workers 6
```

Y en el informe aclarar explicitamente que PyTorch GPU no se pudo medir por falta de CUDA
compatible.

## Archivos de salida

Los resultados se guardan en:

```text
video4k/resultados/
```

CSV general:

```text
video4k/resultados/resultados_video4k.csv
```

Markdown agregado:

```text
video4k/resultados/resultados_video4k.md
```

Markdown parcial por metodo:

```text
video4k/resultados/parciales/resultado_parcial_posterize_secuencial.md
video4k/resultados/parciales/resultado_parcial_posterize_pytorch_cpu.md
video4k/resultados/parciales/resultado_parcial_posterize_pytorch_gpu.md
```

Videos generados:

```text
video4k/resultados/videos/posterize_secuencial_sin_audio.mp4
video4k/resultados/videos/posterize_pytorch_cpu_sin_audio.mp4
video4k/resultados/videos/posterize_pytorch_gpu_sin_audio.mp4
```

Como el video original no tiene una pista de audio detectable, no se conservan versiones
`*_con_audio.mp4`.

Para abrir los videos generados con `mpv`:

```bash
mpv /home/ro/Desktop/facu/SistemasParalelos/video4k/resultados/videos/posterize_secuencial_sin_audio.mp4
mpv /home/ro/Desktop/facu/SistemasParalelos/video4k/resultados/videos/posterize_pytorch_cpu_sin_audio.mp4
mpv /home/ro/Desktop/facu/SistemasParalelos/video4k/resultados/videos/posterize_pytorch_gpu_sin_audio.mp4
```

## Fusion de resultados

Cuando ya existan los parciales, se puede generar el resumen:

```bash
python generar_resumen_video4k.py
```

Eso genera:

```text
video4k/resultados/finales/resumen_benchmarks_video4k.md
```

Ese archivo sirve como base para el informe final.

## Pendiente para el informe final

Despues de correr los benchmarks hay que redactar:

- descripcion del video usado;
- descripcion y justificacion del filtro posterize;
- entorno de ejecucion con CPU, RAM, sistema operativo, Python, OpenCV, PyTorch y GPU si corresponde;
- metodologia de medicion;
- tabla de resultados;
- analisis de speed-up;
- limites observados por lectura/escritura de video;
- manejo de memoria;
- reconstruccion del video y audio;
- conclusiones.

## Relacion con el codigo guia del docente

Se conserva el criterio del codigo guia:

- usar `perf_counter` para medir etapas;
- separar carga/escritura de la parte de computo cuando el analisis lo requiere;
- sincronizar GPU antes de cerrar mediciones;
- mantener una linea base secuencial clara;
- guardar resultados parciales para poder armar el informe final sin repetir todo.
