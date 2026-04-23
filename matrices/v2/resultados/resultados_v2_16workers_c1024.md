# Resultados benchmark — multiplicación de matrices (C = 1024)

Fuente: `resultados_v2_16workers_c1024.csv` (ruta relativa al directorio `matrices/` según ubicación del CSV).

Las columnas **speed_up_*** y **eficiencia_*** usan como baseline el tiempo del método **secuencial** (mismo C, perfil y max-val):
- **_ab**: respecto al tiempo del producto **A·B**.
- **_btat**: respecto al tiempo del producto **Bᵀ·Aᵀ**.

Los **checksum** son la suma de todos los elementos de cada matriz resultado (deben coincidir Σ(A·B) y Σ(Bᵀ·Aᵀ)).

## Tabla

| Algoritmo | C | Perfil | max-val | Workers | t A·B (s) | t Bᵀ·Aᵀ (s) | Speed-up A·B | Eficiencia A·B | Speed-up Bᵀ·Aᵀ | Eficiencia Bᵀ·Aᵀ | Cores | Estado | Σ(A·B) | Σ(Bᵀ·Aᵀ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| secuencial | 1024 | cubo | 256 | 1 | 69.697017 | 57.396771 | 3.102546 | 3.102546 | 3.076964 | 3.076964 | 22 | ok | 34818311 | 34818311 |
| secuencial (tradicional) | 1024 | cubo | 256 | 1 | 216.238226 | 176.607797 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 22 | ok | 34818311 | 34818311 |
| concurrent.futures.ThreadPoolExecutor | 1024 | cubo | 256 | 16 | 18.180905 | 25.259255 | 11.893700 | 0.743356 | 6.991805 | 0.436988 | 22 | ok | 34818311 | 34818311 |
| threading | 1024 | cubo | 256 | 16 | 23.817357 | 23.784791 | 9.079019 | 0.567439 | 7.425241 | 0.464078 | 22 | ok | 34818311 | 34818311 |
| concurrent.futures.ProcessPoolExecutor | 1024 | cubo | 256 | 16 | 18.492709 | 18.103380 | 11.693161 | 0.730823 | 9.755515 | 0.609720 | 22 | ok | 34818311 | 34818311 |
| numba (njit) | 1024 | cubo | 256 | 16 | 2.391426 | 3.608904 | 90.422294 | 5.651393 | 48.936685 | 3.058543 | 22 | ok | 34818311 | 34818311 |

## Notas

- **Eficiencia** = speed-up / número de workers.
- Si falta speed-up/eficiencia para Bᵀ·Aᵀ en un CSV viejo, volvé a ejecutar `benchmark.py` para regenerar columnas.
