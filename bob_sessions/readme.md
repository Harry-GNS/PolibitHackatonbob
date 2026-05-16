# OptiCode QA — Auditor de rendimiento y coste computacional

OptiCode QA es una herramienta de QA enfocada en detectar ineficiencias algorítmicas antes de producción y traducirlas a impacto real: tiempo, memoria y coste estimado en infraestructura cloud.

La idea clave no es que la IA “adivine” todo desde cero. El sistema funciona mejor si separa responsabilidades:
- IBM Bob IDE produce la teoría de complejidad.
- El motor local en Python produce la evidencia práctica.
- watsonx.ai actúa como auditor e integrador final, cruza ambas fuentes y redacta el reporte final.

## Arquitectura del flujo

```text
[Código Fuente] ──> Analizado manualmente en IBM Bob IDE ──> Archivo .md (Teoría)
                       │
[Código Fuente] ──> Ejecutado en Motor Local (Python) ──> JSON/CSV (Práctica)
                       │
                       ▼
               ┌──────────────────────────┐
               │   AGENTE WATSONX.AI      │
               │  (Auditor e Integrador)  │
               └──────────┬───────────────┘
                       │
                       ▼
               [Reporte Final de QA]
```

## Qué hace cada capa

### 1) IBM Bob IDE: capa teórica
IBM Bob IDE se usa de forma quirúrgica sobre funciones o módulos concretos. Su trabajo es identificar la complejidad matemática, encontrar puntos críticos y exportar la evidencia en Markdown dentro de `bob_sessions`.

En esta capa buscamos respuestas como:
- ¿Cuál es la complejidad Big-O del algoritmo?
- ¿Dónde está el cuello de botella teórico?
- ¿Qué optimizaciones lógicas propone Bob?

Importante: no se le pasa todo el repositorio. La estrategia correcta es usar Bob sobre piezas específicas para ahorrar Bobcoins y mantener el análisis enfocado.

### 2) Motor local en Python: capa práctica
El motor local ejecuta los algoritmos con distintos tamaños de entrada y mide:
- tiempo de ejecución en milisegundos,
- pico de memoria RAM,
- resultados exportables en JSON o CSV.

Esta capa responde a una pregunta distinta a Bob: no “qué debería pasar” en teoría, sino “qué está pasando de verdad” en el entorno de ejecución.

### 3) watsonx.ai vía API: capa de auditoría e integración
El agente de watsonx.ai no debe analizar el código desde cero. Su rol es más útil si se convierte en el integrador inteligente del proyecto.

Recibe tres entradas:
1. El código original.
2. El reporte de complejidad generado por Bob.
3. Las métricas reales del motor local.

Con eso, el agente debe:
- comparar teoría vs práctica,
- detectar discrepancias y posibles cuellos de botella ocultos,
- estimar impacto financiero aproximado en servicios cloud,
- estructurar el reporte final de QA para el jurado o cliente.

Esto es mejor que pedirle al modelo que analice todo desde cero porque:
- consume menos tokens y menos recursos,
- hace que Bob siga siendo el núcleo formal del análisis,
- convierte a watsonx.ai en un agente real, no solo en un generador de texto.

## Flujo de trabajo del equipo

1. Elegir uno o varios algoritmos relevantes del repositorio.
2. Auditar esos fragmentos en IBM Bob IDE y guardar la salida en `bob_sessions`.
3. Ejecutarlos en el motor local para capturar tiempo y memoria.
4. Pasar teoría + práctica al agente de watsonx.ai para que genere el diagnóstico final.
5. Exportar el reporte final y reunir todas las evidencias en el repositorio público.

## Reparto sugerido para 4 personas

- Persona 1: selección de algoritmos y limpieza del código de credenciales.
- Persona 2: auditoría manual en Bob IDE y exportación de sesiones.
- Persona 3: motor local de benchmarks y exportación de métricas.
- Persona 4: integración con watsonx.ai, reporte final y video demo.

## Entregables mínimos

- Código fuente limpio y reproducible.
- Carpeta `bob_sessions` con `.md` y capturas de Bob IDE.
- Archivo de métricas generado por el motor local.
- `REPORTE_FINAL_QA.md` con el diagnóstico final.
- Repositorio público para la entrega.
- Video demo de hasta 5 minutos.

## Estructura esperada de carpetas

```text
opticode-qa/
├── .gitignore
├── .env
├── README.md
├── requirements.txt
├── bob_sessions/
│   ├── sesion_dfs_historico.md
│   ├── consumo_bob_ide_1.png
│   └── sesion_optimizacion.md
├── src/
│   ├── __init__.py
│   ├── algoritmos.py
│   ├── motor_qa.py
│   └── integrador_watsonx.py
├── data/
│   ├── grafos_prueba.json
│   └── metricas_salida.json
└── output/
   ├── diagramas/
   └── REPORTE_FINAL_QA.md
```

## Nota operativa

Antes de subir el proyecto al repositorio público, elimina cualquier clave real y deja las credenciales solo en `.env`. Ese archivo no debe compartirse.

## Cómo empezamos ahora mismo

1. Elegir un algoritmo base ineficiente que ya exista en el repositorio o en los apuntes del equipo. Lo ideal es algo con complejidad cuadrática $O(N^2)$ o cúbica $O(N^3)$ para que Bob y el motor local tengan un caso claro que analizar.
2. Abrir ese archivo en IBM Bob IDE, pedir el análisis de complejidad y exportar la sesión en Markdown junto con la captura de consumo en `bob_sessions`.
3. Mientras una persona trabaja en Bob, otra implementa el motor local en Python para medir tiempo y memoria con tamaños crecientes como $N = 10, 100, 500, 1000$ y guardar la salida en JSON o CSV.
4. Cuando ya existan la teoría de Bob y las métricas reales, conectar watsonx.ai como auditor e integrador final para cruzar ambos insumos, estimar impacto financiero y redactar el reporte final en Markdown.
5. Si no tienen todavía un algoritmo elegido, empezar con el más simple de buscar: un bucle anidado, una búsqueda lineal repetida o una ruta de grafo mal implementada. Lo importante es que sea fácil de medir y comparar.

## Interfaz visual del Paso 1

Para que el paso 1 no dependa solo de Markdown, se añadió una interfaz local en Python pensada como un panel ejecutivo:

- Carga el código fuente conejillo de indias.
- Carga el reporte teórico exportado desde IBM Bob IDE.
- Carga las métricas reales del motor local.
- Muestra una lectura visual de divergencia, complejidad y riesgo.
- Exporta un reporte HTML y un JSON resumen para compartir con el equipo.

El archivo principal de esta interfaz es `src/step1_studio.py`. La idea es usarlo como la pantalla central del paso 1, mientras `bob_sessions` sigue guardando la evidencia original de Bob.


