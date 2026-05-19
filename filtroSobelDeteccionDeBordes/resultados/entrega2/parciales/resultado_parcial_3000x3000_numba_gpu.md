# Resultado parcial Sobel 3000x3000 - Numba GPU

## Entorno

- CPU: AMD Ryzen 5 5600X 6-Core Processor
- Nucleos fisicos: 6
- Nucleos logicos: 12
- RAM: 15.52 GiB total, 10.71 GiB disponible
- Sistema operativo: Linux-6.18.26-1-MANJARO-x86_64-with-glibc2.43
- Python: 3.14.4 free-threading build | packaged by conda-forge | (main, Apr  8 2026, 01:59:32) [GCC 14.3.0]
- GIL habilitado: False
- NumPy: 2.4.3
- Numba: 0.65.1
- GPU CUDA: NVIDIA GeForce RTX 2060

## Tabla solicitada

| metodo | tiempo RGB->gris (s) | tiempo Sobel (s) | tiempo total (s) | % blancos | speed-up | performance (%) |
|---|---:|---:|---:|---:|---:|---:|
| Numba GPU | 0.001099 | 0.004376 | 0.005475 | 0.001367 |  |  |

## Datos de control

| metodo | tamanio | corridas | workers/hilos | seed | pixeles blancos | pixeles totales | checksum Sobel | hash salida | estado |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Numba GPU | 3000x3000 | 5 | 256 | 2026 | 123 | 9000000 | 47884245 | 56d292135dc0414f | ok |

## Detalle de corridas

### Numba GPU

| corrida | RGB->gris (s) | Sobel (s) | total (s) | % blancos | checksum | hash |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.001141 | 0.004219 | 0.005361 | 0.001367 | 47884245 | 56d292135dc0414f |
| 2 | 0.001089 | 0.004611 | 0.005700 | 0.001367 | 47884245 | 56d292135dc0414f |
| 3 | 0.001090 | 0.004210 | 0.005300 | 0.001367 | 47884245 | 56d292135dc0414f |
| 4 | 0.001083 | 0.004229 | 0.005313 | 0.001367 | 47884245 | 56d292135dc0414f |
| 5 | 0.001090 | 0.004610 | 0.005700 | 0.001367 | 47884245 | 56d292135dc0414f |

## Transferencias CPU-GPU

Estos tiempos se registran aparte para analizar el costo de mover datos entre host y dispositivo. No se suman en la columna de tiempo total solicitada, que mide solamente conversion RGB->gris y Sobel.

| metodo | H2D CPU->GPU (s) | D2H GPU->CPU (s) | transferencia total (s) | computo total (s) | total con transferencias (s) |
|---|---:|---:|---:|---:|---:|
| Numba GPU | 0.003251 | 0.001517 | 0.004768 | 0.005475 | 0.010242 |

## Notas

- Los tiempos excluyen generacion de imagen y cualquier I/O; solo se mide conversion RGB->gris y Sobel.
- La imagen de entrada se carga desde imagenes/ y la carga queda fuera de la medicion.
- Para Numba GPU, las transferencias CPU-GPU se registran aparte para responder el analisis de la entrega 2.
- Speed-up = tiempo total secuencial promedio / tiempo total del metodo promedio.
- Performance (%) = speed-up / unidades usadas * 100. Para Numba CPU se usan los hilos configurados; para secuencial y NumPy se usa 1 unidad explicita.
- Si todavia no aparece la fila secuencial, speed-up y performance quedan vacios porque falta la referencia.
