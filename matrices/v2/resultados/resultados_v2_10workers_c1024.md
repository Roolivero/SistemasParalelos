# Resultados benchmark — multiplicación de matrices (C = 1024)

Fuente: `resultados_v2_10workers_c1024.csv` (ruta relativa al directorio `matrices/` según ubicación del CSV).

Las columnas **speed_up_*** y **eficiencia_*** usan como baseline el tiempo del método **secuencial** (mismo C, perfil y max-val):
- **_ab**: respecto al tiempo del producto **A·B**.
- **_btat**: respecto al tiempo del producto **Bᵀ·Aᵀ**.

Los **checksum** son la suma de todos los elementos de cada matriz resultado (deben coincidir Σ(A·B) y Σ(Bᵀ·Aᵀ)).

## Tabla

| Algoritmo | C | Perfil | max-val | Workers | t A·B (s) | t Bᵀ·Aᵀ (s) | Speed-up A·B | Eficiencia A·B | Speed-up Bᵀ·Aᵀ | Eficiencia Bᵀ·Aᵀ | Cores | Estado | Σ(A·B) | Σ(Bᵀ·Aᵀ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| secuencial | 1024 | cubo | 256 | 1 | 63.178100 | 58.877171 | 3.779652 | 3.779652 | 2.845825 | 2.845825 | 22 | ok | 34818311 | 34818311 |
| secuencial (tradicional) | 1024 | cubo | 256 | 1 | 238.791204 | 167.554144 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 22 | ok | 34818311 | 34818311 |
| concurrent.futures.ThreadPoolExecutor | 1024 | cubo | 256 | 10 | 18.996816 | 25.321023 | 12.570065 | 1.257006 | 6.617195 | 0.661719 | 22 | ok | 34818311 | 34818311 |
| threading | 1024 | cubo | 256 | 10 | 23.905233 | 24.927668 | 9.989077 | 0.998908 | 6.721613 | 0.672161 | 22 | ok | 34818311 | 34818311 |
| concurrent.futures.ProcessPoolExecutor | 1024 | cubo | 256 | 10 | 20.399256 | 20.461559 | 11.705878 | 1.170588 | 8.188728 | 0.818873 | 22 | ok | 34818311 | 34818311 |
| numba (njit) | 1024 | cubo | 256 | 10 | 2.457141 | 2.359226 | 97.182540 | 9.718254 | 71.020811 | 7.102081 | 22 | ok | 34818311 | 34818311 |

## Notas

- **Eficiencia** = speed-up / número de workers.
- Si falta speed-up/eficiencia para Bᵀ·Aᵀ en un CSV viejo, volvé a ejecutar `benchmark.py` para regenerar columnas.
