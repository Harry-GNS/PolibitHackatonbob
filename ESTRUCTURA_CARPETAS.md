# 📂 Estructura de Carpetas — OptiCode QA PASO 1

## 🎯 Resumen Visual

```
PolibitHackatonbob/
│
├── 📁 bob_sessions/              ← 📝 ANÁLISIS TEÓRICO (Bob IDE)
│   ├── bob_analisis_dfs.md
│   ├── bob_analisis_bubble_sort.md
│   ├── bob_sesion_dfs_consumo.png
│   ├── README_BOB_SESSIONS.md
│   └── (otros análisis...)
│
├── 📁 data/                       ← 📊 DATOS Y MÉTRICAS
│   ├── grafos_prueba.json         (entrada: datos de prueba)
│   ├── metricas_salida.json       (salida: benchmarks)
│   └── README_DATA.md
│
├── 📁 output/                     ← 📄 REPORTES FINALES
│   ├── REPORTE_FINAL_QA.md        (reporte master)
│   ├── README_OUTPUT.md
│   └── diagramas/
│       ├── crecimiento_tiempo.png
│       ├── crecimiento_memoria.png
│       └── comparacion_teorica_practica.png
│
├── 📁 src/                        ← 🐍 CÓDIGO FUENTE
│   ├── algoritmos.py              (algoritmos a optimizar)
│   ├── motor_qa.py                (ejecuta benchmarks → metricas_salida.json)
│   ├── gui_paso1_real.py          (GUI Tkinter para el flujo)
│   ├── servidor_paso1.py          (API REST alternativa)
│   ├── integrador_watsonx.py      (conexión a watsonx.ai)
│   └── examples/
│       ├── tarea.py               (grafos y DFS)
│       ├── inefficient_sort.py    (O(N²) para pruebas)
│       └── nested_loops_example.py
│
└── 📁 [otros archivos]
    ├── .env                       (credenciales - NO subir)
    ├── .gitignore
    ├── requirements.txt
    ├── README.md
    └── INICIO_RAPIDO.md
```

---

## 🔄 FLUJO PASO A PASO

### Paso 1️⃣: Bob IDE Manual (Análisis Teórico)
```
🎯 Ubicación: bob_sessions/

Tú haces:
1. Abres VS Code con Bob IDE
2. Cargas algoritmo (ej: dfs)
3. Pides análisis Big-O a Bob
4. Exportas resultado como: bob_analisis_dfs.md
5. Tomas captura de consumo: bob_sesion_dfs_consumo.png
6. Guardas en bob_sessions/

Resultado:
✅ bob_sessions/bob_analisis_dfs.md
✅ bob_sessions/bob_sesion_dfs_consumo.png
```

### Paso 2️⃣: Motor Local (Benchmarks Prácticos)
```
🎯 Ubicación: data/

Sistema ejecuta:
1. python src/motor_qa.py
2. Lee: data/grafos_prueba.json
3. Ejecuta función con N = 10, 100, 1000, 5000
4. Mide tiempo (ms) y memoria (bytes)
5. Genera: data/metricas_salida.json

Resultado:
✅ data/metricas_salida.json
   {
     "10": {time: 0.15ms, mem: 2.4KB},
     "100": {time: 1.52ms, mem: 24KB},
     "1000": {time: 15.2ms, mem: 240KB},
     "5000": {time: 152ms, mem: 2400KB}
   }
```

### Paso 3️⃣: Integración watsonx.ai (Reporte Final)
```
🎯 Ubicación: output/

Sistema ejecuta:
1. Lee: bob_sessions/bob_analisis_dfs.md
2. Lee: data/metricas_salida.json
3. Envía ambos a watsonx.ai
4. watsonx compara teoría vs práctica
5. Genera: output/REPORTE_FINAL_QA.md

Resultado:
✅ output/REPORTE_FINAL_QA.md
   (incluye: análisis + métricas + divergencia + recomendaciones)
```

---

## 📋 REFERENCIA RÁPIDA

| Carpeta | Contenido | Generado Por | Frecuencia |
|---------|----------|--------------|-----------|
| **bob_sessions/** | .md de Bob IDE + .png | TÚ (manual en Bob) | Una vez por algoritmo |
| **data/** | JSON de benchmarks | `motor_qa.py` | Cada ejecución |
| **output/** | Reporte final | GUI/API (watsonx) | Después de integrar |
| **src/** | Código Python | TÚ (desarrollo) | Según necesites |

---

## ✅ CHECKLIST ANTES DE ENTREGAR

### En `bob_sessions/`
- [ ] Al menos 1 archivo `bob_analisis_*.md`
- [ ] Archivo .png de captura de Bob
- [ ] Contenido sin errores de sintaxis
- [ ] Archivos commitados en git

### En `data/`
- [ ] `grafos_prueba.json` existe
- [ ] `metricas_salida.json` generado correctamente
- [ ] Formato JSON válido
- [ ] Métricas para N = 10, 100, 1000, 5000

### En `output/`
- [ ] `REPORTE_FINAL_QA.md` existe
- [ ] Incluye análisis de Bob
- [ ] Incluye métricas locales
- [ ] Incluye análisis de divergencia
- [ ] Incluye recomendaciones
- [ ] Archivo está commitado

### En `src/`
- [ ] `gui_paso1_real.py` funciona sin errores
- [ ] `motor_qa.py` genera métricas correctas
- [ ] `integrador_watsonx.py` configurado
- [ ] Todos los .py sin errores de sintaxis

---

## 🚀 COMANDOS ÚTILES

```bash
# Ver estructura actual
tree -L 2 -I __pycache__

# Verificar contenido de bob_sessions
ls -la bob_sessions/

# Ver métricas generadas
cat data/metricas_salida.json | python -m json.tool

# Ver reporte final
cat output/REPORTE_FINAL_QA.md

# Ejecutar motor local
python src/motor_qa.py

# Abrir GUI
python src/gui_paso1_real.py

# Abrir servidor REST
python src/servidor_paso1.py
```

---

## 📝 Notas Importantes

✅ **Debe estar en git:** bob_sessions/ (evidencia oficial)
✅ **Debe estar en git:** output/REPORTE_FINAL_QA.md (reporte)
❓ **Opcional en git:** data/metricas_salida.json (se regenera)
❌ **NUNCA en git:** .env (credenciales)

---

## 🎓 Ejemplo Completo

```
Paso 1: Analizar DFS en Bob IDE
└─ Exportar a: bob_sessions/bob_analisis_dfs.md

Paso 2: Ejecutar benchmarks
python src/motor_qa.py
└─ Genera: data/metricas_salida.json

Paso 3: Integrar y reportar
python src/gui_paso1_real.py
└─ Genera: output/REPORTE_FINAL_QA.md

Resultado:
✅ bob_sessions/bob_analisis_dfs.md (teoría)
✅ data/metricas_salida.json (práctica)
✅ output/REPORTE_FINAL_QA.md (reporte final)
```
