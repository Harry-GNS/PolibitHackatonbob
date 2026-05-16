# 🌐 OptiCode QA — Web Dashboard

## 🚀 Cómo Iniciar

### Opción 1: Script automático (Recomendado)
```bash
python iniciar_web.py
```
- ✅ Inicia automáticamente Flask
- ✅ Abre navegador en http://localhost:5000
- ✅ Muestra logs en terminal

### Opción 2: Directamente con Python
```bash
python src/servidor_paso1_web.py
```

### Opción 3: Con Flask CLI
```bash
set FLASK_APP=src/servidor_paso1_web.py
flask run
```

---

## 🎯 Flujo de Uso

### 1️⃣ Página Principal
```
┌─────────────────────────────────────────────┐
│  OptiCode QA — PASO 1 Real                  │
│  Bob IDE (manual) → Motor Local → watsonx   │
└─────────────────────────────────────────────┘

┌─ SIDEBAR ─────┬─────── ANÁLISIS ─────────┬─────── LOG ──────┐
│ Entradas:     │ Teoría de Bob            │ Ejecución       │
│               │ [textarea]               │ [consola]       │
│ • Bob Analysis│                          │                 │
│ • Código      │ ⚡ Benchmarks Prácticos  │                 │
│ • Credenciales│ [tabla de resultados]    │                 │
│               │                          │                 │
│ Acciones:     │                          │                 │
│ • Benchmarks  │                          │                 │
│ • Integrar    │                          │                 │
│ • Reporte     │                          │                 │
└───────────────┴──────────────────────────┴─────────────────┘
```

### 2️⃣ Paso a Paso

#### A. Cargar análisis de Bob IDE
1. Clic en dropdown "Análisis Bob IDE"
2. Selecciona archivo `.md` de bob_sessions/
3. Se carga automáticamente en el textarea

#### B. Seleccionar código
1. Clic en dropdown "Código Fuente"
2. Selecciona algoritmo (dfs, bubble_sort, etc)
3. Se muestra la confirmación

#### C. Ejecutar benchmarks
1. Clic en botón "⚡ Ejecutar Benchmarks"
2. Espera a que se complete
3. Ver tabla con resultados de tiempo y memoria

#### D. Integrar con watsonx.ai
1. Clic en "✓ Verificar Credenciales"
2. Clic en "🔗 Integrar watsonx"
3. Sistema genera REPORTE_FINAL_QA.md

#### E. Ver reporte final
1. Clic en "📄 Ver Reporte Final"
2. Se abre en pestaña nueva
3. Contiene análisis + métricas + recomendaciones

---

## 🎨 Diseño Corporativo

### Tipografía
- ✅ Monoespaciada: JetBrains Mono (Google Fonts)
- ✅ Todos los elementos usan la misma fuente
- ✅ Títulos en MAYÚSCULAS con letter-spacing

### Paleta de Colores
```
Fondo:         #FFFFFF (blanco puro)
Secundario:    #F4F6F8 (gris ultra claro)
Texto:         #161616 (gris muy oscuro)
Acento:        #0F62FE (azul IBM)
Alerta:        #E66000 (naranja industrial)
Error:         #DA1E28 (rojo corporativo)
```

### Componentes
- ✅ Bordes finos (1px) gris claro
- ✅ Esquinas sutiles (4px border-radius)
- ✅ Sombras difusas solo en paneles
- ✅ Tablas con zebrastripe (#FAFAFB)
- ✅ Botones planos, sin gradientes

---

## 📊 API Endpoints

```bash
# Ver análisis de Bob IDE
GET /api/bob-sessions

# Obtener análisis específico
GET /api/bob-sessions/<nombre>

# Listar códigos disponibles
GET /api/codigos

# Obtener código específico
GET /api/codigos/<nombre>

# Ejecutar benchmarks locales
POST /api/ejecutar-benchmarks

# Integrar con watsonx.ai
POST /api/integrar-watsonx

# Listar reportes generados
GET /api/reportes

# Obtener reporte específico
GET /api/reportes/<nombre>

# Estado del sistema
GET /api/estado
```

---

## 🔧 Troubleshooting

### ❌ "Port 5000 already in use"
```bash
# Cambia el puerto en src/servidor_paso1_web.py
# Línea: app.run(debug=True, host='localhost', port=5001)
```

### ❌ "Template not found"
```bash
# Verifica que templates/dashboard.html existe
ls templates/
```

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
# Instala dependencias
pip install -r requirements.txt
```

### ❌ "Cannot find bob_sessions/"
```bash
# Crea la carpeta manualmente y añade archivo .md
mkdir bob_sessions
# Luego copia algún .md ahí
```

---

## 📁 Estructura Esperada

```
PolibitHackatonbob/
├── templates/
│   └── dashboard.html          ← Interfaz web
├── src/
│   ├── servidor_paso1_web.py   ← Servidor Flask
│   ├── motor_qa.py
│   └── ...
├── bob_sessions/
│   ├── bob_analisis_*.md       ← Tus análisis
│   └── ...
├── data/
│   ├── metricas_salida.json    ← Benchmarks (generado)
│   └── grafos_prueba.json
├── output/
│   └── REPORTE_FINAL_QA.md     ← Reporte final
└── iniciar_web.py              ← Script para iniciar
```

---

## ⌚ Tiempo de Ejecución

- Cargar análisis: < 1 segundo
- Ejecutar benchmarks: 30-60 segundos (3 repeticiones × 4 tamaños)
- Integración watsonx.ai: 5-10 segundos

---

## 🎓 Próximos Pasos

1. **Análisis en Bob IDE:**
   - Abre VS Code con Bob IDE
   - Analiza un algoritmo (DFS, bubble sort, etc)
   - Exporta `.md` a bob_sessions/

2. **Ejecutar web:**
   ```bash
   python iniciar_web.py
   ```

3. **Usar interfaz:**
   - Selecciona análisis de Bob
   - Selecciona código para benchmarks
   - Ejecuta y ve resultados en tiempo real

---

## 💡 Tips Profesionales

- ✅ Guarda el URL en favoritos: http://localhost:5000
- ✅ Usa F12 (DevTools) para ver logs en consola
- ✅ Commit los .md de Bob en git (son evidencia oficial)
- ✅ NO hagas commit de metricas_salida.json (se regenera)
- ✅ Captura pantallas del dashboard para la presentación
