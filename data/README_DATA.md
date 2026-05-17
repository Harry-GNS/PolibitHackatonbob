# 📁 data/ — Datos de Entrada y Métricas de Salida

## 📝 Propósito
Esta carpeta contiene:
- **Archivos de entrada:** grafos, datos de prueba
- **Resultados de benchmarks:** JSON con métricas de tiempo y memoria

## 📋 Estructura

### 📥 Entrada (Datos de Prueba)

#### `grafos_prueba.json`
Grafo de prueba para usar en algoritmos de búsqueda (DFS, BFS, etc).

**Formato:**
```json
{
  "A": ["B", "C", "D"],
  "B": ["E", "F"],
  "C": ["G", "H", "I"],
  ...
}
```

**Uso:** Motor local lo usa automáticamente para benchmarks.

### 📊 Salida (Resultados de Benchmarks)

#### `metricas_salida.json`
Generado por `src/motor_qa.py` después de ejecutar benchmarks.

**Formato:**
```json
{
  "benchmarks": {
    "10": {
      "time_ms_mean": 0.15,
      "time_ms_samples": [0.14, 0.16, 0.15],
      "mem_bytes_peak_mean": 2400,
      "mem_bytes_peak_samples": [2400, 2400, 2400]
    },
    "100": {
      "time_ms_mean": 1.52,
      "mem_bytes_peak_mean": 24000
    },
    "1000": {...},
    "5000": {...}
  }
}
```

**Contenido:**
- Tamaños de entrada probados: N = 10, 100, 1000, 5000
- Tiempo de ejecución en milisegundos
- Uso de memoria en bytes
- 3 muestras por tamaño (promedio + muestras individuales)

## 🔄 Workflow

### 1️⃣ Preparar Datos de Entrada
```bash
# Edita grafos_prueba.json con tus datos de prueba
# O usa los proporcionados por defecto
```

### 2️⃣ Ejecutar Motor Local
```bash
# Genera metricas_salida.json automáticamente
python src/motor_qa.py
```

### 3️⃣ Usar en GUI
```bash
# La GUI carga metricas_salida.json automáticamente
python src/gui_paso1_real.py
```

## 📈 Interpretación de Métricas

```
N=10        N=100       N=1000      N=5000
└─ 0.15ms   └─ 1.52ms   └─ 15.2ms   └─ 152ms

Si el crecimiento es lineal (3-5x por 10x N) → O(N)
Si el crecimiento es cuadrático (100x por 10x N) → O(N²)
Si el crecimiento es cúbico (1000x por 10x N) → O(N³)
```

## 🎯 Archivos a Ignorar

- `metricas_salida.json` se recomienda **NO hacer commit** (se regenera cada ejecución)
- O hacer commit con `.gitignore` para no saturar el histórico

## 📝 Notas

- Los benchmarks se ejecutan **3 veces por tamaño** para obtener promedio
- Se mide con `time.perf_counter()` para precisión en milisegundos
- Se usa `tracemalloc` para medir pico de memoria
