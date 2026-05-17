# ⚡ Inicio Rápido - OptiCode QA PASO 1 Automático

## 🎯 En 3 Pasos

### 1️⃣ Instalar Dependencias (30 segundos)

```bash
pip install -r requirements.txt
```

### 2️⃣ Probar el Sistema (1 minuto)

```bash
python test_paso1_automatico.py
```

**Salida esperada:**
```
🧪 TEST: OptiCode QA - PASO 1 Automático
📂 Analizando: src/algoritmos.py
🚀 Iniciando PASO 1 automático...
✅ PASO 1 COMPLETADO EXITOSAMENTE
```

### 3️⃣ Usar la Interfaz Web (2 minutos)

**Opción A: Con servidor Flask (recomendado)**
```bash
python src/servidor_paso1.py
```
Luego abre: **http://localhost:5000**

**Opción B: Sin servidor (solo frontend)**
Abre directamente: `opticode_dashboard_automatico.html`

---

## 🖥️ Uso de la Interfaz

### Paso a Paso:

1. **Cargar código:**
   - Clic en "Cargar algoritmos.py por defecto"
   - O arrastra tu archivo `.py`

2. **Ejecutar análisis:**
   - Clic en "🚀 Ejecutar PASO 1 Completo"
   - Espera 10-30 segundos

3. **Ver resultados:**
   - Tabla con benchmarks
   - Cuellos de botella identificados
   - Reportes descargables

---

## 📊 ¿Qué Hace el Sistema?

### Automáticamente ejecuta:

✅ **Análisis de Complejidad** (simula Bob IDE)
- Identifica Big-O de cada función
- Detecta bucles anidados
- Encuentra operaciones costosas

✅ **Benchmarks Prácticos**
- Mide tiempo de ejecución
- Mide uso de memoria
- Prueba con N = 10, 50, 100, 500, 1000

✅ **Comparación Teoría vs Práctica**
- Calcula divergencia
- Identifica discrepancias
- Genera recomendaciones

✅ **Reportes Automáticos**
- Markdown técnico (estilo Bob)
- JSON para integración
- Comparación ejecutiva

---

## 📁 Archivos Generados

Después de ejecutar, encontrarás:

```
bob_sessions/
  └── analisis_automatico.md      ← Análisis técnico completo

data/
  └── metricas_salida.json         ← Benchmarks en JSON

output/
  ├── PASO1_COMPARACION.md         ← Comparación teoría vs práctica
  └── paso1_resumen.json           ← Resumen ejecutivo
```

---

## 🎨 Capturas de Pantalla

### Interfaz Principal
```
┌─────────────────────────────────────────────────────────┐
│  OptiCode QA — PASO 1 Automático                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Panel de Control          │  Resultados                │
│  ┌──────────────────┐     │  ┌──────────────────────┐  │
│  │ 1. Código Fuente │     │  │ Comparación          │  │
│  │    algoritmos.py │     │  │ Teoría vs Práctica   │  │
│  │    [Cargar]      │     │  │                      │  │
│  └──────────────────┘     │  │ N  │ Tiempo │ RAM   │  │
│                            │  │ 10 │ 0.15ms │ 2.4KB │  │
│  🚀 Ejecutar PASO 1       │  │ 100│ 1.52ms │ 24KB  │  │
│                            │  └──────────────────────┘  │
│  Consola:                  │                            │
│  ✓ Análisis completado     │  Cuellos de Botella:      │
│  ✓ Benchmarks OK           │  • P0: I/O en bucle       │
│  ✓ Reportes generados      │  • P1: Búsqueda lineal    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting Rápido

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask flask-cors
```

### ❌ "Servidor no responde"
Verifica que esté corriendo:
```bash
python src/servidor_paso1.py
```

### ❌ "Error al ejecutar código"
Asegúrate de que tu código Python sea válido:
```python
# ✅ Correcto
def dfs(graph, start):
    return []

# ❌ Incorrecto (error de sintaxis)
def dfs(graph, start)
    return []
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Analizar DFS
```python
# Tu código: algoritmos.py
def dfs(graph, start):
    visited = set()
    order = []
    
    def _dfs(u):
        visited.add(u)
        order.append(u)
        for v in graph.get(u, []):
            if v not in visited:
                _dfs(v)
    
    _dfs(start)
    return order
```

**Resultado automático:**
- Complejidad: O(V + E)
- Cuellos: Búsqueda lineal `in visited`
- Recomendación: Usar set en lugar de lista

### Ejemplo 2: Analizar Bubble Sort
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

**Resultado automático:**
- Complejidad: O(N²)
- Cuellos: Bucles anidados
- Recomendación: Considerar QuickSort o MergeSort

---

## 🚀 Comandos Útiles

### Ejecutar prueba completa
```bash
python test_paso1_automatico.py
```

### Iniciar servidor web
```bash
python src/servidor_paso1.py
```

### Analizar código específico
```python
from src.paso1_automatico import ejecutar_paso1_desde_archivo

resultado = ejecutar_paso1_desde_archivo("mi_codigo.py")
print(resultado['comparacion']['divergencia'])
```

### Usar solo el analizador
```python
from src.analizador_automatico import generar_reporte

codigo = open("algoritmos.py").read()
reporte = generar_reporte(codigo, "algoritmos.py")
print(reporte)
```

---

## 📚 Documentación Completa

Para más detalles, consulta:
- **README_PASO1_AUTOMATICO.md** - Documentación completa
- **bob_sessions/PASO1_RESUMEN_COMPLETADO.md** - Contexto del proyecto

---

## 🎯 Checklist de Verificación

Antes de presentar al jurado:

- [ ] ✅ Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] ✅ Prueba ejecutada exitosamente (`python test_paso1_automatico.py`)
- [ ] ✅ Servidor web funciona (`python src/servidor_paso1.py`)
- [ ] ✅ Interfaz carga correctamente (http://localhost:5000)
- [ ] ✅ Análisis completo genera reportes
- [ ] ✅ Reportes visibles en `output/` y `bob_sessions/`

---

## 🏆 Ventajas del Sistema

| Característica | Valor |
|----------------|-------|
| **Tiempo de análisis** | < 1 minuto |
| **Costo** | $0 (vs Bobcoins) |
| **Automatización** | 100% |
| **Repetibilidad** | Ilimitada |
| **Integración** | API REST |
| **Reportes** | Automáticos |

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa la **Consola de Ejecución** en la interfaz web
2. Ejecuta `python test_paso1_automatico.py` para diagnóstico
3. Verifica que todas las dependencias estén instaladas
4. Consulta **README_PASO1_AUTOMATICO.md** para troubleshooting detallado

---

**¡Listo para usar! 🎉**

El sistema está completamente funcional y listo para demostrar al jurado.