# Resultados benchmark — multiplicación de matrices (C = 512)

Fuente: `resultados_v2_4workers_c512.csv` (ruta relativa al directorio `matrices/` según ubicación del CSV).

Las columnas **speed_up_*** y **eficiencia_*** usan como baseline el tiempo del método **secuencial** (mismo C, perfil y max-val):
- **_ab**: respecto al tiempo del producto **A·B**.
- **_btat**: respecto al tiempo del producto **Bᵀ·Aᵀ**.

Los **checksum** son la suma de todos los elementos de cada matriz resultado (deben coincidir Σ(A·B) y Σ(Bᵀ·Aᵀ)).

## Tabla

| Algoritmo | C | Perfil | max-val | Workers | t A·B (s) | t Bᵀ·Aᵀ (s) | Speed-up A·B | Eficiencia A·B | Speed-up Bᵀ·Aᵀ | Eficiencia Bᵀ·Aᵀ | Cores | Estado | Σ(A·B) | Σ(Bᵀ·Aᵀ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| secuencial | 512 | cubo | 256 | 1 | 6.589254 | 6.361890 | 1.507456 | 1.507456 | 1.561761 | 1.561761 | 22 | ok | -110463704 | -110463704 |
| secuencial (tradicional) | 512 | cubo | 256 | 1 | 9.933010 | 9.935754 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 22 | ok | -110463704 | -110463704 |
| concurrent.futures.ThreadPoolExecutor | 512 | cubo | 256 | 4 | 4.083622 | 4.696354 | 2.432402 | 0.608100 | 2.115631 | 0.528908 | 22 | ok | -110463704 | -110463704 |
| threading | 512 | cubo | 256 | 4 | 4.145853 | 4.461545 | 2.395891 | 0.598973 | 2.226976 | 0.556744 | 22 | ok | -110463704 | -110463704 |
| concurrent.futures.ProcessPoolExecutor | 512 | cubo | 256 | 4 | 3.148144 | 3.066812 | 3.155196 | 0.788799 | 3.239766 | 0.809942 | 22 | ok | -110463704 | -110463704 |
| numba (njit) | 512 | cubo | 256 | 4 | 0.536763 | 0.544091 | 18.505393 | 4.626348 | 18.261199 | 4.565300 | 22 | ok | -110463704 | -110463704 |

## Notas

- **Eficiencia** = speed-up / número de workers.
- Si falta speed-up/eficiencia para Bᵀ·Aᵀ en un CSV viejo, volvé a ejecutar `benchmark.py` para regenerar columnas.
