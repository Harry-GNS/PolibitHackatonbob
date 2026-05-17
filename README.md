# 📊 OptiCode QA — PASO 1 (Polibit Hackathon 2026)

**Sistema integrado para auditoría automática de rendimiento y complejidad de código Python.**

---

## 🎯 Descripción General

OptiCode QA automatiza el análisis de algoritmos combinando:
- **Análisis teórico** (complejidad Big-O)
- **Benchmarks prácticos** (tiempo y memoria real)
- **Comparación teoría vs práctica**
- **Reportes automáticos** (Markdown + JSON)
- **Dashboard web interactivo**
- **Integración watsonx.ai**

---

## ⚡ Instalación Rápida

### Requisitos
- Python 3.10+
- Navegador moderno

### Instalación

```bash
cd c:\Users\harry\PolibitHackatonbob
pip install -r requirements.txt
python src/servidor_paso1_web.py
```

Abre: `http://localhost:5000`

---

## 🖥️ Uso del Dashboard

### Flujo de Trabajo

1. **Seleccionar análisis Bob IDE** → Dropdown con archivos `.md`
2. **Seleccionar código** → Dropdown con archivos `.py`
3. **Ejecutar benchmarks** → Botón "⚡ EJECUTAR"
4. **Ver resultados** → Gráficas, métricas y alertas
5. **Descargar reporte** → Botón "📥 Descargar PDF"

### Componentes Principales

- **📊 Análisis Bob IDE:** Análisis teórico de complejidad
- **💻 Código:** Selector de archivos Python
- **📈 Resultados:** Gráficas de tiempo/memoria
- **⚠️ Alertas:** Detección automática de problemas

---

## 🏗️ Arquitectura del Sistema

```
Dashboard (HTML) → Flask API → Motor QA + watsonx.ai
                              ↓
                    data/metricas_salida.json
                    output/REPORTE_FINAL_QA.md
```

---

## 📁 Estructura

```
PolibitHackatonbob/
├── src/
│   ├── servidor_paso1_web.py    ← Servidor Flask + API
│   ├── motor_qa.py              ← Benchmarks
│   └── integrador_watsonx.py    ← Integración IA
├── data/
│   ├── grafos_prueba.json       ← Entrada
│   └── metricas_salida.json     ← Salida
├── output/
│   ├── REPORTE_FINAL_QA.md      ← Reporte final
│   └── informesbob/             ← Análisis Bob IDE
└── templates/
    └── dashboard.html           ← Interfaz web
```

---

## 🔄 Flujo PASO 1

**3 Etapas:**

1. **Análisis Teórico** → Bob IDE genera `output/informesbob/*.md`
2. **Benchmarks** → Motor QA mide tiempo/memoria → `data/metricas_salida.json`
3. **Reporte Final** → watsonx.ai integra todo → `output/REPORTE_FINAL_QA.md`

---

## 🔌 API REST

**Endpoints principales:**

- `GET /api/bob-sessions` - Lista análisis Bob IDE
- `GET /api/codigos` - Lista códigos disponibles
- `POST /api/ejecutar-benchmarks` - Ejecuta benchmarks
- `POST /api/integrar-watsonx` - Integra con IA
- `GET /api/reportes` - Lista reportes
- `GET /api/estado` - Estado del sistema

---

## 📊 Interpretación de Resultados

### Complejidad por Ratio de Crecimiento

```
O(1):      Ratio ~1x
O(log N):  Ratio ~1.5-2x
O(N):      Ratio ~10x
O(N²):     Ratio ~100x
O(N³):     Ratio ~1000x
```

### Alertas

- **COMPLEJIDAD_ALTA:** Crecimiento no lineal
- **TIEMPO_CRITICO:** > 1 segundo
- **MEMORIA_ALTA:** > 100 MB

---

## 🔧 Troubleshooting

**Puerto ocupado:**
```bash
taskkill /PID <pid> /F
# O cambiar puerto en servidor_paso1_web.py
```

**Sin análisis Bob:**
```bash
dir output\informesbob\*.md
```

**Benchmarks lentos:**
```python
# Editar motor_qa.py
SIZES = [10, 100, 500]  # Reducir tamaños
```

**Falta módulo:**
```bash
pip install -r requirements.txt
```

---

## 🛠️ Desarrollo

### Agregar Nuevo Algoritmo

1. Crear `src/mi_algoritmo.py`
2. Registrar en `motor_qa.py`
3. Generar análisis Bob IDE → `output/informesbob/`
4. Ejecutar: `python src/motor_qa.py`

### Configuración

**Tamaños de prueba** (`motor_qa.py`):
```python
SIZES = [10, 100, 1000, 5000]
```

**Puerto servidor** (`servidor_paso1_web.py`):
```python
app.run(debug=True, host='localhost', port=5000)
```

**Credenciales watsonx** (`.env`):
```
WATSONX_API_KEY=xxxxx
WATSONX_PROJECT_ID=xxxxx
```

---

## 📚 Comandos Útiles

```bash
pip install -r requirements.txt
python src/servidor_paso1_web.py
python src/motor_qa.py
curl http://localhost:5000/api/estado
```

---

## 📄 Licencia

Proyecto de Polibit Hackathon 2026.

---

**Última actualización:** 17 de Mayo de 2026  
**Versión:** 1.0 — Sistema completo  
**Estado:** ✅ Producción
