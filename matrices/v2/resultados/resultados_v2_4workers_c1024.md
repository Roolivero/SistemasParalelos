# Resultados benchmark — multiplicación de matrices (C = 1024)

Fuente: `resultados_v2_4workers_c1024.csv` (ruta relativa al directorio `matrices/` según ubicación del CSV).

Las columnas **speed_up_*** y **eficiencia_*** usan como baseline el tiempo del método **secuencial** (mismo C, perfil y max-val):
- **_ab**: respecto al tiempo del producto **A·B**.
- **_btat**: respecto al tiempo del producto **Bᵀ·Aᵀ**.

Los **checksum** son la suma de todos los elementos de cada matriz resultado (deben coincidir Σ(A·B) y Σ(Bᵀ·Aᵀ)).

## Tabla

| Algoritmo | C | Perfil | max-val | Workers | t A·B (s) | t Bᵀ·Aᵀ (s) | Speed-up A·B | Eficiencia A·B | Speed-up Bᵀ·Aᵀ | Eficiencia Bᵀ·Aᵀ | Cores | Estado | Σ(A·B) | Σ(Bᵀ·Aᵀ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| secuencial | 1024 | cubo | 256 | 1 | 62.864523 | 56.041876 | 3.836468 | 3.836468 | 3.608046 | 3.608046 | 22 | ok | 34818311 | 34818311 |
| secuencial (tradicional) | 1024 | cubo | 256 | 1 | 241.177753 | 202.201683 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 22 | ok | 34818311 | 34818311 |
| concurrent.futures.ThreadPoolExecutor | 1024 | cubo | 256 | 4 | 31.794210 | 35.050143 | 7.585587 | 1.896397 | 5.768926 | 1.442232 | 22 | ok | 34818311 | 34818311 |
| threading | 1024 | cubo | 256 | 4 | 35.203877 | 34.519706 | 6.850886 | 1.712722 | 5.857573 | 1.464393 | 22 | ok | 34818311 | 34818311 |
| concurrent.futures.ProcessPoolExecutor | 1024 | cubo | 256 | 4 | 26.970618 | 27.427959 | 8.942241 | 2.235560 | 7.372101 | 1.843025 | 22 | ok | 34818311 | 34818311 |
| numba (njit) | 1024 | cubo | 256 | 4 | 2.495315 | 2.658940 | 96.652227 | 24.163057 | 76.045974 | 19.011494 | 22 | ok | 34818311 | 34818311 |

## Notas

- **Eficiencia** = speed-up / número de workers.
- Si falta speed-up/eficiencia para Bᵀ·Aᵀ en un CSV viejo, volvé a ejecutar `benchmark.py` para regenerar columnas.
