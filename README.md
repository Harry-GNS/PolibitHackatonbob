# 📊 OptiCode QA — PASO 1 (Polibit Hackathon 2026)

**Sistema integrado para auditoría automática de rendimiento y complejidad de código Python.**

---

## 🎯 Descripción General

OptiCode QA es una herramienta completa que automatiza el ciclo de análisis de algoritmos:
- **Análisis teórico de complejidad** (simulando IBM Bob IDE)
- **Benchmarks prácticos** (medición real de tiempo y memoria)
- **Comparación teoría vs práctica** (divergencia automática)
- **Generación de reportes** (Markdown + JSON + PDF)
- **Interfaz web moderna** (Dashboard interactivo)
- **Integración con watsonx.ai** (análisis avanzado)

### ✨ Características Principales

✅ Análisis automático de complejidad (AST - Abstract Syntax Tree)  
✅ Benchmarks prácticos con múltiples tamaños de entrada (N = 10, 100, 1000, 5000)  
✅ Medición dual: tiempo de ejecución (ms) + consumo de memoria (MB)  
✅ Comparación teoría vs práctica con cálculo de divergencia  
✅ Generación automática de reportes en Markdown  
✅ API REST completa para integración programática  
✅ Interfaz web responsive con gráficas interactivas  
✅ Detección de alertas de rendimiento  
✅ Exportación a PDF (próximamente)  

---

## 📋 Tabla de Contenidos

1. [Instalación Rápida](#instalación-rápida)
2. [Uso del Dashboard Web](#uso-del-dashboard-web)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Estructura de Carpetas](#estructura-de-carpetas)
5. [Flujo PASO 1 Completo](#flujo-paso-1-completo)
6. [API REST](#api-rest)
7. [Archivos Generados](#archivos-generados)
8. [Interpretación de Resultados](#interpretación-de-resultados)
9. [Troubleshooting](#troubleshooting)
10. [Desarrollo](#desarrollo)

---

## ⚡ Instalación Rápida

### Requisitos
- **Python 3.10+** (recomendado 3.11 o 3.12)
- **pip** o **conda** para gestión de paquetes
- Navegador moderno (Chrome, Firefox, Edge)

### Paso 1: Instalar Dependencias

```bash
cd c:\Users\harry\PolibitHackatonbob
pip install -r requirements.txt
```

**Dependencias incluidas:**
- `flask==3.0.0` - Servidor web y API REST
- `flask-cors==4.0.0` - CORS para llamadas Cross-Origin
- `networkx==3.2.1` - Procesamiento de grafos
- `matplotlib>=3.10.0` - Visualización de gráficas
- `ibm-watsonx-ai` - Integración con watsonx.ai
- `python-dotenv` - Gestión de variables de entorno

### Paso 2: Arrancar el Servidor

```bash
python src/servidor_paso1_web.py
```

**Salida esperada:**
```
======================================================================
🚀 SERVIDOR OptiCode QA — PASO 1 REAL
======================================================================

📁 Flujo: Bob IDE (manual) → Motor Local → watsonx.ai
🌐 Dashboard disponible en: http://localhost:5000

🔗 API Endpoints:
   GET  /api/bob-sessions - Lista análisis de Bob IDE
   GET  /api/codigos - Lista códigos disponibles
   POST /api/ejecutar-benchmarks - Ejecuta benchmarks
   POST /api/integrar-watsonx - Integra y genera reporte
   GET  /api/reportes - Lista reportes finales
   GET  /api/estado - Estado del sistema

======================================================================
* Running on http://localhost:5000
Press CTRL+C to quit
```

### Paso 3: Abrir el Dashboard

Abre en tu navegador:
```
http://localhost:5000
```

---

## 🖥️ Uso del Dashboard Web

### 1️⃣ Interfaz Principal

El dashboard tiene 3 secciones principales:

```
┌──────────────────────────────────────────────────────────┐
│  OptiCode QA — Panel del Auditor                         │
│  Panel del auditor | Teoría y práctica en una sola superficie
└──────────────────────────────────────────────────────────┘
        │
        ├─→ 📊 Análisis Bob IDE (selector de análisis previos)
        │
        ├─→ 💻 Código a Analizar (selector de código fuente)
        │
        ├─→ ⚙️ Acciones (botones de ejecución)
        │
        ├─→ ℹ️ Estado (alertas detectadas)
        │
        └─→ 📈 Resultados (gráficas, tablas, métricas)
```

### 2️⃣ Flujo de Trabajo Paso a Paso

#### **Opción A: Usar Análisis Bob IDE Existente**

1. **Seleccionar análisis:**
   - Dropdown: "Seleccionar análisis…"
   - Elige un archivo `.md` de `output/informesbob/`
   - El contenido se carga automáticamente

2. **Seleccionar código:**
   - Dropdown: "Seleccionar archivo…"
   - Elige el código correspondiente
   - Confirma la selección

3. **Ejecutar benchmarks:**
   - Clic: "⚡ EJECUTAR"
   - El sistema mide tiempo y memoria
   - Espera 10-30 segundos

4. **Ver resultados:**
   - Gráficas de tiempo y memoria
   - Tabla de métricas detalladas
   - Alertas automáticas (si hay problemas)

5. **Descargar PDF:**
   - Clic: "📥 Descargar PDF"
   - Se descarga reporte completo

#### **Opción B: Analizar Código Personalizado**

1. **Pegar código:**
   - Área: "Código personalizado"
   - Paste tu código Python aquí
   - El análisis es automático

2. **Ver análisis estático:**
   - Complejidad estimada (O notation)
   - Cuellos de botella identificados
   - Recomendaciones de optimización

### 3️⃣ Componentes del Dashboard

#### **📊 Análisis Bob IDE**
- Muestra análisis cargados desde `output/informesbob/`
- Contiene análisis teórico de complejidad
- Generados por IBM Bob IDE (simulados o reales)

#### **💻 Código a Analizar**
- Selector de archivos `.py` disponibles
- Muestra preview del código
- Confirma la selección antes de ejecutar

#### **⚙️ Acciones**
- **⚡ EJECUTAR:** Inicia benchmarks locales
- **📥 Descargar PDF:** Exporta reporte (con datos)
- **🔗 Integrar watsonx:** Envía análisis a AI

#### **ℹ️ Estado**
- Número de alertas detectadas
- Estado del sistema
- Información de conexión

#### **📈 Análisis de Rendimiento**
Tres gráficas interactivas:
- **Tiempo de Ejecución (ms):** Crecimiento temporal por tamaño N
- **Consumo de Memoria (MB):** Crecimiento de memoria por tamaño N
- **Proyección de concurrencia crítica:** Predicción con múltiples instancias

#### **📊 Métricas Detalladas**
Tabla con columnas:
- Tamaño (N)
- DFS (ms) / Tiempo del algoritmo
- LDFS (ms) / Variante alternativa
- IDFS (ms) / Variante iterativa
- Mem DFS (MB) / Memoria pico

#### **⚠️ Alertas**
- **COMPLEJIDAD_ALTA:** Crecimiento no lineal detectado
- **TIEMPO_CRITICO:** Supera 1 segundo
- **MEMORIA_ALTA:** Consumo > 100 MB
- **COMPLEJIDAD_ESTIMADA:** Predicción O(N²), O(N³), etc

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ WEB (HTML)                      │
│              templates/dashboard.html                       │
│                                                             │
│  - 📊 Análisis de Bob IDE (selector)                       │
│  - 💻 Código a Analizar (textarea)                         │
│  - ⚡ Benchmarks (gráficas + tabla)                        │
│  - 📈 Alertas automáticas                                  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP REST API (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 SERVIDOR FLASK (Python)                     │
│              src/servidor_paso1_web.py                      │
│                                                             │
│  Endpoints:                                                │
│  - GET  /api/bob-sessions           ← Lee análisis        │
│  - GET  /api/codigos                ← Lista código        │
│  - POST /api/ejecutar-benchmarks    ← Corre benchmarks    │
│  - POST /api/integrar-watsonx       ← Integra IA         │
│  - GET  /api/reportes               ← Lista reportes     │
│  - GET  /api/estado                 ← Sistema status     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐   ┌──────────┐   ┌─────────────┐
    │  Motor  │   │    Bob   │   │  Integrador │
    │   QA    │   │ Simulator│   │  watsonx.ai │
    │         │   │          │   │             │
    │motor_qa │   │(futuro)  │   │integrador_  │
    │  .py    │   │          │   │watsonx.py   │
    └────┬────┘   └──────────┘   └─────────────┘
         │
         └─→ Mide: tiempo (ms) + memoria (bytes)
         └─→ Lee: data/grafos_prueba.json
         └─→ Escribe: data/metricas_salida.json
```

### Flujo de Datos

```
1. USUARIO carga análisis de Bob
   └─→ GET /api/bob-sessions
   └─→ Lee: output/informesbob/*.md

2. USUARIO selecciona código
   └─→ GET /api/codigos
   └─→ Lee: src/*.py

3. USUARIO ejecuta benchmarks
   └─→ POST /api/ejecutar-benchmarks
   └─→ motor_qa.py mide tiempo y memoria
   └─→ Escribe: data/metricas_salida.json
   └─→ JSON devuelto al frontend

4. USUARIO integra watsonx (opcional)
   └─→ POST /api/integrar-watsonx
   └─→ integrador_watsonx.py envía datos
   └─→ Genera: output/REPORTE_FINAL_QA.md

5. USUARIO descarga reporte
   └─→ GET /api/reportes
   └─→ Lee: output/REPORTE_FINAL_QA.md
```

---

## 📁 Estructura de Carpetas

```
PolibitHackatonbob/
│
├── 🚀 RAÍZ (Configuración y ejecución)
│   ├── README.md                 ← ESTE ARCHIVO (documentación consolidada)
│   ├── requirements.txt          ← Dependencias de pip
│   ├── .env                      ← Credenciales (NO en git)
│   ├── .gitignore               ← Archivos ignorados
│   ├── LOGOQA.png               ← Logo del proyecto
│   ├── skills-lock.json         ← Configuración de skills
│   └── PolibitHackatonbob.code-workspace ← Workspace VS Code
│
├── 📁 src/                       ← 🐍 CÓDIGO FUENTE DEL SISTEMA
│   ├── __init__.py              ← Init package
│   ├── servidor_paso1_web.py    ← 🌐 Servidor Flask + API REST (PRINCIPAL)
│   ├── motor_qa.py              ← ⚡ Motor de benchmarks (mide tiempo + memoria)
│   ├── integrador_watsonx.py    ← 🤖 Conexión a watsonx.ai
│   ├── algoritmos.py            ← 📋 Ejemplos de algoritmos
│   ├── PolibitHackatonbob.code-workspace ← Workspace (backup)
│   └── [otros archivos .py según sea necesario]
│
├── 📁 data/                      ← 📊 DATOS DE ENTRADA Y MÉTRICAS
│   ├── grafos_prueba.json       ← 📥 Grafo de prueba (entrada)
│   ├── metricas_salida.json     ← 📤 Benchmarks (salida automática)
│   └── [otros datos según sea necesario]
│
├── 📁 output/                    ← 📄 REPORTES FINALES Y ANÁLISIS
│   ├── REPORTE_FINAL_QA.md      ← 🎯 Reporte maestro (teoría + práctica + IA)
│   └── informesbob/             ← 📝 Análisis teóricos de Bob IDE
│       ├── ANALISIS_RENDIMIENTO_ALGORITMOS_BUSQUEDA.md
│       ├── [otros análisis .md]
│       └── [capturas .png si existen]
│
├── 📁 templates/                 ← 🌐 INTERFAZ WEB
│   └── dashboard.html           ← 💻 Dashboard web interactivo
│
└── 📁 [ELIMINADAS - Ver abajo]
    ├── ❌ bob_sessions/         ← Histórico (consolidado en docs)
    ├── ❌ frontend/             ← Redundante (existe templates/)
    └── ❌ output/diagramas/     ← No se usa en flujo actual
```

### 📝 Propósito de Cada Carpeta

#### `src/` — Código Fuente
Contiene toda la lógica del sistema:
- **servidor_paso1_web.py** (PRINCIPAL): Servidor Flask con API REST
- **motor_qa.py**: Ejecuta benchmarks, mide tiempo y memoria
- **integrador_watsonx.py**: Conexión a IBM watsonx.ai
- **algoritmos.py**: Ejemplos de algoritmos a analizar

#### `data/` — Datos
- **Entrada**: `grafos_prueba.json` (datos para benchmarks)
- **Salida**: `metricas_salida.json` (resultados auto-generados)

#### `output/` — Reportes
- **REPORTE_FINAL_QA.md**: Reporte completo (consolidado)
- **informesbob/**: Análisis teóricos de Bob IDE (uno por algoritmo)

#### `templates/` — Interfaz Web
- **dashboard.html**: Página web con todas las funcionalidades

---

## 🔄 Flujo PASO 1 Completo

### 📊 El flujo tiene 3 etapas principales:

```
ETAPA 1: ANÁLISIS TEÓRICO (Bob IDE)
↓
Ubicación: output/informesbob/*.md

Tú o IBM Bob IDE generan:
- Análisis de complejidad Big-O
- Cuellos de botella identificados
- Recomendaciones de optimización

Salida:
✅ output/informesbob/bob_analisis_[algoritmo].md


ETAPA 2: BENCHMARKS PRÁCTICOS (Motor Local)
↓
Ubicación: motor_qa.py → data/metricas_salida.json

Sistema ejecuta automáticamente:
1. Lee: data/grafos_prueba.json (datos de prueba)
2. Ejecuta algoritmo con N = 10, 100, 1000, 5000
3. Mide tiempo (ms) y memoria (bytes)
4. Repite 3 veces por tamaño (promedio)
5. Guarda resultados: data/metricas_salida.json

Ejemplo de salida:
{
  "benchmarks": {
    "10": {
      "time_ms_mean": 0.15,
      "time_ms_samples": [0.14, 0.16, 0.15],
      "mem_bytes_peak_mean": 2400,
      "mem_bytes_peak_samples": [2400, 2400, 2400]
    },
    "100": { "time_ms_mean": 1.52, ... },
    "1000": { "time_ms_mean": 15.2, ... },
    "5000": { "time_ms_mean": 152, ... }
  }
}

Salida:
✅ data/metricas_salida.json


ETAPA 3: INTEGRACIÓN Y REPORTE FINAL (watsonx.ai)
↓
Ubicación: integrador_watsonx.py → output/REPORTE_FINAL_QA.md

Sistema integra:
1. Lee: output/informesbob/*.md (análisis teórico)
2. Lee: data/metricas_salida.json (benchmarks prácticos)
3. Envía a watsonx.ai para análisis IA
4. watsonx compara teoría vs práctica
5. Genera recomendaciones
6. Consolida en reporte final

Contenido del reporte:
- Resumen ejecutivo
- Análisis teórico (de Bob)
- Métricas prácticas (del motor)
- Comparación teoría vs práctica
- Alertas automáticas
- Recomendaciones finales
- Coste estimado (si watsonx lo calcula)

Salida:
✅ output/REPORTE_FINAL_QA.md
```

---

## 🔌 API REST

### Endpoints Disponibles

#### **Listar Análisis de Bob IDE**
```bash
GET /api/bob-sessions

Response:
{
  "success": true,
  "total": 3,
  "archivos": [
    {
      "nombre": "bob_analisis_dfs.md",
      "contenido_preview": "# Análisis DFS...",
      "tamaño": 2500,
      "tipo": "Bob IDE Analysis"
    },
    ...
  ]
}
```

#### **Obtener Análisis Completo**
```bash
GET /api/bob-sessions/<nombre>

Example:
GET /api/bob-sessions/ANALISIS_RENDIMIENTO_ALGORITMOS_BUSQUEDA.md

Response:
{
  "success": true,
  "nombre": "ANALISIS_RENDIMIENTO_ALGORITMOS_BUSQUEDA.md",
  "contenido": "[contenido completo del .md]"
}
```

#### **Listar Códigos Disponibles**
```bash
GET /api/codigos

Response:
{
  "success": true,
  "total": 5,
  "archivos": [
    {
      "nombre": "motor_qa.py",
      "ruta": "src/motor_qa.py",
      "contenido_preview": "# Motor de benchmarks..."
    },
    ...
  ]
}
```

#### **Obtener Código Completo**
```bash
GET /api/codigos/<nombre>

Example:
GET /api/codigos/motor_qa.py

Response:
{
  "success": true,
  "nombre": "motor_qa.py",
  "contenido": "[código completo]"
}
```

#### **Ejecutar Benchmarks**
```bash
POST /api/ejecutar-benchmarks

Request (opcional - usa datos por defecto):
{
  "codigo": "def dfs(graph, start): ...",
  "nombre_archivo": "algoritmos.py",
  "grafo_path": "data/grafos_prueba.json"
}

Response:
{
  "success": true,
  "mensaje": "✅ Benchmarks completados exitosamente",
  "metricas": {
    "10": {
      "n": 10,
      "time_ms": 0.15,
      "memory_mb": 2.4,
      "samples_time": [0.14, 0.16, 0.15],
      "samples_memory": [2.4, 2.4, 2.4]
    },
    ...
  },
  "alertas": [
    {
      "tipo": "COMPLEJIDAD_ESTIMADA",
      "nivel": "info",
      "icono": "📊",
      "mensaje": "Complejidad estimada: O(N²)",
      "ratio": 2.8
    }
  ],
  "resumen_analisis": { ... },
  "timestamp": "2026-05-17T14:30:00"
}
```

#### **Integrar con watsonx.ai**
```bash
POST /api/integrar-watsonx

Request:
{
  "bob_analysis_file": "ANALISIS_RENDIMIENTO_ALGORITMOS_BUSQUEDA.md",
  "codigo": "def dfs(graph, start): ..."
}

Response:
{
  "success": true,
  "mensaje": "✅ Integración completada exitosamente",
  "archivo_reporte": "/ruta/a/REPORTE_FINAL_QA.md",
  "resumen_watsonx": "[resumen del análisis IA]"
}
```

#### **Listar Reportes**
```bash
GET /api/reportes

Response:
{
  "success": true,
  "total": 1,
  "reportes": [
    {
      "nombre": "REPORTE_FINAL_QA.md",
      "contenido_preview": "# 📊 REPORTE FINAL QA...",
      "tamaño": 5000
    }
  ]
}
```

#### **Descargar Reporte Específico**
```bash
GET /api/reportes/<nombre>

Example:
GET /api/reportes/REPORTE_FINAL_QA.md

Response:
{
  "success": true,
  "nombre": "REPORTE_FINAL_QA.md",
  "contenido": "[reporte completo en markdown]"
}
```

#### **Estado del Sistema**
```bash
GET /api/estado

Response:
{
  "success": true,
  "sistema": "OptiCode QA — PASO 1 Real",
  "estado": "✅ Operacional",
  "archivos_bob": 3,
  "reportes_generados": 1,
  "metricas_disponibles": true,
  "timestamp": "2026-05-17T14:30:00"
}
```

---

## 📊 Archivos Generados

### 📥 Entrada (Manual)

#### `data/grafos_prueba.json`
Grafo de prueba para algoritmos de búsqueda.

```json
{
  "A": ["B", "C", "D"],
  "B": ["E", "F"],
  "C": ["G", "H", "I"],
  "D": ["J"],
  "E": [],
  "F": ["K"],
  "G": [],
  "H": [],
  "I": [],
  "J": [],
  "K": []
}
```

#### `output/informesbob/*.md`
Análisis generados por Bob IDE (o simulados).

Ejemplo `ANALISIS_RENDIMIENTO_ALGORITMOS_BUSQUEDA.md`:
```markdown
# Análisis de Rendimiento: Algoritmos de Búsqueda

## DFS (Depth-First Search)
- **Complejidad Teórica:** O(V + E)
- **Cuellos de Botella:**
  - Línea 15: búsqueda lineal en lista
  - Línea 22: operación de diccionario anidado

## BFS (Breadth-First Search)
- **Complejidad Teórica:** O(V + E)
- **Cuellos de Botella:**
  - Línea 8: deque append (O(1) pero overhead)

## Recomendaciones
1. Usar defaultdict en lugar de if-checks
2. Precalcular índices
3. Usar sets para búsquedas O(1)
```

### 📤 Salida Automática

#### `data/metricas_salida.json`
Generado por `motor_qa.py` después de ejecutar benchmarks.

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
      "time_ms_samples": [1.50, 1.54, 1.52],
      "mem_bytes_peak_mean": 24000,
      "mem_bytes_peak_samples": [24000, 24000, 24000]
    },
    "1000": {
      "time_ms_mean": 15.2,
      "time_ms_samples": [15.0, 15.4, 15.2],
      "mem_bytes_peak_mean": 240000,
      "mem_bytes_peak_samples": [240000, 240000, 240000]
    },
    "5000": {
      "time_ms_mean": 152,
      "time_ms_samples": [150, 154, 152],
      "mem_bytes_peak_mean": 2400000,
      "mem_bytes_peak_samples": [2400000, 2400000, 2400000]
    }
  }
}
```

#### `output/REPORTE_FINAL_QA.md`
Reporte consolidado final.

```markdown
# 📊 REPORTE FINAL QA — OptiCode

## 🔍 Análisis de Bob IDE
[Contenido del análisis teórico]

---

## ⚡ Métricas Prácticas (Motor Local)

```json
[Contenido de metricas_salida.json]
```

---

## 🤖 Resumen de watsonx.ai
[Análisis IA y recomendaciones]

---

## 📈 Conclusiones
- Teoría vs Práctica: ±5% divergencia
- Complejidad validada: O(V + E)
- Optimizaciones recomendadas: 3 críticas, 2 menores
- Coste estimado en cloud: $0.12/millón ops

---

**Generado automáticamente por OptiCode QA**
**Fecha:** 2026-05-17T14:30:00
```

---

## 📈 Interpretación de Resultados

### Cálculo de Complejidad

#### Patrón de Crecimiento

```
Tamaño (N)      Tiempo (ms)     Ratio
10              0.15            ×1
100             1.52            ×10.1  (casi lineal)
1000            15.2            ×10.0  (casi lineal)
5000            152             ×10.0  (casi lineal)

Conclusión: O(N) — Complejidad lineal
```

#### Ejemplos de Ratios por Big-O

```
O(1) - Constante:
  N=10 → 0.1ms, N=100 → 0.1ms, N=1000 → 0.1ms
  Ratio: ~1x

O(log N) - Logarítmica:
  N=10 → 0.1ms, N=100 → 0.15ms, N=1000 → 0.22ms
  Ratio: ~1.5-2x

O(N) - Lineal:
  N=10 → 0.1ms, N=100 → 1.0ms, N=1000 → 10ms
  Ratio: ~10x

O(N log N) - Lineal-logarítmica:
  N=10 → 0.2ms, N=100 → 2.5ms, N=1000 → 40ms
  Ratio: ~15-20x

O(N²) - Cuadrática:
  N=10 → 0.1ms, N=100 → 10ms, N=1000 → 1000ms (1s)
  Ratio: ~100x

O(N³) - Cúbica:
  N=10 → 0.1ms, N=100 → 1000ms (1s), N=1000 → 1M ms (1000s)
  Ratio: ~1000x
```

### Alertas Automáticas

El sistema detecta automáticamente:

#### **COMPLEJIDAD_ALTA** ⚠️
Cuando el tiempo crece mucho más que lo esperado:
```
Ejemplo: N=100→1000 debería crecer 10x
Pero el tiempo crece 100x → Alerta
```

#### **TIEMPO_CRITICO** 🔴
Cuando el tiempo supera 1 segundo:
```
N=5000 tarda 1200ms → Error crítico
Algoritmo no es viable para datos grandes
```

#### **MEMORIA_ALTA** 💾
Cuando la memoria supera 100 MB:
```
Pico de memoria: 256 MB → Alerta
Algoritmo usa demasiados recursos
```

#### **COMPLEJIDAD_ESTIMADA** 📊
Predicción de Big-O basada en ratios:
```
Ratio promedio: 2.8x → Probablemente O(N log N)
Ratio promedio: 10.5x → Probablemente O(N²)
Ratio promedio: 100x → Probablemente O(N³)
```

---

## 🔧 Troubleshooting

### ❌ Servidor no arranca

**Error:** `Address already in use`
```bash
# Solución: el puerto 5000 está ocupado
# Opción 1: Matar proceso
taskkill /PID <pid> /F

# Opción 2: Cambiar puerto en código
# Editar servidor_paso1_web.py última línea:
# app.run(debug=True, host='localhost', port=5001)
```

### ❌ No aparecen análisis de Bob

**Verificar:**
```bash
# 1. Carpeta exists:
dir output\informesbob\

# 2. Archivos .md existen:
dir output\informesbob\*.md

# 3. Si no hay, crear ejemplo:
echo # Análisis Test > output\informesbob\test_analisis.md
```

### ❌ Benchmarks lentos

**Causa:** Tamaños de prueba muy grandes

**Solución:** Editar `src/motor_qa.py`
```python
# Buscar esta línea:
SIZES = [10, 100, 1000, 5000]

# Cambiar a:
SIZES = [10, 100, 500]  # Menos tamaños = más rápido
```

### ❌ Falta módulo (ej: `flask`)

```bash
# Reinstalar dependencias:
pip install --upgrade -r requirements.txt

# O instalar individual:
pip install flask==3.0.0
```

### ❌ No se genera `metricas_salida.json`

**Verificar:**
```bash
# 1. Carpeta data/ existe:
dir data\

# 2. motor_qa.py tiene permisos:
python src/motor_qa.py

# 3. Si hay error, mostrar:
python src/motor_qa.py 2>&1
```

---

## 🛠️ Desarrollo

### Agregar Nuevo Algoritmo

1. **Crear archivo en `src/`:**
   ```python
   # src/mi_algoritmo.py
   
   def mi_busqueda(graph, start):
       """Mi algoritmo de búsqueda."""
       visited = set()
       queue = [start]
       
       while queue:
           node = queue.pop(0)
           if node not in visited:
               visited.add(node)
               queue.extend(graph[node])
       
       return visited
   ```

2. **Registrar en `motor_qa.py`:**
   ```python
   # Agregar a la lista de funciones a benchmarkear
   ALGORITMOS = {
       'mi_busqueda': (src.mi_algoritmo.mi_busqueda, None)
   }
   ```

3. **Crear análisis en Bob IDE:**
   - Abrir VS Code con Bob IDE
   - Cargar `src/mi_algoritmo.py`
   - Solicitar análisis Big-O
   - Guardar como `output/informesbob/bob_analisis_mi_busqueda.md`

4. **Ejecutar benchmarks:**
   ```bash
   python src/motor_qa.py
   ```

5. **Ver en dashboard:**
   - Abre http://localhost:5000
   - Selecciona tu análisis en el dropdown
   - Ejecuta

### Modificar Tamaños de Prueba

**Archivo:** `src/motor_qa.py`
```python
# Buscar:
SIZES = [10, 100, 1000, 5000]

# Cambiar a:
SIZES = [5, 20, 50, 200, 1000]  # Para pruebas rápidas
# O:
SIZES = [100, 1000, 5000, 10000, 50000]  # Para análisis exhaustivo
```

### Cambiar Puerto del Servidor

**Archivo:** `src/servidor_paso1_web.py`
```python
# Última línea:
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    # Cambiar 5000 al puerto deseado
```

### Agregar Credenciales watsonx.ai

1. **Crear `.env`:**
   ```
   WATSONX_API_KEY=tu_api_key_aqui
   WATSONX_PROJECT_ID=tu_project_id
   ```

2. **Usar en `integrador_watsonx.py`:**
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv('WATSONX_API_KEY')
   ```

### Estructura de un Análisis Bob IDE

```markdown
# Análisis de Complejidad: [Nombre Algoritmo]

## Función Analizada
```python
[código]
```

## Complejidad Teórica
- **Tiempo:** O(...)
- **Espacio:** O(...)

## Cuellos de Botella
1. Línea X: descripción
2. Línea Y: descripción

## Recomendaciones
1. Recomendación 1
2. Recomendación 2

---
*Generado por IBM Bob IDE - [timestamp]*
```

---

## 📚 Referencia Rápida

### Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Arrancar servidor
python src/servidor_paso1_web.py

# Ejecutar benchmarks manualmente
python src/motor_qa.py

# Ver estado del sistema
curl http://localhost:5000/api/estado

# Listar análisis disponibles
curl http://localhost:5000/api/bob-sessions

# Listar código disponible
curl http://localhost:5000/api/codigos

# Ejecutar benchmarks vía API
curl -X POST http://localhost:5000/api/ejecutar-benchmarks

# Ver reporte final
curl http://localhost:5000/api/reportes
```

### Variables de Entorno (`.env`)

```
# watsonx.ai
WATSONX_API_KEY=xxxxx
WATSONX_PROJECT_ID=xxxxx

# Flask
FLASK_DEBUG=True
FLASK_PORT=5000

# Sistema
LOG_LEVEL=INFO
```

### Estructura de un Reporte

```markdown
# 📊 REPORTE FINAL QA

## Ejecutivo
- Algoritmo: [nombre]
- Complejidad Teórica: O(...)
- Complejidad Práctica: O(...)
- Divergencia: ±X%
- Estado: ✅ OPTIMIZADO

## 1. Análisis Teórico
[Contenido de Bob IDE]

## 2. Métricas Prácticas
[Tabla y gráficas]

## 3. Comparación
[Análisis de diferencias]

## 4. Alertas
[Problemas detectados]

## 5. Recomendaciones
[Optimizaciones propuestas]
```

---

## 📞 Soporte

Si tienes problemas:

1. **Verifica la instalación:**
   ```bash
   pip list | findstr flask
   ```

2. **Revisa los logs:**
   ```bash
   # Terminal donde corre el servidor
   # Habrá errores detallados aquí
   ```

3. **Lee README_PASO1.md** en cada carpeta para detalles específicos

4. **Verifica permisos** de carpetas `output/`, `data/`

---

## 📄 Licencia

Proyecto de Polibit Hackathon 2026.

---

**Última actualización:** 17 de Mayo de 2026  
**Versión:** 1.0 — Sistema completo  
**Estado:** ✅ Producción
