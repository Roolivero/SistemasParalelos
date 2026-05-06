# Documentatio - Sobel entrega 1

## Que se implemento

Para la entrega del 7/05 se implementaron tres versiones:

- `sobel_secuencial.py`: version secuencial pura con bucles Python, sin importar modulos ni librerias.
- `sobel_numpy.py`: version vectorizada con NumPy.
- `sobel_numba_cpu.py`: version Numba CPU con `njit(parallel=True)` y `prange`.
- `benchmark_sobel.py`: script para correr benchmarks por partes y generar Markdown/CSV.
- `generar_finales_sobel.py`: script para juntar CSV existentes y generar finales por metodo.

La consigna pide medir por separado:

- conversion RGB->gris;
- aplicacion del filtro Sobel;
- tiempo total como suma de ambas partes.

El benchmark hace al menos 5 corridas por defecto y usa el promedio.

## Formula RGB->gris

Se usa la luminancia indicada por la consigna:

```text
I = 0.299R + 0.587G + 0.114B
```

En la version secuencial esto se hace pixel por pixel. En NumPy se hace con operaciones sobre
arreglos completos. En Numba se hace con un kernel compilado y paralelizado por filas.

## Formula Sobel

Se usan las mascaras de la consigna:

```text
Gx = [-1  0  1]
     [-2  0  2]
     [-1  0  1]

Gy = [ 1  2  1]
     [ 0  0  0]
     [-1 -2 -1]
```

Para cada pixel interior se calcula:

```text
grad = sqrt(gx^2 + gy^2)
```

Luego se recorta al rango de imagen:

```text
si grad > 255 -> 255
si no -> int(grad)
```

Los bordes de la imagen quedan en 0 porque no tienen una vecindad 3x3 completa.

## Por que la version secuencial usa bytes

La version secuencial trabaja con `bytes` y `bytearray`, no con operaciones vectorizadas ni librerias.
Eso permite representar la imagen de forma compacta y recorrerla con bucles normales de Python.

El benchmark genera la imagen sintetica con tipos basicos de Python fuera de la medicion. Eso no
entra en los tiempos del benchmark. La parte medida de la version secuencial tampoco usa NumPy.

## Por que hay una imagen sintetica

No habia una imagen base en la carpeta. Para que las corridas sean reproducibles, el script genera
una imagen RGB sintetica del tamanio pedido. Esa imagen tiene:

- un rectangulo;
- una banda vertical;
- un cuadrado central;
- una linea diagonal.

Asi hay bordes reales para detectar y todos los metodos reciben la misma entrada si se usa el mismo
`--size` y el mismo `--seed`.

## Relacion con el libro

El libro presenta Sobel como un recorrido de vecinos 3x3 sobre una imagen en gris. Tambien muestra
que con Numba se puede paralelizar el bucle externo con `prange`, repartiendo filas entre hilos.

Para NumPy, el libro propone reformular el problema con cortes de arreglos: en vez de recorrer pixel
por pixel desde Python, se toman submatrices como `top_left`, `top`, `right`, etc. Cada submatriz
representa una posicion de la vecindad 3x3.

## Diferencia entre NumPy y Numba CPU

NumPy evita bucles Python expresando operaciones completas sobre arreglos. No escribimos la
paralelizacion explicita, sino que delegamos trabajo a rutinas optimizadas.

Numba CPU conserva una forma parecida al algoritmo secuencial, pero compila la funcion. Con
`parallel=True` y `prange`, Numba puede repartir filas de la imagen entre varios hilos.

Importante: no se agregaron librerias extra. Para la entrega 1 se usan solo las herramientas pedidas:
Python puro en secuencial, NumPy en la version NumPy y Numba/NumPy en la version Numba CPU
porque Numba trabaja sobre arreglos numericos.

## Que se mide y que no se mide

Se mide:

- tiempo de conversion RGB->gris;
- tiempo de Sobel;
- tiempo total.

No se mide:

- generacion de la imagen;
- escritura de CSV o Markdown;
- calculo de metricas de control como hash o checksum;
- carga/guardado en disco.

Esto respeta la consigna, que pide excluir I/O.

## Porcentaje de blancos

La metrica de salida pedida es:

```text
% blancos = pixeles con valor 255 / pixeles totales * 100
```

El valor 255 aparece cuando la magnitud del gradiente supera el rango visible y se recorta a 255.

## Speed-up y performance

El speed-up se calcula con el tiempo total promedio:

```text
speed-up = tiempo secuencial / tiempo del metodo
```

La performance se calcula siguiendo la idea de eficiencia del libro:

```text
performance (%) = speed-up / unidades usadas * 100
```

Para Numba CPU, las unidades usadas son los hilos configurados con `--workers`.
Para secuencial y NumPy se usa 1 unidad explicita, porque no estamos controlando manualmente
workers en esas versiones.

## Como correr por partes

Desde esta carpeta:

```bash
cd /home/ro/Desktop/facu/SistemasParalelos/filtroSobelDeteccionDeBordes/codigo
```

Para correr todo lo de la entrega 1 en un solo tamanio:

```bash
python benchmark_sobel.py --size 750 --methods secuencial,numpy,numba_cpu --runs 5
```

Para correr solo un metodo:

```bash
python benchmark_sobel.py --size 750 --methods secuencial --runs 5
python benchmark_sobel.py --size 750 --methods numpy --runs 5
python benchmark_sobel.py --size 750 --methods numba_cpu --runs 5 --workers 8
```

Para los tamanios de la consigna, repetir cambiando `--size`:

```bash
python benchmark_sobel.py --size 1500 --methods secuencial,numpy,numba_cpu --runs 5
python benchmark_sobel.py --size 3000 --methods secuencial,numpy,numba_cpu --runs 5
python benchmark_sobel.py --size 6000 --methods secuencial,numpy,numba_cpu --runs 5
```

Si la maquina se satura, conviene correr de a un metodo por vez, sobre todo en `3000` y `6000`.

## Archivos que genera

Los resultados se guardan en:

```text
filtroSobelDeteccionDeBordes/resultados/
```

Por cada tamanio se genera:

```text
resultados_sobel_750x750.csv
resultados_sobel_750x750.md
```

Y tambien parciales por metodo:

```text
parciales/resultado_parcial_750x750_secuencial.md
parciales/resultado_parcial_750x750_numpy.md
parciales/resultado_parcial_750x750_numba_cpu.md
```

El Markdown por tamanio sirve para armar la tabla del informe final. Los parciales sirven para
guardar lo que se corrio paso a paso.

## Finales por metodo

Cada vez que `benchmark_sobel.py` termina una corrida, tambien actualiza el archivo final del metodo
ejecutado en:

```text
resultados/finales/resultado_final_secuencial.md
resultados/finales/resultado_final_numpy.md
resultados/finales/resultado_final_numba_cpu.md
```

Si ya existen CSV y solo queres regenerar esos finales sin volver a correr los benchmarks:

```bash
python generar_finales_sobel.py
```

Esos finales incluyen la tabla **Blancos normalizados por escala**. Esa tabla divide los pixeles
blancos por el crecimiento del lado de la imagen respecto del tamanio base. Sirve para comparar
contornos de forma mas justa, porque los bordes crecen como lineas y no como area completa.
