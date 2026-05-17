# OptiCode QA — PASO 1 (Polibit Hackathon 2026)

## Descripción

OptiCode QA es una herramienta de auditoría automática de rendimiento y complejidad para código Python. Este repositorio contiene un sistema que analiza la complejidad teórica de funciones, ejecuta benchmarks prácticos, compara teoría vs práctica y genera reportes listos para entrega.

El proyecto está pensado para facilitar evaluaciones rápidas de algoritmos (por ejemplo: DFS, ordenamientos) y para integrarse con una interfaz web y APIs REST.

## Características principales

- Análisis automático de complejidad (AST)
- Benchmarks prácticos (tiempo y memoria)
- Comparación entre complejidad teórica y observada
- Generación de reportes en Markdown y JSON
- Interfaz web para ejecución y visualización
- API REST para integración programática

## Quick Start

Requisitos: Python 3.10+ (recomendado) y pip.

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar servidor web (dashboard):

```bash
python src/servidor_paso1.py
```

3. Abrir en el navegador:

http://localhost:5000

4. Ejecutar pruebas rápidas (opcional):

```bash
python test_paso1_automatico.py
```

## Estructura del repositorio

Una vista rápida de los elementos más importantes:

- `bob_sessions/` — Análisis estilo Bob IDE en Markdown y capturas.
- `data/` — Datos de entrada y métricas generadas (`grafos_prueba.json`, `metricas_salida.json`).
- `output/` — Reportes finales y diagramas (`REPORTE_FINAL_QA.md`, `PASO1_COMPARACION.md`).
- `src/` — Código fuente del sistema:
  - `algoritmos.py` — Ejemplos/algoritmos a analizar.
  - `motor_qa.py` — Motor de benchmarks prácticos.
  - `analizador_automatico.py` — Lógica de análisis AST (si existe / equivalente).
  - `paso1_automatico.py` — Orquestador del flujo PASO 1.
  - `servidor_paso1.py` — API REST y servidor Flask.
- `INICIO_RAPIDO.md` — Guía mínima para arrancar.
- `README_PASO1_AUTOMATICO.md` — Documentación específica del modo automático.

## Cómo usar la API (ejemplos)

Ejecutar todo el PASO 1 mediante la API REST:

```bash
curl -X POST http://localhost:5000/api/paso1/ejecutar \
  -H "Content-Type: application/json" \
  -d '{"codigo":"def dfs(graph, start): ...","nombre_archivo":"algoritmos.py","grafo_path":"data/grafos_prueba.json"}'
```

Ejecutar solo análisis teórico:

```bash
curl -X POST http://localhost:5000/api/paso1/analizar-codigo -H "Content-Type: application/json" -d '{"codigo":"def foo(): pass"}'
```

## Reportes generados

Después de ejecutar el flujo, se generan automáticamente:

- `bob_sessions/analisis_automatico.md` — Análisis técnico detallado.
- `data/metricas_salida.json` — Métricas de benchmarks.
- `output/PASO1_COMPARACION.md` — Comparación teoría vs práctica.
- `output/paso1_resumen.json` — Resumen ejecutivo en JSON.

## Troubleshooting rápido

- Si falta `flask`: `pip install -r requirements.txt`.
- Si el servidor no responde: verificar que `src/servidor_paso1.py` esté corriendo.
- Si los benchmarks son lentos: reducir tamaños de prueba en `paso1_automatico.py`.

## Desarrollo y pruebas

- Ejecuta linter/sintaxis antes de commitear.
- Añade nuevos algoritmos en `src/algoritmos.py` o `src/examples/`.
- Para depurar el motor de benchmarks, ejecuta `python src/motor_qa.py`.

## Contribuir

1. Crea una rama feature/bugfix.
2. Añade tests mínimos si aplica.
3. Abre un Pull Request describiendo cambios.

## Créditos

Proyecto creado para el Hackathon Polibit 2026 — OptiCode QA.

## Licencia

El repositorio contiene materiales del hackathon; añade una licencia apropiada si planeas publicar (por ejemplo MIT).

---

Para más detalles específicos del modo automático, consulta `README_PASO1_AUTOMATICO.md`.
