# 📁 output/ — Reportes Finales y Exportaciones

## 📝 Propósito
Esta carpeta contiene:
- **Reportes finales generados:** REPORTE_FINAL_QA.md (cruza teoría + práctica)
- **Diagramas y visualizaciones:** gráficas, imágenes, comparaciones
- **Exportaciones JSON:** resúmenes ejecutivos

## 📋 Estructura

### 📊 Reportes Principales

#### `REPORTE_FINAL_QA.md`
Reporte integral que combina:

1. **Análisis Teórico (de Bob IDE)**
   ```markdown
   # Análisis de Complejidad
   - Big-O detectado: O(N²)
   - Cuellos de botella: líneas 5, 8, 12
   ```

2. **Métricas Prácticas (del Motor Local)**
   ```json
   {
     "N": [10, 100, 1000, 5000],
     "tiempo_ms": [0.15, 1.52, 15.2, 152],
     "memoria_kb": [2.4, 24, 240, 2400]
   }
   ```

3. **Análisis de Divergencia (de watsonx.ai)**
   ```
   Teoría predice O(N²): debería crecer 100x
   Práctica muestra: crece 100.8x
   ✅ Divergencia: 0.8% (coincide perfectamente)
   ```

4. **Recomendaciones Finales**
   - Optimizaciones propuestas
   - Impacto estimado en coste cloud
   - Prioridad de corrección

### 📁 Subcarpeta: `diagramas/`

```
output/diagramas/
├── README.md                    (este archivo)
├── crecimiento_tiempo.png       (gráfica N vs ms)
├── crecimiento_memoria.png      (gráfica N vs KB)
├── comparacion_teorica_practica.png
└── recomendaciones_prioridad.png
```

**Contenido:**
- Gráficas de crecimiento temporal
- Gráficas de consumo de memoria
- Comparación visual teoría vs realidad
- Matriz de prioridad de optimizaciones

## 🔄 Workflow de Generación

### Opción 1: Vía GUI Tkinter
```bash
python src/gui_paso1_real.py

# Pasos:
# 1. Cargar análisis .md de bob_sessions
# 2. Cargar código .py
# 3. Ejecutar benchmarks → genera data/metricas_salida.json
# 4. Integrar con watsonx.ai
# 5. ✅ Genera output/REPORTE_FINAL_QA.md
```

### Opción 2: Vía API REST
```bash
python src/servidor_paso1.py

# Endpoints:
curl -X GET http://localhost:5000/api/bob-sessions
curl -X POST http://localhost:5000/api/ejecutar-benchmarks
curl -X POST http://localhost:5000/api/integrar-watsonx
curl -X GET http://localhost:5000/api/reportes
```

## 📈 Estructura del Reporte Final

```markdown
# 📊 REPORTE FINAL QA — OptiCode

## Ejecutivo
- Algoritmo: DFS
- Complejidad Teórica: O(V + E)
- Complejidad Práctica: O(1.02 × (V + E))
- Divergencia: ±2%
- Estado: ✅ OPTIMIZADO

## 1. Análisis Teórico (Bob IDE)
[Contenido completo de bob_analisis_*.md]

## 2. Métricas Prácticas (Motor Local)
[JSON con benchmarks para N = 10, 100, 1000, 5000]

## 3. Comparación Teoría vs Práctica
[Análisis de discrepancias]

## 4. Cuellos de Botella Críticos
- [P0] Búsqueda lineal en línea 8 (alto impacto)
- [P1] Diccionario no indexado en línea 5 (medio)
- [P2] Loop sobre lista completa (bajo)

## 5. Recomendaciones de Optimización
1. Usar hash set en lugar de lista
2. Precalcular índices
3. Paralelizar búsqueda

## 6. Impacto Financiero Estimado
- Coste actual: ~$850/mes en AWS
- Coste optimizado: ~$42/mes
- Ahorro potencial: 95%

---
*Generado: [timestamp]*
*Auditor: IBM watsonx.ai*
*Fuentes: Bob IDE + Motor Local*
```

## ✅ Deliverables para Jurado

Los archivos de esta carpeta incluyen:

```
✅ REPORTE_FINAL_QA.md          → Entrega principal al jurado
✅ diagramas/*.png               → Evidencia visual
✅ datos comparativos en JSON    → Datos procesables
```

## 🎯 Checklist Antes de Entregar

- [ ] `REPORTE_FINAL_QA.md` existe y tiene contenido
- [ ] Análisis de Bob IDE integrado
- [ ] Métricas locales incluidas
- [ ] Análisis de divergencia completado
- [ ] Recomendaciones redactadas
- [ ] Impacto financiero estimado
- [ ] Diagramas generados (opcional pero recomendado)
- [ ] Todo commitado en git
