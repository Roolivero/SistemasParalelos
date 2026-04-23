# Resultados benchmark — multiplicación de matrices (C = 512)

Fuente: `resultados_v2_1worker_c512.csv` (ruta relativa al directorio `matrices/` según ubicación del CSV).

Las columnas **speed_up_*** y **eficiencia_*** usan como baseline el tiempo del método **secuencial** (mismo C, perfil y max-val):
- **_ab**: respecto al tiempo del producto **A·B**.
- **_btat**: respecto al tiempo del producto **Bᵀ·Aᵀ**.

Los **checksum** son la suma de todos los elementos de cada matriz resultado (deben coincidir Σ(A·B) y Σ(Bᵀ·Aᵀ)).

## Tabla

| Algoritmo | C | Perfil | max-val | Workers | t A·B (s) | t Bᵀ·Aᵀ (s) | Speed-up A·B | Eficiencia A·B | Speed-up Bᵀ·Aᵀ | Eficiencia Bᵀ·Aᵀ | Cores | Estado | Σ(A·B) | Σ(Bᵀ·Aᵀ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| secuencial | 512 | cubo | 256 | 1 | 6.594259 | 6.329482 | 1.408197 | 1.408197 | 1.469898 | 1.469898 | 22 | ok | -110463704 | -110463704 |
| secuencial (tradicional) | 512 | cubo | 256 | 1 | 9.286013 | 9.303695 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 22 | ok | -110463704 | -110463704 |
| concurrent.futures.ThreadPoolExecutor | 512 | cubo | 256 | 1 | 7.070678 | 7.524049 | 1.313313 | 1.313313 | 1.236528 | 1.236528 | 22 | ok | -110463704 | -110463704 |
| threading | 512 | cubo | 256 | 1 | 7.261479 | 7.233229 | 1.278805 | 1.278805 | 1.286244 | 1.286244 | 22 | ok | -110463704 | -110463704 |
| concurrent.futures.ProcessPoolExecutor | 512 | cubo | 256 | 1 | 6.942384 | 6.634457 | 1.337583 | 1.337583 | 1.402330 | 1.402330 | 22 | ok | -110463704 | -110463704 |
| numba (njit) | 512 | cubo | 256 | 1 | 0.580156 | 0.610545 | 16.006062 | 16.006062 | 15.238344 | 15.238344 | 22 | ok | -110463704 | -110463704 |

## Notas

- **Eficiencia** = speed-up / número de workers.
- Si falta speed-up/eficiencia para Bᵀ·Aᵀ en un CSV viejo, volvé a ejecutar `benchmark.py` para regenerar columnas.
