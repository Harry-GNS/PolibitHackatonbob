**User:**

<task>
EL PDF QUE SALE, NO SE VE BIEN, QUIERO QUE TENGA COLORES CORPORATIVOS, AZULES MARINOS ENTIENDES? Y QUE SEA LEIBLE
</task>
<environment_details>
# VSCode Visible Files
.gitignore

# VSCode Open Tabs
templates/dashboard.html,src/servidor_paso1_web.py,.gitignore,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:53:54.028Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (c:/Users/harry/PolibitHackatonbob) Files
.gitignore
ESTRUCTURA_FINAL.txt
LOGOQA.png
README.md
requirements.txt
data/
data/grafos_prueba.json
data/metricas_salida.json
output/
output/informesbob/
output/informesbob/ANALISIS_RENDIMIENTO_ALGORITMOS_BUSQUEDA.md
src/
src/algoritmos.py
src/integrador_watsonx.py
src/motor_qa.py
src/PolibitHackatonbob.code-workspace
src/servidor_paso1_web.py
templates/
templates/dashboard.html
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll help you improve the PDF output with corporate navy blue colors and better readability. Let me first examine the current code to understand how the PDF is being generated.

<read_file>
<args>
<file>
<path>src/servidor_paso1_web.py</path>
</file>
<file>
<path>src/motor_qa.py</path>
</file>
<file>
<path>src/integrador_watsonx.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'src/servidor_paso1_web.py', 'src/motor_qa.py', 'src/integrador_watsonx.py'] Result:
<files>
<file><path>src/servidor_paso1_web.py</path>
<content lines="1-851">
  1 | """Servidor Flask con interfaz web bonita para PASO 1 Real
  2 | 
  3 | Flujo: Bob IDE (manual) → Motor Local → watsonx.ai
  4 | """
  5 | 
  6 | from flask import Flask, render_template, request, jsonify, send_from_directory
  7 | from flask_cors import CORS
  8 | from pathlib import Path
  9 | import ast
 10 | import json
 11 | import traceback
 12 | import sys
 13 | import re
 14 | from datetime import datetime
 15 | 
 16 | # Añadir el directorio raíz al path
 17 | ROOT = Path(__file__).resolve().parents[1]
 18 | sys.path.insert(0, str(ROOT))
 19 | 
 20 | from src.motor_qa import run_benchmarks
 21 | from src.integrador_watsonx import summarize_metrics
 22 | 
 23 | app = Flask(__name__, template_folder=str(ROOT / "templates"))
 24 | CORS(app)
 25 | 
 26 | # Directorio de análisis de Bob IDE - USAR SOLO output/informesbob
 27 | BOB_SESSIONS_DIR = ROOT / "output" / "informesbob"
 28 | OUTPUT_DIR = ROOT / "output"
 29 | DATA_DIR = ROOT / "data"
 30 | SRC_DIR = ROOT / "src"
 31 | 
 32 | # Crear directorios si no existen
 33 | BOB_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
 34 | OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
 35 | DATA_DIR.mkdir(parents=True, exist_ok=True)
 36 | 
 37 | 
 38 | # ============================================
 39 | # RUTAS HTML (Frontend)
 40 | # ============================================
 41 | 
 42 | @app.route('/')
 43 | def index():
 44 |     """Sirve el dashboard principal."""
 45 |     return render_template('dashboard.html')
 46 | 
 47 | 
 48 | @app.route('/LOGOQA.png')
 49 | def logo_qa():
 50 |     """Sirve el logo del dashboard."""
 51 |     return send_from_directory(str(ROOT), 'LOGOQA.png')
 52 | 
 53 | 
 54 | # ============================================
 55 | # API REST (Backend)
 56 | # ============================================
 57 | 
 58 | @app.route('/api/bob-sessions', methods=['GET'])
 59 | def listar_bob_sessions():
 60 |     """Lista todos los análisis .md de Bob IDE."""
 61 |     try:
 62 |         archivos = []
 63 |         
 64 |         if BOB_SESSIONS_DIR.exists():
 65 |             for archivo in sorted(BOB_SESSIONS_DIR.glob('*.md')):
 66 |                 # Saltar archivos README
 67 |                 if 'README' in archivo.name:
 68 |                     continue
 69 |                     
 70 |                 contenido = archivo.read_text(encoding='utf-8')
 71 |                 archivos.append({
 72 |                     "nombre": archivo.name,
 73 |                     "contenido_preview": contenido[:200],
 74 |                     "tamaño": len(contenido),
 75 |                     "tipo": "Bob IDE Analysis"
 76 |                 })
 77 |         
 78 |         return jsonify({
 79 |             "success": True,
 80 |             "total": len(archivos),
 81 |             "archivos": archivos
 82 |         })
 83 |     
 84 |     except Exception as e:
 85 |         return jsonify({"success": False, "error": str(e)}), 500
 86 | 
 87 | 
 88 | @app.route('/api/bob-sessions/<nombre>', methods=['GET'])
 89 | def obtener_bob_analysis(nombre):
 90 |     """Obtiene el contenido completo de un análisis de Bob IDE."""
 91 |     try:
 92 |         ruta = BOB_SESSIONS_DIR / nombre
 93 |         
 94 |         if not ruta.exists():
 95 |             return jsonify({"error": f"Archivo no encontrado: {nombre}"}), 404
 96 |         
 97 |         contenido = ruta.read_text(encoding='utf-8')
 98 |         
 99 |         return jsonify({
100 |             "success": True,
101 |             "nombre": nombre,
102 |             "contenido": contenido
103 |         })
104 |     
105 |     except Exception as e:
106 |         return jsonify({"success": False, "error": str(e)}), 500
107 | 
108 | 
109 | @app.route('/api/codigos', methods=['GET'])
110 | def listar_codigos():
111 |     """Lista archivos .py disponibles para benchmarks."""
112 |     try:
113 |         archivos = []
114 |         
115 |         # Buscar en src/
116 |         if SRC_DIR.exists():
117 |             for archivo in sorted(SRC_DIR.glob('*.py')):
118 |                 if archivo.name.startswith('__'):
119 |                     continue
120 |                     
121 |                 contenido = archivo.read_text(encoding='utf-8')
122 |                 archivos.append({
123 |                     "nombre": archivo.name,
124 |                     "ruta": f"src/{archivo.name}",
125 |                     "contenido_preview": contenido[:200]
126 |                 })
127 |         
128 |         # Buscar en src/examples/
129 |         examples_dir = SRC_DIR / "examples"
130 |         if examples_dir.exists():
131 |             for archivo in sorted(examples_dir.glob('*.py')):
132 |                 if archivo.name.startswith('__'):
133 |                     continue
134 |                     
135 |                 contenido = archivo.read_text(encoding='utf-8')
136 |                 archivos.append({
137 |                     "nombre": archivo.name,
138 |                     "ruta": f"src/examples/{archivo.name}",
139 |                     "contenido_preview": contenido[:200]
140 |                 })
141 |         
142 |         return jsonify({
143 |             "success": True,
144 |             "total": len(archivos),
145 |             "archivos": archivos
146 |         })
147 |     
148 |     except Exception as e:
149 |         return jsonify({"success": False, "error": str(e)}), 500
150 | 
151 | 
152 | @app.route('/api/codigos/<nombre>', methods=['GET'])
153 | def obtener_codigo(nombre):
154 |     """Obtiene el contenido de un archivo .py."""
155 |     try:
156 |         # Buscar en src/
157 |         rutas_posibles = [
158 |             SRC_DIR / nombre,
159 |             SRC_DIR / "examples" / nombre
160 |         ]
161 |         
162 |         for ruta in rutas_posibles:
163 |             if ruta.exists():
164 |                 contenido = ruta.read_text(encoding='utf-8')
165 |                 return jsonify({
166 |                     "success": True,
167 |                     "nombre": nombre,
168 |                     "contenido": contenido
169 |                 })
170 |         
171 |         return jsonify({"error": f"Archivo no encontrado: {nombre}"}), 404
172 |     
173 |     except Exception as e:
174 |         return jsonify({"success": False, "error": str(e)}), 500
175 | 
176 | 
177 | @app.route('/api/analizar-codigo-personalizado', methods=['POST'])
178 | def analizar_codigo_personalizado():
179 |     """Analiza código Python pegado por el usuario con heurísticas estáticas simples."""
180 |     try:
181 |         data = request.get_json(silent=True) or {}
182 |         codigo = (data.get('codigo') or '').strip()
183 |         nombre = (data.get('nombre') or 'codigo_pegado.py').strip()
184 | 
185 |         if not codigo:
186 |             return jsonify({
187 |                 "success": False,
188 |                 "error": "El campo 'codigo' está vacío."
189 |             }), 400
190 | 
191 |         lineas = codigo.splitlines()
192 | 
193 |         try:
194 |             tree = ast.parse(codigo)
195 |         except SyntaxError as exc:
196 |             return jsonify({
197 |                 "success": False,
198 |                 "error": f"Error de sintaxis en línea {exc.lineno}: {exc.msg}",
199 |                 "nombre": nombre,
200 |                 "codigo": codigo,
201 |                 "analisis": {
202 |                     "titulo": "Código pegado con errores de sintaxis",
203 |                     "complejidad_estimada": "No evaluable",
204 |                     "puntos_clave": [
205 |                         f"La línea {exc.lineno or '?'} tiene un error de sintaxis: {exc.msg}",
206 |                     ],
207 |                     "cuellos_botella": [],
208 |                     "recomendaciones": [
209 |                         "Corrige la sintaxis antes de ejecutar el análisis de complejidad.",
210 |                         "Verifica sangrías, paréntesis y dos puntos en funciones y bucles."
211 |                     ],
212 |                     "metricas": {
213 |                         "lineas_detectadas": len(lineas),
214 |                         "errores_sintaxis": True,
215 |                     }
216 |                 }
217 |             }), 200
218 | 
219 |         class HeuristicaVisitor(ast.NodeVisitor):
220 |             def __init__(self):
221 |                 self.funciones = []
222 |                 self.bucles = []
223 |                 self.comparaciones_in = []
224 |                 self.comprehensions = []
225 |                 self.recursivas = []
226 |                 self.max_profundidad_bucles = 0
227 |                 self._profundidad_bucle = 0
228 |                 self._pila_funciones = []
229 | 
230 |             def visit_FunctionDef(self, node):
231 |                 self.funciones.append({
232 |                     "nombre": node.name,
233 |                     "linea": node.lineno,
234 |                 })
235 |                 self._pila_funciones.append(node.name)
236 |                 self.generic_visit(node)
237 |                 self._pila_funciones.pop()
238 | 
239 |             visit_AsyncFunctionDef = visit_FunctionDef
240 | 
241 |             def visit_For(self, node):
242 |                 self._profundidad_bucle += 1
243 |                 self.max_profundidad_bucles = max(self.max_profundidad_bucles, self._profundidad_bucle)
244 |                 self.bucles.append({
245 |                     "tipo": "for",
246 |                     "linea": node.lineno,
247 |                     "anidado": self._profundidad_bucle > 1,
248 |                 })
249 |                 self.generic_visit(node)
250 |                 self._profundidad_bucle -= 1
251 | 
252 |             def visit_While(self, node):
253 |                 self._profundidad_bucle += 1
254 |                 self.max_profundidad_bucles = max(self.max_profundidad_bucles, self._profundidad_bucle)
255 |                 self.bucles.append({
256 |                     "tipo": "while",
257 |                     "linea": node.lineno,
258 |                     "anidado": self._profundidad_bucle > 1,
259 |                 })
260 |                 self.generic_visit(node)
261 |                 self._profundidad_bucle -= 1
262 | 
263 |             def visit_Call(self, node):
264 |                 if self._pila_funciones and isinstance(node.func, ast.Name):
265 |                     if node.func.id == self._pila_funciones[-1]:
266 |                         self.recursivas.append({
267 |                             "funcion": node.func.id,
268 |                             "linea": node.lineno,
269 |                         })
270 |                 self.generic_visit(node)
271 | 
272 |             def visit_Compare(self, node):
273 |                 if any(isinstance(op, (ast.In, ast.NotIn)) for op in node.ops):
274 |                     self.comparaciones_in.append(node.lineno)
275 |                 self.generic_visit(node)
276 | 
277 |             def visit_ListComp(self, node):
278 |                 self.comprehensions.append({"tipo": "listcomp", "linea": node.lineno})
279 |                 self.generic_visit(node)
280 | 
281 |             def visit_SetComp(self, node):
282 |                 self.comprehensions.append({"tipo": "setcomp", "linea": node.lineno})
283 |                 self.generic_visit(node)
284 | 
285 |             def visit_DictComp(self, node):
286 |                 self.comprehensions.append({"tipo": "dictcomp", "linea": node.lineno})
287 |                 self.generic_visit(node)
288 | 
289 |             def visit_GeneratorExp(self, node):
290 |                 self.comprehensions.append({"tipo": "genexp", "linea": node.lineno})
291 |                 self.generic_visit(node)
292 | 
293 |         visitor = HeuristicaVisitor()
294 |         visitor.visit(tree)
295 | 
296 |         if visitor.max_profundidad_bucles >= 3:
297 |             complejidad = 'O(N^3) o peor'
298 |         elif visitor.max_profundidad_bucles == 2:
299 |             complejidad = 'O(N^2)'
300 |         elif visitor.max_profundidad_bucles == 1:
301 |             complejidad = 'O(N)'
302 |         else:
303 |             complejidad = 'O(1) a O(N) según las operaciones internas'
304 | 
305 |         puntos_clave = []
306 |         if visitor.funciones:
307 |             puntos_clave.append(f"Se detectaron {len(visitor.funciones)} función(es) en el código pegado.")
308 |         if visitor.max_profundidad_bucles > 0:
309 |             puntos_clave.append(f"Profundidad máxima de bucles detectada: {visitor.max_profundidad_bucles}.")
310 |         if visitor.recursivas:
311 |             nombres_recursivos = ', '.join(sorted({r['funcion'] for r in visitor.recursivas}))
312 |             puntos_clave.append(f"Se detectó recursión directa en: {nombres_recursivos}.")
313 |         if visitor.comparaciones_in:
314 |             puntos_clave.append(f"Se hallaron {len(visitor.comparaciones_in)} comparaciones 'in/not in', posibles cuellos de botella en listas.")
315 |         if visitor.comprehensions:
316 |             puntos_clave.append(f"Se detectaron {len(visitor.comprehensions)} comprensiones de datos.")
317 | 
318 |         cuellos_botella = []
319 |         recomendaciones = []
320 |         alertas = []
321 | 
322 |         for bucle in visitor.bucles:
323 |             etiqueta = f"Línea {bucle['linea']} ({bucle['tipo']})"
324 |             if bucle['anidado']:
325 |                 cuellos_botella.append(f"{etiqueta}: bucle anidado que puede elevar la complejidad.")
326 |                 recomendaciones.append("Revisa si el bucle interno puede eliminarse, indexarse o precalcularse.")
327 |                 alertas.append({
328 |                     'tipo': 'BUCLE_ANIDADO',
329 |                     'nivel': 'warning',
330 |                     'icono': 'WARNING',
331 |                     'mensaje': f"Bucle anidado detectado en la línea {bucle['linea']}",
332 |                     'linea': bucle['linea']
333 |                 })
334 | 
335 |         for rec in visitor.recursivas:
336 |             cuellos_botella.append(f"Línea {rec['linea']}: llamada recursiva a {rec['funcion']}().")
337 |             recomendaciones.append("Verifica el caso base y evalúa una versión iterativa si la profundidad puede crecer mucho.")
338 |             alertas.append({
339 |                 'tipo': 'RECURSION',
340 |                 'nivel': 'info',
341 |                 'icono': 'RECURSION',
342 |                 'mensaje': f"Recursión detectada en {rec['funcion']}() línea {rec['linea']}",
343 |                 'linea': rec['linea']
344 |             })
345 | 
346 |         for linea in visitor.comparaciones_in:
347 |             cuellos_botella.append(f"Línea {linea}: comparación de membresía en una estructura lineal.")
348 |             recomendaciones.append("Si la estructura crece, cambia la lista por un set o dict para búsquedas O(1).")
349 |             alertas.append({
350 |                 'tipo': 'MEMBRESIA_LINEAL',
351 |                 'nivel': 'warning',
352 |                 'icono': 'SEARCH',
353 |                 'mensaje': f"Posible búsqueda lineal con 'in/not in' en la línea {linea}",
354 |                 'linea': linea
355 |             })
356 | 
357 |         if visitor.comprehensions:
358 |             cuellos_botella.append("Se detectaron comprensiones de datos que pueden duplicar trabajo si se usan dentro de bucles frecuentes.")
359 |             recomendaciones.append("Mantén las comprensiones solo si aportan claridad y no se ejecutan en rutas críticas repetidas.")
360 |             alertas.append({
361 |                 'tipo': 'COMPRENSIONES',
362 |                 'nivel': 'info',
363 |                 'icono': 'COMPREHENSION',
364 |                 'mensaje': f"Se detectaron {len(visitor.comprehensions)} comprensiones de datos",
365 |                 'cantidad': len(visitor.comprehensions)
366 |             })
367 | 
368 |         if not cuellos_botella:
369 |             cuellos_botella.append("No se detectaron cuellos de botella obvios con las heurísticas básicas.")
370 |             recomendaciones.append("Complementa este análisis con benchmarks locales si el código se ejecuta en rutas críticas.")
371 |             alertas.append({
372 |                 'tipo': 'SIN_ALERTAS_CRITICAS',
373 |                 'nivel': 'success',
374 |                 'icono': 'SUCCESS',
375 |                 'mensaje': 'No se detectaron patrones críticos evidentes con las heurísticas básicas.'
376 |             })
377 | 
378 |         metricas = {
379 |             'lineas_detectadas': len(lineas),
380 |             'funciones_detectadas': len(visitor.funciones),
381 |             'bucles_detectados': len(visitor.bucles),
382 |             'profundidad_maxima_bucles': visitor.max_profundidad_bucles,
383 |             'recursiones_detectadas': len(visitor.recursivas),
384 |             'comparaciones_in_detectadas': len(visitor.comparaciones_in),
385 |             'comprehensions_detectadas': len(visitor.comprehensions),
386 |             'complejidad_heuristica': complejidad,
387 |             'factor_riesgo': min(100, (visitor.max_profundidad_bucles * 25) + (len(visitor.recursivas) * 15) + (len(visitor.comparaciones_in) * 10) + (len(visitor.comprehensions) * 5))
388 |         }
389 | 
390 |         markdown = [
391 |             f"# Análisis de código pegado: {nombre}",
392 |             "",
393 |             "## Complejidad estimada",
394 |             f"- **Estimación global:** {complejidad}",
395 |             f"- **Líneas analizadas:** {len(lineas)}",
396 |             f"- **Funciones detectadas:** {len(visitor.funciones)}",
397 |             f"- **Profundidad máxima de bucles:** {visitor.max_profundidad_bucles}",
398 |             f"- **Factor de riesgo heurístico:** {metricas['factor_riesgo']}/100",
399 |             "",
400 |             "## Cuellos de botella",
401 |             *[f"- {item}" for item in cuellos_botella],
402 |             "",
403 |             "## Métricas detalladas",
404 |             f"- **Bucles detectados:** {metricas['bucles_detectados']}",
405 |             f"- **Recursiones detectadas:** {metricas['recursiones_detectadas']}",
406 |             f"- **Comparaciones in/not in:** {metricas['comparaciones_in_detectadas']}",
407 |             f"- **Comprensiones detectadas:** {metricas['comprehensions_detectadas']}",
408 |             "",
409 |             "## Recomendaciones",
410 |             *[f"- {item}" for item in recomendaciones[:6]],
411 |         ]
412 | 
413 |         return jsonify({
414 |             "success": True,
415 |             "nombre": nombre,
416 |             "codigo": codigo,
417 |             "analisis": {
418 |                 "titulo": f"Análisis de código pegado: {nombre}",
419 |                 "complejidad_estimada": complejidad,
420 |                 "puntos_clave": puntos_clave[:5],
421 |                 "cuellos_botella": cuellos_botella[:6],
422 |                 "recomendaciones": recomendaciones[:6],
423 |                 "metricas": metricas,
424 |                 "alertas": alertas[:8],
425 |             },
426 |             "markdown": "\n".join(markdown),
427 |             "metricas": metricas,
428 |             "alertas": alertas[:8],
429 |         })
430 | 
431 |     except Exception as e:
432 |         return jsonify({"success": False, "error": str(e)}), 500
433 | 
434 | 
435 | @app.route('/api/ejecutar-benchmarks', methods=['POST'])
436 | def ejecutar_benchmarks():
437 |     """Ejecuta motor_qa.py para benchmarks prácticos."""
438 |     try:
439 |         print("Iniciando benchmarks locales...")
440 |         
441 |         # Ejecutar motor_qa
442 |         run_benchmarks()
443 |         
444 |         # Cargar y procesar métricas generadas
445 |         metricas_path = DATA_DIR / "metricas_salida.json"
446 |         
447 |         if not metricas_path.exists():
448 |             return jsonify({
449 |                 "success": False,
450 |                 "error": "No se generó archivo de métricas"
451 |             }), 500
452 |         
453 |         metricas_raw = json.loads(metricas_path.read_text(encoding='utf-8'))
454 |         benchmarks = metricas_raw.get('benchmarks', {})
455 |         
456 |         # Procesar para formato visual, preservando estructura de algoritmos
457 |         metricas_procesadas = {}
458 |         for size_str in sorted(benchmarks.keys(), key=lambda x: int(x)):
459 |             metrics = benchmarks[size_str]
460 |             metricas_procesadas[size_str] = {}
461 |             
462 |             # Copiar estructura de algoritmos (dfs, ldfs, idfs)
463 |             for algo in ['dfs', 'ldfs', 'idfs']:
464 |                 if algo in metrics and isinstance(metrics[algo], dict):
465 |                     algo_data = metrics[algo]
466 |                     metricas_procesadas[size_str][algo] = {
467 |                         'time_ms_mean': round(float(algo_data.get('time_ms_mean', 0)), 2),
468 |                         'mem_bytes_peak_mean': round(float(algo_data.get('mem_bytes_peak_mean', 0)), 2),
469 |                         'time_ms_samples': [round(float(t), 2) for t in algo_data.get('time_ms_samples', [])],
470 |                         'mem_bytes_peak_samples': [round(float(m), 2) for m in algo_data.get('mem_bytes_peak_samples', [])]
471 |                     }
472 |             
473 |             # Agregar promedios a nivel de tamaño para compatibilidad con detectar_alertas
474 |             all_times = []
475 |             all_mems = []
476 |             for algo in ['dfs', 'ldfs', 'idfs']:
477 |                 if algo in metricas_procesadas[size_str]:
478 |                     all_times.append(metricas_procesadas[size_str][algo]['time_ms_mean'])
479 |                     all_mems.append(metricas_procesadas[size_str][algo]['mem_bytes_peak_mean'] / (1024 * 1024))
480 |             
481 |             if all_times:
482 |                 metricas_procesadas[size_str]['time_ms'] = round(sum(all_times) / len(all_times), 2)
483 |                 metricas_procesadas[size_str]['memory_mb'] = round(sum(all_mems) / len(all_mems), 2)
484 |         
485 |         # Detectar alertas de rendimiento
486 |         alertas = detectar_alertas(metricas_procesadas)
487 |         
488 |         # Obtener resumen del análisis si está disponible
489 |         resumen_analisis = None
490 |         bob_files = list(BOB_SESSIONS_DIR.glob('*.md'))
491 |         if bob_files:
492 |             # Tomar el archivo más reciente
493 |             archivo_mas_reciente = sorted(bob_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
494 |             contenido_md = archivo_mas_reciente.read_text(encoding='utf-8')
495 |             resumen_analisis = resumir_analisis_md(contenido_md)
496 |         
497 |         return jsonify({
498 |             "success": True,
499 |             "mensaje": "Benchmarks completados exitosamente",
500 |             "metricas": metricas_procesadas,
501 |             "alertas": alertas,
502 |             "resumen_analisis": resumen_analisis,
503 |             "timestamp": datetime.now().isoformat()
504 |         })
505 |     
506 |     except Exception as e:
507 |         return jsonify({
508 |             "success": False,
509 |             "error": f"Error en benchmarks: {str(e)}",
510 |             "traceback": traceback.format_exc()
511 |         }), 500
512 | 
513 | 
514 | @app.route('/api/resumen-analisis/<nombre>', methods=['GET'])
515 | def obtener_resumen_analisis(nombre):
516 |     """Obtiene el resumen procesado de un análisis MD."""
517 |     try:
518 |         ruta = BOB_SESSIONS_DIR / nombre
519 |         
520 |         if not ruta.exists():
521 |             return jsonify({"error": f"Archivo no encontrado: {nombre}"}), 404
522 |         
523 |         contenido = ruta.read_text(encoding='utf-8')
524 |         resumen = resumir_analisis_md(contenido)
525 |         
526 |         return jsonify({
527 |             "success": True,
528 |             "nombre": nombre,
529 |             "resumen": resumen,
530 |             "contenido_completo": contenido  # También devolver para PDF si es necesario
531 |         })
532 |     
533 |     except Exception as e:
534 |         return jsonify({"success": False, "error": str(e)}), 500
535 | 
536 | 
537 | def detectar_alertas(metricas):
538 |     """Detecta problemas de rendimiento y genera alertas."""
539 |     alertas = []
540 |     
541 |     if not metricas:
542 |         return alertas
543 |     
544 |     # Obtener valores ordenados por tamaño (convertir a int para ordenar correctamente)
545 |     sizes = sorted(metricas.keys(), key=lambda x: int(x) if isinstance(x, str) else x)
546 |     valores_tiempo = [metricas[s]['time_ms'] for s in sizes]
547 |     valores_memoria = [metricas[s]['memory_mb'] for s in sizes]
548 |     
549 |     # Convertir tamaños a int para comparaciones
550 |     sizes_int = [int(s) if isinstance(s, str) else s for s in sizes]
551 |     # Detectar crecimiento exponencial
552 |     if len(valores_tiempo) >= 2:
553 |         for i in range(1, len(valores_tiempo)):
554 |             tiempo_actual = valores_tiempo[i]
555 |             tiempo_anterior = valores_tiempo[i-1]
556 |             size_actual = sizes_int[i]
557 |             size_anterior = sizes_int[i-1]
558 |             
559 |             if tiempo_anterior > 0:
560 |                 ratio_tiempo = tiempo_actual / tiempo_anterior
561 |                 ratio_tamaño = size_actual / size_anterior
562 |                 
563 |                 # Si el tiempo crece mucho más que linealmente
564 |                 if ratio_tiempo > ratio_tamaño * 2:
565 |                     alertas.append({
566 |                         'tipo': 'COMPLEJIDAD_ALTA',
567 |                         'nivel': 'warning',
568 |                         'icono': 'WARNING',
569 |                         'mensaje': f'Crecimiento no lineal: N={size_anterior}→{size_actual}, tiempo crece {ratio_tiempo:.1f}x (esperado ~{ratio_tamaño:.1f}x)',
570 |                         'tamaños': [size_anterior, size_actual]
571 |                     })
572 |                 
573 |                 # Si el tiempo supera 1 segundo
574 |                 if tiempo_actual > 1000:
575 |                     alertas.append({
576 |                         'tipo': 'TIEMPO_CRITICO',
577 |                         'nivel': 'error',
578 |                         'icono': 'CRITICAL',
579 |                         'mensaje': f'Tiempo crítico en N={size_actual}: {tiempo_actual:.0f}ms (>1s)',
580 |                         'tamaño': size_actual
581 |                     })
582 |     
583 |     # Alertas de memoria
584 |     max_memoria = max(valores_memoria) if valores_memoria else 0
585 |     if max_memoria > 100:
586 |         alertas.append({
587 |             'tipo': 'MEMORIA_ALTA',
588 |             'nivel': 'warning',
589 |             'icono': 'MEMORY',
590 |             'mensaje': f'Consumo de memoria elevado: {max_memoria:.1f} MB',
591 |             'valor_mb': max_memoria
592 |         })
593 |     
594 |     # Estimar complejidad basándose en el patrón de crecimiento
595 |     if len(valores_tiempo) >= 3:
596 |         ratios = []
597 |         for i in range(1, len(valores_tiempo)):
598 |             if valores_tiempo[i-1] > 0:
599 |                 ratios.append(valores_tiempo[i] / valores_tiempo[i-1])
600 |         
601 |         promedio_ratio = sum(ratios) / len(ratios) if ratios else 1
602 |         
603 |         if promedio_ratio > 10:
604 |             alertas.append({
605 |                 'tipo': 'COMPLEJIDAD_ESTIMADA',
606 |                 'nivel': 'info',
607 |                 'icono': 'INFO',
608 |                 'mensaje': f'Complejidad estimada: O(N³) o peor (ratio promedio: {promedio_ratio:.1f}x)',
609 |                 'ratio': promedio_ratio
610 |             })
611 |         elif promedio_ratio > 2.5:
612 |             alertas.append({
613 |                 'tipo': 'COMPLEJIDAD_ESTIMADA',
614 |                 'nivel': 'info',
615 |                 'icono': 'INFO',
616 |                 'mensaje': f'Complejidad estimada: O(N²) (ratio promedio: {promedio_ratio:.1f}x)',
617 |                 'ratio': promedio_ratio
618 |             })
619 |     
620 |     return alertas
621 | 
622 | 
623 | def resumir_analisis_md(contenido_md, max_puntos=5):
624 |     """Extrae y resume los puntos clave del análisis MD.
625 |     
626 |     Args:
627 |         contenido_md: Contenido del archivo markdown
628 |         max_puntos: Máximo número de puntos clave a extraer
629 |     
630 |     Returns:
631 |         dict con resumen estructurado
632 |     """
633 |     resumen = {
634 |         'titulo': '',
635 |         'puntos_clave': [],
636 |         'cuellos_botella': [],
637 |         'recomendaciones': [],
638 |         'metricas': {}
639 |     }
640 |     
641 |     lineas = contenido_md.split('\n')
642 |     
643 |     # Extraer título principal
644 |     for linea in lineas:
645 |         if linea.startswith('# '):
646 |             resumen['titulo'] = linea.replace('# ', '').strip()
647 |             break
648 |     
649 |     # Extraer secciones principales
650 |     seccion_actual = None
651 |     buffer = []
652 |     
653 |     for linea in lineas:
654 |         if linea.startswith('## '):
655 |             # Procesar sección anterior
656 |             if seccion_actual and buffer:
657 |                 texto = '\n'.join(buffer).strip()
658 |                 if seccion_actual == 'CUELLOS DE BOTELLA':
659 |                     # Extraer problemas marcados con [CRITICAL]
660 |                     if '[CRITICAL]' in texto:
661 |                         problemas = re.findall(r'\[CRITICAL\].*?(?=\[CRITICAL\]|$)', texto, re.DOTALL)
662 |                         for p in problemas:
663 |                             linea_problema = p.strip().split('\n')[0]
664 |                             resumen['cuellos_botella'].append(linea_problema.replace('[CRITICAL]', '').strip())
665 |                 elif seccion_actual == 'RECOMENDACIONES':
666 |                     # Extraer recomendaciones numeradas
667 |                     recs = re.findall(r'\d+\.\s+(.*?)(?=\d+\.|$)', texto, re.DOTALL)
668 |                     for r in recs[:max_puntos]:
669 |                         resumen['recomendaciones'].append(r.strip().split('\n')[0])
670 |             
671 |             seccion_actual = linea.replace('## ', '').strip().split(' ')[0]
672 |             buffer = []
673 |         else:
674 |             buffer.append(linea)
675 |     
676 |     # Extraer complejidades
677 |     complejidades = re.findall(r'O\([^)]+\)', contenido_md)
678 |     resumen['metricas']['complejidades_encontradas'] = list(set(complejidades))
679 |     
680 |     # Si no encontramos suficientes puntos clave, extraer del resumen general
681 |     if not resumen['puntos_clave']:
682 |         # Buscar líneas que empiezan con "**" o "- "
683 |         for linea in lineas:
684 |             if (linea.startswith('**') or linea.startswith('- ')) and len(resumen['puntos_clave']) < max_puntos:
685 |                 punto = linea.replace('**', '').replace('- ', '').strip()
686 |                 if punto and len(punto) > 10:
687 |                     resumen['puntos_clave'].append(punto[:100] + '...' if len(punto) > 100 else punto)
688 |     
689 |     return resumen
690 | 
691 | 
692 | @app.route('/api/integrar-watsonx', methods=['POST'])
693 | def integrar_watsonx():
694 |     """Integra análisis de Bob IDE + benchmarks con watsonx.ai."""
695 |     try:
696 |         data = request.get_json()
697 |         
698 |         if not data or 'bob_analysis_file' not in data:
699 |             return jsonify({"error": "Falta campo 'bob_analysis_file'"}), 400
700 |         
701 |         bob_file = data['bob_analysis_file']
702 |         codigo = data.get('codigo', '')
703 |         
704 |         # Cargar análisis de Bob
705 |         bob_path = BOB_SESSIONS_DIR / bob_file
706 |         if not bob_path.exists():
707 |             return jsonify({"error": f"Archivo Bob no encontrado: {bob_file}"}), 404
708 |         
709 |         bob_analysis = bob_path.read_text(encoding='utf-8')
710 |         
711 |         # Cargar métricas locales
712 |         metricas_path = DATA_DIR / "metricas_salida.json"
713 |         metricas = {}
714 |         if metricas_path.exists():
715 |             metricas = json.loads(metricas_path.read_text(encoding='utf-8'))
716 |         
717 |         # Enviar a watsonx.ai
718 |         print("Integrando con watsonx.ai...")
719 |         resultado_watsonx = summarize_metrics(bob_analysis)
720 |         
721 |         # Generar reporte final
722 |         reporte_final = f"""# REPORTE FINAL QA - OptiCode
723 | 
724 | ## Analisis de Bob IDE
725 | 
726 | {bob_analysis}
727 | 
728 | ---
729 | 
730 | ## Metricas Practicas (Motor Local)
731 | 
732 | ```json
733 | {json.dumps(metricas, indent=2)}
734 | ```
735 | 
736 | ---
737 | 
738 | ## Resumen de watsonx.ai
739 | 
740 | {resultado_watsonx if resultado_watsonx else "Integración aún no configurada."}
741 | 
742 | ---
743 | 
744 | **Generado automáticamente por OptiCode QA**
745 | **Fecha:** {datetime.now().isoformat()}
746 | """
747 |         
748 |         # Guardar reporte
749 |         reporte_path = OUTPUT_DIR / "REPORTE_FINAL_QA.md"
750 |         reporte_path.write_text(reporte_final, encoding='utf-8')
751 |         
752 |         return jsonify({
753 |             "success": True,
754 |             "mensaje": "Integracion completada exitosamente",
755 |             "archivo_reporte": str(reporte_path),
756 |             "resumen_watsonx": resultado_watsonx or "Resumen disponible después de integración completa"
757 |         })
758 |     
759 |     except Exception as e:
760 |         return jsonify({
761 |             "success": False,
762 |             "error": f"Error en integracion: {str(e)}",
763 |             "traceback": traceback.format_exc()
764 |         }), 500
765 | 
766 | 
767 | @app.route('/api/reportes', methods=['GET'])
768 | def listar_reportes():
769 |     """Lista reportes finales generados."""
770 |     try:
771 |         reportes = []
772 |         
773 |         if OUTPUT_DIR.exists():
774 |             for archivo in sorted(OUTPUT_DIR.glob('*.md')):
775 |                 contenido = archivo.read_text(encoding='utf-8')
776 |                 reportes.append({
777 |                     "nombre": archivo.name,
778 |                     "contenido_preview": contenido[:300],
779 |                     "tamaño": len(contenido)
780 |                 })
781 |         
782 |         return jsonify({
783 |             "success": True,
784 |             "total": len(reportes),
785 |             "reportes": reportes
786 |         })
787 |     
788 |     except Exception as e:
789 |         return jsonify({"success": False, "error": str(e)}), 500
790 | 
791 | 
792 | @app.route('/api/reportes/<nombre>', methods=['GET'])
793 | def descargar_reporte(nombre):
794 |     """Descarga un reporte específico."""
795 |     try:
796 |         ruta = OUTPUT_DIR / nombre
797 |         
798 |         if not ruta.exists():
799 |             return jsonify({"error": f"Reporte no encontrado: {nombre}"}), 404
800 |         
801 |         contenido = ruta.read_text(encoding='utf-8')
802 |         
803 |         return jsonify({
804 |             "success": True,
805 |             "nombre": nombre,
806 |             "contenido": contenido
807 |         })
808 |     
809 |     except Exception as e:
810 |         return jsonify({"success": False, "error": str(e)}), 500
811 | 
812 | 
813 | @app.route('/api/estado', methods=['GET'])
814 | def estado():
815 |     """Devuelve estado del sistema."""
816 |     try:
817 |         bob_files = len(list(BOB_SESSIONS_DIR.glob('*.md')))
818 |         reportes = len(list(OUTPUT_DIR.glob('*.md')))
819 |         metricas_existe = (DATA_DIR / "metricas_salida.json").exists()
820 |         
821 |         return jsonify({
822 |             "success": True,
823 |             "sistema": "OptiCode QA — PASO 1 Real",
824 |             "estado": "Operacional",
825 |             "archivos_bob": bob_files,
826 |             "reportes_generados": reportes,
827 |             "metricas_disponibles": metricas_existe,
828 |             "timestamp": datetime.now().isoformat()
829 |         })
830 |     
831 |     except Exception as e:
832 |         return jsonify({"success": False, "error": str(e)}), 500
833 | 
834 | 
835 | if __name__ == '__main__':
836 |     print("\n" + "=" * 70)
837 |     print("SERVIDOR OptiCode QA - PASO 1 REAL")
838 |     print("=" * 70)
839 |     print("\nFlujo: Bob IDE (manual) -> Motor Local -> watsonx.ai")
840 |     print("\nDashboard disponible en: http://localhost:5000")
841 |     print("\nAPI Endpoints:")
842 |     print("   GET  /api/bob-sessions - Lista análisis de Bob IDE")
843 |     print("   GET  /api/codigos - Lista códigos disponibles")
844 |     print("   POST /api/analizar-codigo-personalizado - Analiza código pegado")
845 |     print("   POST /api/ejecutar-benchmarks - Ejecuta benchmarks")
846 |     print("   POST /api/integrar-watsonx - Integra y genera reporte")
847 |     print("   GET  /api/reportes - Lista reportes finales")
848 |     print("   GET  /api/estado - Estado del sistema")
849 |     print("\n" + "=" * 70 + "\n")
850 |     
851 |     app.run(debug=True, host='localhost', port=5000)
</content>
</file>
<file><path>src/motor_qa.py</path>
<content lines="1-109">
  1 | """Motor local de QA — lógica de Alex integrada con la GUI de Harry.
  2 | 
  3 | Mide tiempo de ejecución y uso de memoria para DFS, LDFS e IDFS.
  4 | Genera data/metricas_salida.json compatible con el dashboard de Harry.
  5 | """
  6 | import json
  7 | import time
  8 | import tracemalloc
  9 | import sys
 10 | from pathlib import Path
 11 | from statistics import mean
 12 | 
 13 | # Configuración automática de rutas (patrón de Alex)
 14 | RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
 15 | if str(RAIZ_PROYECTO) not in sys.path:
 16 |     sys.path.insert(0, str(RAIZ_PROYECTO))
 17 | 
 18 | from src.algoritmos import dfs_puro, ldfs, idfs
 19 | 
 20 | DATA_DIR = RAIZ_PROYECTO / 'data'
 21 | OUT_FILE = DATA_DIR / 'metricas_salida.json'
 22 | 
 23 | 
 24 | # =========================================================================
 25 | # SISTEMA DE MEDICIÓN DE RENDIMIENTO (BENCHMARK) — de Alex
 26 | # =========================================================================
 27 | def measure_func(func, *args, repeats=3):
 28 |     """Mide tiempo (ms) y memoria (bytes) de una función en N repeticiones."""
 29 |     times = []
 30 |     peaks = []
 31 |     for _ in range(repeats):
 32 |         tracemalloc.start()
 33 |         t0 = time.perf_counter()
 34 |         func(*args)
 35 |         t1 = time.perf_counter()
 36 |         current, peak = tracemalloc.get_traced_memory()
 37 |         tracemalloc.stop()
 38 |         times.append((t1 - t0) * 1000)  # ms
 39 |         peaks.append(peak)
 40 |     return {
 41 |         'time_ms_mean': round(mean(times), 4),
 42 |         'time_ms_samples': [round(t, 4) for t in times],
 43 |         'mem_bytes_peak_mean': int(mean(peaks)),
 44 |         'mem_bytes_peak_samples': peaks
 45 |     }
 46 | 
 47 | 
 48 | # =========================================================================
 49 | # EJECUCIÓN PRINCIPAL DEL STRESS TEST — estructura de Alex, datos de Harry
 50 | # =========================================================================
 51 | def run_benchmarks():
 52 |     """Ejecuta benchmarks para DFS, LDFS e IDFS y guarda métricas en JSON."""
 53 |     graph_file = DATA_DIR / 'grafos_prueba.json'
 54 | 
 55 |     if not graph_file.exists():
 56 |         print(f'Error: No se encontro el archivo de datos en: {graph_file}')
 57 |         return
 58 | 
 59 |     with open(graph_file, 'r', encoding='utf-8') as f:
 60 |         graph = json.load(f)
 61 | 
 62 |     print("Iniciando Motor de Pruebas de Estres...")
 63 | 
 64 |     nodo_inicial = list(graph.keys())[0]
 65 |     nodo_final = list(graph.keys())[-1]
 66 | 
 67 |     sizes = [10, 100, 1000, 5000]
 68 |     results = {}
 69 | 
 70 |     for N in sizes:
 71 |         print(f"   -> Evaluando carga simulada N = {N}...")
 72 |         repeticiones = max(1, N // 10)
 73 | 
 74 |         # DFS puro
 75 |         res_dfs = measure_func(
 76 |             lambda: [dfs_puro(graph, nodo_inicial, nodo_final) for _ in range(repeticiones)]
 77 |         )
 78 | 
 79 |         # LDFS con límite razonable (profundidad del grafo ~6)
 80 |         res_ldfs = measure_func(
 81 |             lambda: [ldfs(graph, nodo_inicial, nodo_final, 6) for _ in range(repeticiones)]
 82 |         )
 83 | 
 84 |         # IDFS con límite máximo razonable
 85 |         res_idfs = measure_func(
 86 |             lambda: [idfs(graph, nodo_inicial, nodo_final, 6) for _ in range(repeticiones)]
 87 |         )
 88 | 
 89 |         results[N] = {
 90 |             'dfs':  res_dfs,
 91 |             'ldfs': res_ldfs,
 92 |             'idfs': res_idfs,
 93 |             # Compatibilidad con el parser del servidor de Harry:
 94 |             # usa los valores de DFS como métricas "generales"
 95 |             'time_ms_mean':         res_dfs['time_ms_mean'],
 96 |             'time_ms_samples':      res_dfs['time_ms_samples'],
 97 |             'mem_bytes_peak_mean':  res_dfs['mem_bytes_peak_mean'],
 98 |             'mem_bytes_peak_samples': res_dfs['mem_bytes_peak_samples'],
 99 |         }
100 | 
101 |     DATA_DIR.mkdir(parents=True, exist_ok=True)
102 |     with open(OUT_FILE, 'w', encoding='utf-8') as f:
103 |         json.dump({'benchmarks': results}, f, indent=2)
104 | 
105 |     print(f'\nProceso terminado! Resultados guardados en: {OUT_FILE}')
106 | 
107 | 
108 | if __name__ == '__main__':
109 |     run_benchmarks()
</content>
</file>
<file><path>src/integrador_watsonx.py</path>
<content lines="1-139">
  1 | """Integrador con watsonx.ai — lógica completa de Alex adaptada para la GUI de Harry.
  2 | 
  3 | Cruza el análisis teórico de Bob IDE con las métricas del motor QA
  4 | y genera un veredicto final usando IBM watsonx.ai (Llama 3.3 70B).
  5 | """
  6 | import json
  7 | import sys
  8 | from pathlib import Path
  9 | 
 10 | # Configuración de rutas
 11 | RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
 12 | DATA_DIR = RAIZ_PROYECTO / 'data'
 13 | BOB_SESSIONS_DIR = RAIZ_PROYECTO / 'output' / 'informesbob'
 14 | 
 15 | # =========================================================================
 16 | # CREDENCIALES — configuradas por Alex para el sandbox IBM pre-conectado
 17 | # También se admite override desde variables de entorno (.env)
 18 | # =========================================================================
 19 | try:
 20 |     from dotenv import load_dotenv
 21 |     import os
 22 |     load_dotenv()
 23 |     API_KEY    = os.getenv('WATSONX_API_KEY',    "r7N0t-5xbndvsYVshMeoE1Ax_SSbLrbAbh0UM6TrDgIu")
 24 |     PROJECT_ID = os.getenv('WATSONX_PROJECT_ID', "a4b3f3fe-9336-4169-8a54-d22d88de90a6")
 25 |     URL_ENDPOINT = os.getenv('WATSONX_URL',      "https://us-south.ml.cloud.ibm.com")
 26 | except ImportError:
 27 |     API_KEY      = "r7N0t-5xbndvsYVshMeoE1Ax_SSbLrbAbh0UM6TrDgIu"
 28 |     PROJECT_ID   = "a4b3f3fe-9336-4169-8a54-d22d88de90a6"
 29 |     URL_ENDPOINT = "https://us-south.ml.cloud.ibm.com"
 30 | 
 31 | 
 32 | # =========================================================================
 33 | # FUNCIÓN PRINCIPAL — llamada desde servidor_paso1_web.py de Harry
 34 | # Firma: summarize_metrics(bob_analysis_text: str) -> str | None
 35 | # =========================================================================
 36 | def summarize_metrics(bob_analysis_text: str) -> str | None:
 37 |     """Envía el análisis de Bob IDE + métricas locales a watsonx.ai y retorna el veredicto."""
 38 |     # Cargar métricas del motor QA
 39 |     metricas_path = DATA_DIR / 'metricas_salida.json'
 40 |     practica_json = {}
 41 |     if metricas_path.exists():
 42 |         with open(metricas_path, 'r', encoding='utf-8') as f:
 43 |             practica_json = json.load(f)
 44 | 
 45 |     # Construcción del prompt (igual que en Alex)
 46 |     prompt = f"""Actúa como un Ingeniero Principal de QA y DevOps en IBM Cloud.
 47 | Tu misión es generar un "Veredicto Final de Rendimiento y Escalabilidad Cloud" cruzando un análisis teórico con métricas reales de un stress test.
 48 | 
 49 | === 1. AUDITORÍA TEÓRICA DE COGNICIÓN (IBM Bob IDE) ===
 50 | {bob_analysis_text}
 51 | 
 52 | === 2. MÉTRICAS REALES DE RENDIMIENTO LOCAL (JSON) ===
 53 | {json.dumps(practica_json, indent=2)}
 54 | 
 55 | === INSTRUCCIONES DE REDACCIÓN ===
 56 | 1. **Validación Cruzada:** Determina si los tiempos promedios reales (time_ms_mean) del JSON concuerdan asintóticamente con la complejidad teórica Big O descrita.
 57 | 2. **Comparación DFS vs LDFS vs IDFS:** Si existen métricas diferenciadas, compara el comportamiento de los tres algoritmos.
 58 | 3. **Impacto Cloud:** Explica cómo afectaría a la RAM en producción según los picos medidos (mem_bytes_peak_mean) en un entorno de tráfico masivo.
 59 | 4. **Conclusión General:** Da una calificación de escalabilidad (Aprobado / No Aprobado) y una recomendación clave.
 60 | 
 61 | Por favor, genera tu respuesta en un formato Markdown impecable y ejecutivo.
 62 | """
 63 | 
 64 |     try:
 65 |         from ibm_watsonx_ai import APIClient
 66 |         from ibm_watsonx_ai.foundation_models import ModelInference
 67 | 
 68 |         credentials = {"url": URL_ENDPOINT, "apikey": API_KEY}
 69 | 
 70 |         model = ModelInference(
 71 |             model_id = "ibm/granite-8b-code-instruct",
 72 |             params={
 73 |                 "decoding_method": "greedy",
 74 |                 "max_new_tokens": 1000,
 75 |                 "repetition_penalty": 1.0
 76 |             },
 77 |             credentials=credentials,
 78 |             project_id=PROJECT_ID
 79 |         )
 80 | 
 81 |         print("Conectando con watsonx.ai (Llama 3.3 70B)...")
 82 |         resultado = model.generate_text(prompt=prompt)
 83 | 
 84 |         # Guardar veredicto en data/
 85 |         ruta_salida = DATA_DIR / 'veredicto_final_auditoria.md'
 86 |         ruta_salida.write_text(resultado, encoding='utf-8')
 87 |         print(f"Veredicto guardado en: {ruta_salida}")
 88 | 
 89 |         return resultado
 90 | 
 91 |     except ImportError:
 92 |         print("WARNING: ibm-watsonx-ai no instalado. Retornando resumen simulado.")
 93 |         return _resumen_simulado(practica_json)
 94 |     except Exception as e:
 95 |         print(f"Error en watsonx.ai: {e}")
 96 |         return _resumen_simulado(practica_json)
 97 | 
 98 | 
 99 | def _resumen_simulado(practica_json: dict) -> str:
100 |     """Genera un resumen local cuando watsonx no está disponible."""
101 |     benchmarks = practica_json.get('benchmarks', {})
102 |     lineas = ["## Resumen Local (watsonx no disponible)\n"]
103 |     for size, m in sorted(benchmarks.items(), key=lambda x: int(x[0])):
104 |         t = m.get('time_ms_mean', m.get('dfs', {}).get('time_ms_mean', 0))
105 |         mem = m.get('mem_bytes_peak_mean', m.get('dfs', {}).get('mem_bytes_peak_mean', 0))
106 |         lineas.append(f"- **N={size}**: tiempo promedio `{t:.4f} ms`, memoria pico `{mem // 1024} KB`")
107 |     lineas.append("\n> Configura `ibm-watsonx-ai` para el análisis completo con IA.")
108 |     return "\n".join(lineas)
109 | 
110 | 
111 | # =========================================================================
112 | # EJECUCIÓN DIRECTA (opcional, igual que en Alex)
113 | # =========================================================================
114 | def generar_veredicto_final():
115 |     """Ejecuta la integración completa desde línea de comandos."""
116 |     # Buscar reporte teórico
117 |     ruta_teoria = None
118 |     for ruta in [RAIZ_PROYECTO / 'reporte_analisis_algoritmo.md',
119 |                  *list(BOB_SESSIONS_DIR.glob('*.md')),
120 |                  *list(RAIZ_PROYECTO.glob('*.md'))]:
121 |         if ruta.exists() and 'README' not in ruta.name:
122 |             ruta_teoria = ruta
123 |             break
124 | 
125 |     if not ruta_teoria:
126 |         print("Error: No se encontro reporte teorico (.md). Genera uno primero.")
127 |         sys.exit(1)
128 | 
129 |     print(f"Leyendo reporte teorico: {ruta_teoria.name}")
130 |     teoria = ruta_teoria.read_text(encoding='utf-8')
131 | 
132 |     resultado = summarize_metrics(teoria)
133 |     if resultado:
134 |         print("\n--- VEREDICTO ---\n")
135 |         print(resultado[:500], "...\n(ver archivo completo en data/veredicto_final_auditoria.md)")
136 | 
137 | 
138 | if __name__ == '__main__':
139 |     generar_veredicto_final()
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
.gitignore

# VSCode Open Tabs
templates/dashboard.html,src/servidor_paso1_web.py,.gitignore,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:54:11.155Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Entiendo que necesitas mejorar el PDF con colores corporativos azul marino y mejor legibilidad. Primero necesito ver el código del dashboard para entender cómo se genera el PDF actualmente.

<read_file>
<args>
<file>
<path>templates/dashboard.html</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'templates/dashboard.html'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>templates/dashboard.html</path><file_outline>File: dashboard.html (2629 lines)

Fields: html
</file_outline>
<notice>This file is large (2628 lines). You will use the following strategy to understand this file:
- Inform the user you are going to use large file strategy, to efficiently understand the file
- Use the file_outline provided to get an overview of the file structure to help decide next action. This is not the full file. It is not the full depth of the contents.
- If you read the file, use precise file reads with line ranges for specific sections of interest
- Consider if other commands/tools are better suited for extracting information from that file type
- Use ask_followup_question tool if needed to identify the best next action
</notice></file>
</files>
<environment_details>
# VSCode Visible Files
.gitignore

# VSCode Open Tabs
templates/dashboard.html,src/servidor_paso1_web.py,.gitignore,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:54:27.234Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Voy a usar una estrategia de lectura eficiente para este archivo grande. Necesito buscar la sección donde se genera el PDF para entender cómo mejorarlo con colores corporativos azul marino.

<search_files>
<path>templates/dashboard.html</path>
<regex>(jsPDF|pdf|generatePDF|exportar.*pdf)</regex>
</search_files>

---

**User:**

[search_files for '(jsPDF|pdf|generatePDF|exportar.*pdf)'] Result:
Found 6 results.

# templates/dashboard.html
 11 |     <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
 12 |     <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
 13 |     <style>
----
376 | 
377 |       .sidebar-button.btn-pdf {
378 |         background: linear-gradient(
----
384 | 
385 |       .sidebar-button.btn-pdf:hover:not(:disabled) {
386 |         box-shadow: 0 0 20px rgba(245, 169, 98, 0.4);
----
1088 |           <button
1089 |             class="sidebar-button btn-pdf"
1090 |             id="reporteBtn"
----
2189 |         try {
2190 |           const { jsPDF } = window.jspdf;
2191 |           const doc = new jsPDF({ unit: "mm", format: "a4" });
2192 |           const W = 210,
----
2616 |             .slice(0, 16);
2617 |           doc.save(`OptiCode_QA_Reporte_${ts}.pdf`);
2618 |           log("✅ PDF generado y descargado exitosamente", "success");
----
<environment_details>
# VSCode Visible Files
.gitignore

# VSCode Open Tabs
templates/dashboard.html,src/servidor_paso1_web.py,.gitignore,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:54:33.030Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.11

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Perfecto, encontré la sección del PDF. Ahora voy a leer esa parte específica para ver cómo se genera actualmente:

<read_file>
<args>
<file>
<path>templates/dashboard.html</path>
<line_range>2180-2620</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'templates/dashboard.html'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>templates/dashboard.html</path>
<content lines="2180-2620">
2180 | 
2181 |       // ── Generar PDF ───────────────────────────────────────────────────────────
2182 |       async function descargarPDF() {
2183 |         document.getElementById("spinnerOverlay").classList.add("active");
2184 |         log("📥 Generando PDF…", "info");
2185 | 
2186 |         // Esperar un tick para que el spinner se pinte
2187 |         await new Promise((r) => setTimeout(r, 80));
2188 | 
2189 |         try {
2190 |           const { jsPDF } = window.jspdf;
2191 |           const doc = new jsPDF({ unit: "mm", format: "a4" });
2192 |           const W = 210,
2193 |             margin = 14;
2194 |           let y = 0;
2195 | 
2196 |           // ── Paleta ────────────────────────────────────────────────────────
2197 |           const BLUE = [78, 163, 184];
2198 |           const DARK = [237, 244, 251];
2199 |           const GRAY = [169, 183, 200];
2200 |           const LGRAY = [45, 58, 76];
2201 |           const GREEN = [78, 163, 184];
2202 |           const ORANGE = [224, 138, 60];
2203 |           const RED = [240, 139, 126];
2204 |           const WHITE = [255, 255, 255];
2205 | 
2206 |           // ── Portada ───────────────────────────────────────────────────────
2207 |           doc.setFillColor(...BLUE);
2208 |           doc.rect(0, 0, W, 55, "F");
2209 | 
2210 |           doc.setTextColor(...WHITE);
2211 |           doc.setFont("helvetica", "bold");
2212 |           doc.setFontSize(22);
2213 |           doc.text("OPTICODE QA", margin, 22);
2214 | 
2215 |           doc.setFontSize(11);
2216 |           doc.setFont("helvetica", "normal");
2217 |           doc.text(
2218 |             "Panel del Auditor - Reporte de Analisis de Rendimiento",
2219 |             margin,
2220 |             31,
2221 |           );
2222 | 
2223 |           doc.setFontSize(9);
2224 |           const fecha = new Date().toLocaleString("es-ES", {
2225 |             dateStyle: "long",
2226 |             timeStyle: "short",
2227 |           });
2228 |           doc.text(`Generado: ${fecha}`, margin, 40);
2229 | 
2230 |           const archivoCodigo = fuenteCodigoActual || "N/A";
2231 |           const archivoAnalisis =
2232 |             document.getElementById("bobAnalysisSelect").value || "N/A";
2233 |           doc.text(
2234 |             `Código analizado: ${archivoCodigo}   |   Analisis Bob: ${archivoAnalisis}`,
2235 |             margin,
2236 |             47,
2237 |           );
2238 | 
2239 |           y = 65;
2240 | 
2241 |           // ── Función helpers ───────────────────────────────────────────────
2242 |           function checkPage(needed = 20) {
2243 |             if (y + needed > 280) {
2244 |               doc.addPage();
2245 |               y = 15;
2246 |             }
2247 |           }
2248 | 
2249 |           function sectionTitle(txt) {
2250 |             checkPage(14);
2251 |             doc.setFillColor(...BLUE);
2252 |             doc.rect(margin, y, W - margin * 2, 8, "F");
2253 |             doc.setTextColor(...WHITE);
2254 |             doc.setFont("helvetica", "bold");
2255 |             doc.setFontSize(9);
2256 |             doc.text(txt.toUpperCase(), margin + 3, y + 5.5);
2257 |             y += 12;
2258 |             doc.setTextColor(...DARK);
2259 |           }
2260 | 
2261 |           function rowBg(i) {
2262 |             return i % 2 === 0 ? [249, 250, 251] : WHITE;
2263 |           }
2264 | 
2265 |           // ── Sección 0: Resumen del Análisis ───────────────────────────────
2266 |           if (resumenActual) {
2267 |             sectionTitle("[RESUMEN] Analisis Bob IDE");
2268 | 
2269 |             if (resumenActual.titulo) {
2270 |               doc.setFont("helvetica", "bold");
2271 |               doc.setFontSize(9);
2272 |               doc.setTextColor(...DARK);
2273 |               doc.text(`Analisis: ${resumenActual.titulo}`, margin, y);
2274 |               y += 6;
2275 |             }
2276 | 
2277 |             // Puntos clave
2278 |             if (
2279 |               resumenActual.puntos_clave &&
2280 |               resumenActual.puntos_clave.length > 0
2281 |             ) {
2282 |               doc.setFont("helvetica", "bold");
2283 |               doc.setFontSize(8);
2284 |               doc.setTextColor(...BLUE);
2285 |               doc.text("[OK] Puntos Clave:", margin, y);
2286 |               y += 4;
2287 | 
2288 |               resumenActual.puntos_clave.slice(0, 3).forEach((punto) => {
2289 |                 checkPage(6);
2290 |                 doc.setFont("helvetica", "normal");
2291 |                 doc.setFontSize(7.5);
2292 |                 doc.setTextColor(...DARK);
2293 |                 const lineas = doc.splitTextToSize(
2294 |                   `- ${punto}`,
2295 |                   W - margin * 2 - 4,
2296 |                 );
2297 |                 doc.text(lineas[0] || "", margin + 2, y);
2298 |                 y += 5;
2299 |               });
2300 |               y += 2;
2301 |             }
2302 | 
2303 |             // Cuellos de botella
2304 |             if (
2305 |               resumenActual.cuellos_botella &&
2306 |               resumenActual.cuellos_botella.length > 0
2307 |             ) {
2308 |               doc.setFont("helvetica", "bold");
2309 |               doc.setFontSize(8);
2310 |               doc.setTextColor(...RED);
2311 |               doc.text("[CRITICO] Cuellos de Botella:", margin, y);
2312 |               y += 4;
2313 | 
2314 |               resumenActual.cuellos_botella.slice(0, 3).forEach((cuello) => {
2315 |                 checkPage(6);
2316 |                 doc.setFont("helvetica", "normal");
2317 |                 doc.setFontSize(7.5);
2318 |                 doc.setTextColor(...DARK);
2319 |                 const lineas = doc.splitTextToSize(
2320 |                   `- ${cuello}`,
2321 |                   W - margin * 2 - 4,
2322 |                 );
2323 |                 doc.text(lineas[0] || "", margin + 2, y);
2324 |                 y += 5;
2325 |               });
2326 |               y += 2;
2327 |             }
2328 | 
2329 |             // Recomendaciones
2330 |             if (
2331 |               resumenActual.recomendaciones &&
2332 |               resumenActual.recomendaciones.length > 0
2333 |             ) {
2334 |               doc.setFont("helvetica", "bold");
2335 |               doc.setFontSize(8);
2336 |               doc.setTextColor(...GREEN);
2337 |               doc.text("[RECOMENDACION] Propuestas:", margin, y);
2338 |               y += 4;
2339 | 
2340 |               resumenActual.recomendaciones.slice(0, 3).forEach((rec) => {
2341 |                 checkPage(6);
2342 |                 doc.setFont("helvetica", "normal");
2343 |                 doc.setFontSize(7.5);
2344 |                 doc.setTextColor(...DARK);
2345 |                 const lineas = doc.splitTextToSize(
2346 |                   `- ${rec}`,
2347 |                   W - margin * 2 - 4,
2348 |                 );
2349 |                 doc.text(lineas[0] || "", margin + 2, y);
2350 |                 y += 5;
2351 |               });
2352 |               y += 4;
2353 |             }
2354 | 
2355 |             // Complejidades
2356 |             if (
2357 |               resumenActual.metricas &&
2358 |               resumenActual.metricas.complejidades_encontradas
2359 |             ) {
2360 |               doc.setFont("helvetica", "bold");
2361 |               doc.setFontSize(7.5);
2362 |               doc.setTextColor(...DARK);
2363 |               const complejos =
2364 |                 resumenActual.metricas.complejidades_encontradas.join(" | ");
2365 |               doc.text(`Complejidades: ${complejos}`, margin, y);
2366 |               y += 6;
2367 |             }
2368 | 
2369 |             y += 4;
2370 |           }
2371 | 
2372 |           // ── Sección 1: Métricas Detalladas ────────────────────────────────
2373 |           sectionTitle("[METRICAS] Detalles de Rendimiento");
2374 | 
2375 |           const sizes = Object.keys(metricsData).sort(
2376 |             (a, b) => parseInt(a) - parseInt(b),
2377 |           );
2378 | 
2379 |           // Cabecera tabla
2380 |           const cols = [
2381 |             "Tamaño N",
2382 |             "DFS (ms)",
2383 |             "LDFS (ms)",
2384 |             "IDFS (ms)",
2385 |             "Mem DFS (MB)",
2386 |           ];
2387 |           const colW = [30, 38, 38, 38, 42];
2388 |           const colX = [margin];
2389 |           colW.forEach((w, i) => {
2390 |             if (i > 0) colX.push(colX[i - 1] + colW[i - 1]);
2391 |           });
2392 | 
2393 |           doc.setFillColor(...LGRAY);
2394 |           doc.rect(margin, y, W - margin * 2, 8, "F");
2395 |           doc.setFont("helvetica", "bold");
2396 |           doc.setFontSize(8);
2397 |           doc.setTextColor(...DARK);
2398 |           cols.forEach((c, i) => doc.text(c, colX[i] + 2, y + 5.5));
2399 |           y += 9;
2400 | 
2401 |           sizes.forEach((size, ri) => {
2402 |             checkPage(9);
2403 |             const m = metricsData[size];
2404 | 
2405 |             function tv(algo) {
2406 |               return m[algo]?.time_ms_mean !== undefined
2407 |                 ? m[algo].time_ms_mean.toFixed(2)
2408 |                 : (m.time_ms || 0).toFixed(2);
2409 |             }
2410 |             function mv(algo) {
2411 |               return m[algo]?.mem_bytes_peak_mean !== undefined
2412 |                 ? (m[algo].mem_bytes_peak_mean / (1024 * 1024)).toFixed(3)
2413 |                 : (m.memory_mb || 0).toFixed(3);
2414 |             }
2415 |             function colorNum(v) {
2416 |               const n = parseFloat(v);
2417 |               return n > 1000 ? RED : n > 100 ? ORANGE : GREEN;
2418 |             }
2419 | 
2420 |             doc.setFillColor(...rowBg(ri));
2421 |             doc.rect(margin, y, W - margin * 2, 8, "F");
2422 |             doc.setFont("helvetica", "bold");
2423 |             doc.setFontSize(8);
2424 |             doc.setTextColor(...DARK);
2425 |             doc.text(`N = ${size}`, colX[0] + 2, y + 5.5);
2426 | 
2427 |             const vals = [tv("dfs"), tv("ldfs"), tv("idfs"), mv("dfs")];
2428 |             vals.forEach((v, i) => {
2429 |               doc.setTextColor(...colorNum(i < 3 ? v : "0"));
2430 |               doc.setFont("helvetica", "normal");
2431 |               doc.text(v, colX[i + 1] + 2, y + 5.5);
2432 |             });
2433 |             y += 9;
2434 |           });
2435 | 
2436 |           y += 6;
2437 | 
2438 |           // ── Sección 2: Alertas ────────────────────────────────────────────
2439 |           sectionTitle(`[ALERTAS] Detectadas (${alertasActuales.length})`);
2440 | 
2441 |           if (alertasActuales.length === 0) {
2442 |             doc.setFont("helvetica", "italic");
2443 |             doc.setFontSize(9);
2444 |             doc.setTextColor(...GRAY);
2445 |             doc.text(
2446 |               "Sin alertas. Rendimiento dentro de parametros normales.",
2447 |               margin,
2448 |               y,
2449 |             );
2450 |             y += 10;
2451 |           } else {
2452 |             alertasActuales.forEach((a, i) => {
2453 |               checkPage(18);
2454 |               const c =
2455 |                 a.nivel === "error"
2456 |                   ? RED
2457 |                   : a.nivel === "warning"
2458 |                     ? ORANGE
2459 |                     : BLUE;
2460 |               doc.setFillColor(...c);
2461 |               doc.rect(margin, y, 3, 14, "F");
2462 |               doc.setFillColor(...rowBg(i));
2463 |               doc.rect(margin + 3, y, W - margin * 2 - 3, 14, "F");
2464 | 
2465 |               doc.setFont("helvetica", "bold");
2466 |               doc.setFontSize(8);
2467 |               doc.setTextColor(...DARK);
2468 |               const tipoLimpio = a.tipo.replace(/[^a-zA-Z0-9_-]/g, "");
2469 |               doc.text(`[${tipoLimpio}]`, margin + 6, y + 5);
2470 |               doc.setFont("helvetica", "normal");
2471 |               doc.setFontSize(7.5);
2472 |               doc.setTextColor(...GRAY);
2473 |               const lineas = doc.splitTextToSize(
2474 |                 a.mensaje,
2475 |                 W - margin * 2 - 12,
2476 |               );
2477 |               doc.text(lineas[0], margin + 6, y + 11);
2478 |               y += 16;
2479 |             });
2480 |           }
2481 | 
2482 |           y += 4;
2483 | 
2484 |           // ── Sección 3: Gráficos ────────────────────────────────────────────
2485 |           sectionTitle("[GRAFICOS] Rendimiento");
2486 | 
2487 |           const chartT = document.getElementById("chartTiempo");
2488 |           const chartM = document.getElementById("chartMemoria");
2489 |           const imgT = chartT.toDataURL("image/png", 0.95);
2490 |           const imgMem = chartM.toDataURL("image/png", 0.95);
2491 |           const gW = (W - margin * 2 - 6) / 2;
2492 |           const gH = gW * 0.65;
2493 | 
2494 |           checkPage(gH + 6);
2495 |           doc.addImage(imgT, "PNG", margin, y, gW, gH);
2496 |           doc.addImage(imgMem, "PNG", margin + gW + 6, y, gW, gH);
2497 |           y += gH + 4;
2498 | 
2499 |           // Leyenda de colores
2500 |           doc.setFont("helvetica", "bold");
2501 |           doc.setFontSize(7.5);
2502 |           [
2503 |             ["DFS", BLUE],
2504 |             ["LDFS", ORANGE],
2505 |             ["IDFS", [159, 24, 83]],
2506 |           ].forEach(([lbl, clr], i) => {
2507 |             const lx = margin + i * 30;
2508 |             doc.setFillColor(...clr);
2509 |             doc.rect(lx, y + 1, 6, 4, "F");
2510 |             doc.setTextColor(...DARK);
2511 |             doc.text(lbl, lx + 8, y + 5);
2512 |           });
2513 |           y += 12;
2514 | 
2515 |           // ── Sección 4: Código analizado ───────────────────────────────────
2516 |           if (codigoActual) {
2517 |             checkPage(20);
2518 |             sectionTitle(`[CODIGO] Analizado: ${archivoCodigo}`);
2519 | 
2520 |             const lineas = codigoActual.split("\n").slice(0, 50);
2521 |             doc.setFont("courier", "normal");
2522 |             doc.setFontSize(7);
2523 |             doc.setTextColor(...DARK);
2524 | 
2525 |             lineas.forEach((linea, i) => {
2526 |               checkPage(6);
2527 |               if (i % 2 === 0) {
2528 |                 doc.setFillColor(245, 247, 250);
2529 |                 doc.rect(margin, y - 3, W - margin * 2, 5.5, "F");
2530 |               }
2531 |               doc.setTextColor(100, 100, 100);
2532 |               doc.text(String(i + 1).padStart(3, " "), margin + 1, y + 1.5);
2533 |               doc.setTextColor(...DARK);
2534 |               const cortada = doc.splitTextToSize(linea, W - margin * 2 - 12);
2535 |               doc.text(cortada[0] || "", margin + 10, y + 1.5);
2536 |               y += 5.5;
2537 |             });
2538 | 
2539 |             if (codigoActual.split("\n").length > 50) {
2540 |               checkPage(8);
2541 |               doc.setFont("helvetica", "italic");
2542 |               doc.setFontSize(7.5);
2543 |               doc.setTextColor(...GRAY);
2544 |               doc.text(
2545 |                 `... (se muestran las primeras 50 lineas de ${codigoActual.split("\n").length})`,
2546 |                 margin,
2547 |                 y + 4,
2548 |               );
2549 |               y += 10;
2550 |             }
2551 |           }
2552 | 
2553 |           // ── Sección 5: análisis del código pegado ───────────────────────
2554 |           if (analisisCodigoPersonalizado) {
2555 |             checkPage(18);
2556 |             sectionTitle("[CODIGO PERSONALIZADO] Métricas y alertas");
2557 | 
2558 |             doc.setFont("helvetica", "normal");
2559 |             doc.setFontSize(8.5);
2560 |             doc.setTextColor(...DARK);
2561 | 
2562 |             const analisis = analisisCodigoPersonalizado;
2563 |             const metricas = metricasCodigoPersonalizado || analisis.metricas || {};
2564 |             const alertas = alertasCodigoPersonalizado || analisis.alertas || [];
2565 | 
2566 |             const lineasResumen = [
2567 |               `Complejidad estimada: ${analisis.complejidad_estimada || 'N/D'}`,
2568 |               `Líneas: ${metricas.lineas_detectadas ?? 'N/D'} | Funciones: ${metricas.funciones_detectadas ?? 'N/D'}`,
2569 |               `Bucles: ${metricas.bucles_detectados ?? 'N/D'} | Profundidad máxima: ${metricas.profundidad_maxima_bucles ?? 'N/D'}`,
2570 |               `Recursiones: ${metricas.recursiones_detectadas ?? 'N/D'} | Comparaciones in/not in: ${metricas.comparaciones_in_detectadas ?? 'N/D'}`,
2571 |               `Factor de riesgo: ${metricas.factor_riesgo ?? 'N/D'}/100`,
2572 |             ];
2573 | 
2574 |             lineasResumen.forEach((texto) => {
2575 |               checkPage(5);
2576 |               doc.text(texto, margin, y);
2577 |               y += 4.8;
2578 |             });
2579 | 
2580 |             if (alertas.length > 0) {
2581 |               checkPage(8);
2582 |               doc.setFont("helvetica", "bold");
2583 |               doc.text("Alertas:", margin, y);
2584 |               y += 5;
2585 |               doc.setFont("helvetica", "normal");
2586 |               alertas.slice(0, 5).forEach((alerta) => {
2587 |                 checkPage(6);
2588 |                 const texto = `- ${alerta.icono || '•'} ${alerta.tipo || 'ALERTA'}: ${alerta.mensaje || ''}`;
2589 |                 doc.text(doc.splitTextToSize(texto, W - margin * 2), margin, y);
2590 |                 y += 5;
2591 |               });
2592 |             }
2593 |           }
2594 | 
2595 |           // ── Pie de página en todas las páginas ────────────────────────────
2596 |           const total = doc.getNumberOfPages();
2597 |           for (let p = 1; p <= total; p++) {
2598 |             doc.setPage(p);
2599 |             doc.setFillColor(...LGRAY);
2600 |             doc.rect(0, 290, W, 7, "F");
2601 |             doc.setFont("helvetica", "normal");
2602 |             doc.setFontSize(7);
2603 |             doc.setTextColor(...GRAY);
2604 |             doc.text(
2605 |               "OptiCode QA - Reporte de Auditoria de Algoritmos",
2606 |               margin,
2607 |               294.5,
2608 |             );
2609 |             doc.text(`Página ${p} / ${total}`, W - margin - 20, 294.5);
2610 |           }
2611 | 
2612 |           // ── Guardar ───────────────────────────────────────────────────────
2613 |           const ts = new Date()
2614 |             .toISOString()
2615 |             .replace(/[:.]/g, "-")
2616 |             .slice(0, 16);
2617 |           doc.save(`OptiCode_QA_Reporte_${ts}.pdf`);
2618 |           log("✅ PDF generado y descargado exitosamente", "success");
2619 |         } catch (e) {
2620 |           log(`❌ Error generando PDF: ${e.message}`, "error");
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
.gitignore

# VSCode Open Tabs
templates/dashboard.html,src/servidor_paso1_web.py,.gitignore,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:54:48.886Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Perfecto, ahora entiendo el problema. El PDF actual usa colores claros (azul claro, gris claro) que no se ven bien. Voy a mejorar el PDF con colores corporativos azul marino profesionales y mejor legibilidad.

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          // ── Paleta ────────────────────────────────────────────────────────
          const BLUE = [78, 163, 184];
          const DARK = [237, 244, 251];
          const GRAY = [169, 183, 200];
          const LGRAY = [45, 58, 76];
          const GREEN = [78, 163, 184];
          const ORANGE = [224, 138, 60];
          const RED = [240, 139, 126];
          const WHITE = [255, 255, 255];
=======
          // ── Paleta Corporativa Azul Marino ────────────────────────────────
          const NAVY_DARK = [13, 27, 62];      // Azul marino oscuro principal
          const NAVY_MEDIUM = [25, 55, 109];   // Azul marino medio
          const NAVY_LIGHT = [41, 98, 255];    // Azul corporativo brillante
          const NAVY_ACCENT = [0, 123, 255];   // Azul acento
          const TEXT_DARK = [33, 37, 41];      // Texto principal oscuro
          const TEXT_GRAY = [108, 117, 125];   // Texto secundario
          const GREEN = [40, 167, 69];         // Verde éxito
          const ORANGE = [255, 152, 0];        // Naranja advertencia
          const RED = [220, 53, 69];           // Rojo error
          const WHITE = [255, 255, 255];       // Blanco
          const BG_LIGHT = [248, 249, 250];    // Fondo claro
=======
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
Unable to apply diff to file: c:\Users\harry\PolibitHackatonbob\templates\dashboard.html

<error_details>
ERROR: Special marker '=======' found in your diff content at line 24:

When removing merge conflict markers like '=======' from files, you MUST escape them
in your SEARCH section by prepending a backslash (\) at the beginning of the line:

CORRECT FORMAT:

<<<<<<< SEARCH
content before
\=======    <-- Note the backslash here in this example
content after
=======
replacement content
>>>>>>> REPLACE

Without escaping, the system confuses your content with diff syntax markers.
You may use multiple diff blocks in a single diff request, but ANY of ONLY the following separators that occur within SEARCH or REPLACE content must be escaped, as follows:
\<<<<<<< SEARCH>?
\=======
\>>>>>>> REPLACE

</error_details>
<environment_details>
# VSCode Visible Files
.gitignore

# VSCode Open Tabs
templates/dashboard.html,src/servidor_paso1_web.py,.gitignore,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:54:58.581Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.24

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          // ── Paleta ────────────────────────────────────────────────────────
          const BLUE = [78, 163, 184];
          const DARK = [237, 244, 251];
          const GRAY = [169, 183, 200];
          const LGRAY = [45, 58, 76];
          const GREEN = [78, 163, 184];
          const ORANGE = [224, 138, 60];
          const RED = [240, 139, 126];
          const WHITE = [255, 255, 255];

          // ── Portada ───────────────────────────────────────────────────────
          doc.setFillColor(...BLUE);
=======
          // ── Paleta Corporativa Azul Marino ────────────────────────────────
          const NAVY_DARK = [13, 27, 62];      // Azul marino oscuro principal
          const NAVY_MEDIUM = [25, 55, 109];   // Azul marino medio
          const NAVY_LIGHT = [41, 98, 255];    // Azul corporativo brillante
          const NAVY_ACCENT = [0, 123, 255];   // Azul acento
          const TEXT_DARK = [33, 37, 41];      // Texto principal oscuro
          const TEXT_GRAY = [108, 117, 125];   // Texto secundario
          const GREEN = [40, 167, 69];         // Verde éxito
          const ORANGE = [255, 152, 0];        // Naranja advertencia
          const RED = [220, 53, 69];           // Rojo error
          const WHITE = [255, 255, 255];       // Blanco
          const BG_LIGHT = [248, 249, 250];    // Fondo claro

          // ── Portada ───────────────────────────────────────────────────────
          doc.setFillColor(...NAVY_DARK);
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:55:20.020Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.31

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Excelente, ahora voy a actualizar todas las referencias de colores en el resto del código PDF para usar la nueva paleta azul marino corporativa:

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          doc.setFontSize(11);
          doc.setFont("helvetica", "normal");
          doc.text(
            "Panel del Auditor - Reporte de Analisis de Rendimiento",
            margin,
            31,
          );

          doc.setFontSize(9);
          const fecha = new Date().toLocaleString("es-ES", {
            dateStyle: "long",
            timeStyle: "short",
          });
          doc.text(`Generado: ${fecha}`, margin, 40);

          const archivoCodigo = fuenteCodigoActual || "N/A";
          const archivoAnalisis =
            document.getElementById("bobAnalysisSelect").value || "N/A";
          doc.text(
            `Código analizado: ${archivoCodigo}   |   Analisis Bob: ${archivoAnalisis}`,
            margin,
            47,
          );

          y = 65;

          // ── Función helpers ───────────────────────────────────────────────
          function checkPage(needed = 20) {
            if (y + needed > 280) {
              doc.addPage();
              y = 15;
            }
          }

          function sectionTitle(txt) {
            checkPage(14);
            doc.setFillColor(...BLUE);
            doc.rect(margin, y, W - margin * 2, 8, "F");
            doc.setTextColor(...WHITE);
            doc.setFont("helvetica", "bold");
            doc.setFontSize(9);
            doc.text(txt.toUpperCase(), margin + 3, y + 5.5);
            y += 12;
            doc.setTextColor(...DARK);
          }

          function rowBg(i) {
            return i % 2 === 0 ? [249, 250, 251] : WHITE;
          }
=======
          doc.setFontSize(12);
          doc.setFont("helvetica", "bold");
          doc.text(
            "Panel del Auditor - Reporte de Analisis de Rendimiento",
            margin,
            31,
          );

          doc.setFontSize(9);
          doc.setFont("helvetica", "normal");
          const fecha = new Date().toLocaleString("es-ES", {
            dateStyle: "long",
            timeStyle: "short",
          });
          doc.text(`Generado: ${fecha}`, margin, 40);

          const archivoCodigo = fuenteCodigoActual || "N/A";
          const archivoAnalisis =
            document.getElementById("bobAnalysisSelect").value || "N/A";
          doc.setFontSize(8);
          doc.text(
            `Código analizado: ${archivoCodigo}   |   Analisis Bob: ${archivoAnalisis}`,
            margin,
            47,
          );

          y = 65;

          // ── Función helpers ───────────────────────────────────────────────
          function checkPage(needed = 20) {
            if (y + needed > 280) {
              doc.addPage();
              y = 15;
            }
          }

          function sectionTitle(txt) {
            checkPage(14);
            doc.setFillColor(...NAVY_MEDIUM);
            doc.rect(margin, y, W - margin * 2, 9, "F");
            doc.setTextColor(...WHITE);
            doc.setFont("helvetica", "bold");
            doc.setFontSize(10);
            doc.text(txt.toUpperCase(), margin + 3, y + 6);
            y += 13;
            doc.setTextColor(...TEXT_DARK);
          }

          function rowBg(i) {
            return i % 2 === 0 ? BG_LIGHT : WHITE;
          }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:55:37.819Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.39

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
            if (resumenActual.titulo) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(9);
              doc.setTextColor(...DARK);
              doc.text(`Analisis: ${resumenActual.titulo}`, margin, y);
              y += 6;
            }

            // Puntos clave
            if (
              resumenActual.puntos_clave &&
              resumenActual.puntos_clave.length > 0
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(8);
              doc.setTextColor(...BLUE);
              doc.text("[OK] Puntos Clave:", margin, y);
              y += 4;

              resumenActual.puntos_clave.slice(0, 3).forEach((punto) => {
                checkPage(6);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(7.5);
                doc.setTextColor(...DARK);
                const lineas = doc.splitTextToSize(
                  `- ${punto}`,
                  W - margin * 2 - 4,
                );
                doc.text(lineas[0] || "", margin + 2, y);
                y += 5;
              });
              y += 2;
            }

            // Cuellos de botella
            if (
              resumenActual.cuellos_botella &&
              resumenActual.cuellos_botella.length > 0
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(8);
              doc.setTextColor(...RED);
              doc.text("[CRITICO] Cuellos de Botella:", margin, y);
              y += 4;

              resumenActual.cuellos_botella.slice(0, 3).forEach((cuello) => {
                checkPage(6);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(7.5);
                doc.setTextColor(...DARK);
                const lineas = doc.splitTextToSize(
                  `- ${cuello}`,
                  W - margin * 2 - 4,
                );
                doc.text(lineas[0] || "", margin + 2, y);
                y += 5;
              });
              y += 2;
            }

            // Recomendaciones
            if (
              resumenActual.recomendaciones &&
              resumenActual.recomendaciones.length > 0
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(8);
              doc.setTextColor(...GREEN);
              doc.text("[RECOMENDACION] Propuestas:", margin, y);
              y += 4;

              resumenActual.recomendaciones.slice(0, 3).forEach((rec) => {
                checkPage(6);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(7.5);
                doc.setTextColor(...DARK);
                const lineas = doc.splitTextToSize(
                  `- ${rec}`,
                  W - margin * 2 - 4,
                );
                doc.text(lineas[0] || "", margin + 2, y);
                y += 5;
              });
              y += 4;
            }

            // Complejidades
            if (
              resumenActual.metricas &&
              resumenActual.metricas.complejidades_encontradas
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(7.5);
              doc.setTextColor(...DARK);
              const complejos =
                resumenActual.metricas.complejidades_encontradas.join(" | ");
              doc.text(`Complejidades: ${complejos}`, margin, y);
              y += 6;
            }
=======
            if (resumenActual.titulo) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(10);
              doc.setTextColor(...TEXT_DARK);
              doc.text(`Analisis: ${resumenActual.titulo}`, margin, y);
              y += 7;
            }

            // Puntos clave
            if (
              resumenActual.puntos_clave &&
              resumenActual.puntos_clave.length > 0
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(9);
              doc.setTextColor(...NAVY_ACCENT);
              doc.text("✓ Puntos Clave:", margin, y);
              y += 5;

              resumenActual.puntos_clave.slice(0, 3).forEach((punto) => {
                checkPage(6);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(8.5);
                doc.setTextColor(...TEXT_DARK);
                const lineas = doc.splitTextToSize(
                  `• ${punto}`,
                  W - margin * 2 - 4,
                );
                doc.text(lineas[0] || "", margin + 3, y);
                y += 5.5;
              });
              y += 2;
            }

            // Cuellos de botella
            if (
              resumenActual.cuellos_botella &&
              resumenActual.cuellos_botella.length > 0
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(9);
              doc.setTextColor(...RED);
              doc.text("⚠ CRITICO - Cuellos de Botella:", margin, y);
              y += 5;

              resumenActual.cuellos_botella.slice(0, 3).forEach((cuello) => {
                checkPage(6);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(8.5);
                doc.setTextColor(...TEXT_DARK);
                const lineas = doc.splitTextToSize(
                  `• ${cuello}`,
                  W - margin * 2 - 4,
                );
                doc.text(lineas[0] || "", margin + 3, y);
                y += 5.5;
              });
              y += 2;
            }

            // Recomendaciones
            if (
              resumenActual.recomendaciones &&
              resumenActual.recomendaciones.length > 0
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(9);
              doc.setTextColor(...GREEN);
              doc.text("→ Recomendaciones:", margin, y);
              y += 5;

              resumenActual.recomendaciones.slice(0, 3).forEach((rec) => {
                checkPage(6);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(8.5);
                doc.setTextColor(...TEXT_DARK);
                const lineas = doc.splitTextToSize(
                  `• ${rec}`,
                  W - margin * 2 - 4,
                );
                doc.text(lineas[0] || "", margin + 3, y);
                y += 5.5;
              });
              y += 4;
            }

            // Complejidades
            if (
              resumenActual.metricas &&
              resumenActual.metricas.complejidades_encontradas
            ) {
              doc.setFont("helvetica", "bold");
              doc.setFontSize(8.5);
              doc.setTextColor(...NAVY_MEDIUM);
              const complejos =
                resumenActual.metricas.complejidades_encontradas.join(" | ");
              doc.text(`Complejidades detectadas: ${complejos}`, margin, y);
              y += 7;
            }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:56:07.004Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.48

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          // Cabecera tabla
          const cols = [
            "Tamaño N",
            "DFS (ms)",
            "LDFS (ms)",
            "IDFS (ms)",
            "Mem DFS (MB)",
          ];
          const colW = [30, 38, 38, 38, 42];
          const colX = [margin];
          colW.forEach((w, i) => {
            if (i > 0) colX.push(colX[i - 1] + colW[i - 1]);
          });

          doc.setFillColor(...LGRAY);
          doc.rect(margin, y, W - margin * 2, 8, "F");
          doc.setFont("helvetica", "bold");
          doc.setFontSize(8);
          doc.setTextColor(...DARK);
          cols.forEach((c, i) => doc.text(c, colX[i] + 2, y + 5.5));
          y += 9;

          sizes.forEach((size, ri) => {
            checkPage(9);
            const m = metricsData[size];

            function tv(algo) {
              return m[algo]?.time_ms_mean !== undefined
                ? m[algo].time_ms_mean.toFixed(2)
                : (m.time_ms || 0).toFixed(2);
            }
            function mv(algo) {
              return m[algo]?.mem_bytes_peak_mean !== undefined
                ? (m[algo].mem_bytes_peak_mean / (1024 * 1024)).toFixed(3)
                : (m.memory_mb || 0).toFixed(3);
            }
            function colorNum(v) {
              const n = parseFloat(v);
              return n > 1000 ? RED : n > 100 ? ORANGE : GREEN;
            }

            doc.setFillColor(...rowBg(ri));
            doc.rect(margin, y, W - margin * 2, 8, "F");
            doc.setFont("helvetica", "bold");
            doc.setFontSize(8);
            doc.setTextColor(...DARK);
            doc.text(`N = ${size}`, colX[0] + 2, y + 5.5);

            const vals = [tv("dfs"), tv("ldfs"), tv("idfs"), mv("dfs")];
            vals.forEach((v, i) => {
              doc.setTextColor(...colorNum(i < 3 ? v : "0"));
              doc.setFont("helvetica", "normal");
              doc.text(v, colX[i + 1] + 2, y + 5.5);
            });
            y += 9;
          });
=======
          // Cabecera tabla
          const cols = [
            "Tamaño N",
            "DFS (ms)",
            "LDFS (ms)",
            "IDFS (ms)",
            "Mem DFS (MB)",
          ];
          const colW = [30, 38, 38, 38, 42];
          const colX = [margin];
          colW.forEach((w, i) => {
            if (i > 0) colX.push(colX[i - 1] + colW[i - 1]);
          });

          doc.setFillColor(...NAVY_MEDIUM);
          doc.rect(margin, y, W - margin * 2, 9, "F");
          doc.setFont("helvetica", "bold");
          doc.setFontSize(9);
          doc.setTextColor(...WHITE);
          cols.forEach((c, i) => doc.text(c, colX[i] + 2, y + 6));
          y += 10;

          sizes.forEach((size, ri) => {
            checkPage(9);
            const m = metricsData[size];

            function tv(algo) {
              return m[algo]?.time_ms_mean !== undefined
                ? m[algo].time_ms_mean.toFixed(2)
                : (m.time_ms || 0).toFixed(2);
            }
            function mv(algo) {
              return m[algo]?.mem_bytes_peak_mean !== undefined
                ? (m[algo].mem_bytes_peak_mean / (1024 * 1024)).toFixed(3)
                : (m.memory_mb || 0).toFixed(3);
            }
            function colorNum(v) {
              const n = parseFloat(v);
              return n > 1000 ? RED : n > 100 ? ORANGE : GREEN;
            }

            doc.setFillColor(...rowBg(ri));
            doc.rect(margin, y, W - margin * 2, 8, "F");
            doc.setFont("helvetica", "bold");
            doc.setFontSize(8.5);
            doc.setTextColor(...TEXT_DARK);
            doc.text(`N = ${size}`, colX[0] + 2, y + 5.5);

            const vals = [tv("dfs"), tv("ldfs"), tv("idfs"), mv("dfs")];
            vals.forEach((v, i) => {
              doc.setTextColor(...colorNum(i < 3 ? v : "0"));
              doc.setFont("helvetica", "normal");
              doc.setFontSize(8.5);
              doc.text(v, colX[i + 1] + 2, y + 5.5);
            });
            y += 9;
          });
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:56:26.627Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.57

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          // ── Sección 2: Alertas ────────────────────────────────────────────
          sectionTitle(`[ALERTAS] Detectadas (${alertasActuales.length})`);

          if (alertasActuales.length === 0) {
            doc.setFont("helvetica", "italic");
            doc.setFontSize(9);
            doc.setTextColor(...GRAY);
            doc.text(
              "Sin alertas. Rendimiento dentro de parametros normales.",
              margin,
              y,
            );
            y += 10;
          } else {
            alertasActuales.forEach((a, i) => {
              checkPage(18);
              const c =
                a.nivel === "error"
                  ? RED
                  : a.nivel === "warning"
                    ? ORANGE
                    : BLUE;
              doc.setFillColor(...c);
              doc.rect(margin, y, 3, 14, "F");
              doc.setFillColor(...rowBg(i));
              doc.rect(margin + 3, y, W - margin * 2 - 3, 14, "F");

              doc.setFont("helvetica", "bold");
              doc.setFontSize(8);
              doc.setTextColor(...DARK);
              const tipoLimpio = a.tipo.replace(/[^a-zA-Z0-9_-]/g, "");
              doc.text(`[${tipoLimpio}]`, margin + 6, y + 5);
              doc.setFont("helvetica", "normal");
              doc.setFontSize(7.5);
              doc.setTextColor(...GRAY);
              const lineas = doc.splitTextToSize(
                a.mensaje,
                W - margin * 2 - 12,
              );
              doc.text(lineas[0], margin + 6, y + 11);
              y += 16;
            });
          }
=======
          // ── Sección 2: Alertas ────────────────────────────────────────────
          sectionTitle(`[ALERTAS] Detectadas (${alertasActuales.length})`);

          if (alertasActuales.length === 0) {
            doc.setFont("helvetica", "italic");
            doc.setFontSize(9);
            doc.setTextColor(...TEXT_GRAY);
            doc.text(
              "✓ Sin alertas. Rendimiento dentro de parametros normales.",
              margin,
              y,
            );
            y += 10;
          } else {
            alertasActuales.forEach((a, i) => {
              checkPage(18);
              const c =
                a.nivel === "error"
                  ? RED
                  : a.nivel === "warning"
                    ? ORANGE
                    : NAVY_ACCENT;
              doc.setFillColor(...c);
              doc.rect(margin, y, 4, 15, "F");
              doc.setFillColor(...rowBg(i));
              doc.rect(margin + 4, y, W - margin * 2 - 4, 15, "F");

              doc.setFont("helvetica", "bold");
              doc.setFontSize(8.5);
              doc.setTextColor(...TEXT_DARK);
              const tipoLimpio = a.tipo.replace(/[^a-zA-Z0-9_-]/g, "");
              doc.text(`[${tipoLimpio}]`, margin + 7, y + 5.5);
              doc.setFont("helvetica", "normal");
              doc.setFontSize(8);
              doc.setTextColor(...TEXT_GRAY);
              const lineas = doc.splitTextToSize(
                a.mensaje,
                W - margin * 2 - 14,
              );
              doc.text(lineas[0], margin + 7, y + 11);
              y += 17;
            });
          }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:56:42.617Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.66

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          // Leyenda de colores
          doc.setFont("helvetica", "bold");
          doc.setFontSize(7.5);
          [
            ["DFS", BLUE],
            ["LDFS", ORANGE],
            ["IDFS", [159, 24, 83]],
          ].forEach(([lbl, clr], i) => {
            const lx = margin + i * 30;
            doc.setFillColor(...clr);
            doc.rect(lx, y + 1, 6, 4, "F");
            doc.setTextColor(...DARK);
            doc.text(lbl, lx + 8, y + 5);
          });
          y += 12;

          // ── Sección 4: Código analizado ───────────────────────────────────
          if (codigoActual) {
            checkPage(20);
            sectionTitle(`[CODIGO] Analizado: ${archivoCodigo}`);

            const lineas = codigoActual.split("\n").slice(0, 50);
            doc.setFont("courier", "normal");
            doc.setFontSize(7);
            doc.setTextColor(...DARK);

            lineas.forEach((linea, i) => {
              checkPage(6);
              if (i % 2 === 0) {
                doc.setFillColor(245, 247, 250);
                doc.rect(margin, y - 3, W - margin * 2, 5.5, "F");
              }
              doc.setTextColor(100, 100, 100);
              doc.text(String(i + 1).padStart(3, " "), margin + 1, y + 1.5);
              doc.setTextColor(...DARK);
              const cortada = doc.splitTextToSize(linea, W - margin * 2 - 12);
              doc.text(cortada[0] || "", margin + 10, y + 1.5);
              y += 5.5;
            });

            if (codigoActual.split("\n").length > 50) {
              checkPage(8);
              doc.setFont("helvetica", "italic");
              doc.setFontSize(7.5);
              doc.setTextColor(...GRAY);
              doc.text(
                `... (se muestran las primeras 50 lineas de ${codigoActual.split("\n").length})`,
                margin,
                y + 4,
              );
              y += 10;
            }
          }
=======
          // Leyenda de colores
          doc.setFont("helvetica", "bold");
          doc.setFontSize(8.5);
          [
            ["DFS", NAVY_LIGHT],
            ["LDFS", ORANGE],
            ["IDFS", [159, 24, 83]],
          ].forEach(([lbl, clr], i) => {
            const lx = margin + i * 32;
            doc.setFillColor(...clr);
            doc.rect(lx, y + 1, 7, 4.5, "F");
            doc.setTextColor(...TEXT_DARK);
            doc.text(lbl, lx + 9, y + 5);
          });
          y += 12;

          // ── Sección 4: Código analizado ───────────────────────────────────
          if (codigoActual) {
            checkPage(20);
            sectionTitle(`[CODIGO] Analizado: ${archivoCodigo}`);

            const lineas = codigoActual.split("\n").slice(0, 50);
            doc.setFont("courier", "normal");
            doc.setFontSize(7.5);
            doc.setTextColor(...TEXT_DARK);

            lineas.forEach((linea, i) => {
              checkPage(6);
              if (i % 2 === 0) {
                doc.setFillColor(...BG_LIGHT);
                doc.rect(margin, y - 3, W - margin * 2, 5.5, "F");
              }
              doc.setTextColor(...TEXT_GRAY);
              doc.text(String(i + 1).padStart(3, " "), margin + 1, y + 1.5);
              doc.setTextColor(...TEXT_DARK);
              const cortada = doc.splitTextToSize(linea, W - margin * 2 - 12);
              doc.text(cortada[0] || "", margin + 10, y + 1.5);
              y += 5.5;
            });

            if (codigoActual.split("\n").length > 50) {
              checkPage(8);
              doc.setFont("helvetica", "italic");
              doc.setFontSize(8);
              doc.setTextColor(...TEXT_GRAY);
              doc.text(
                `... (se muestran las primeras 50 lineas de ${codigoActual.split("\n").length})`,
                margin,
                y + 4,
              );
              y += 10;
            }
          }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:57:04.085Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.76

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<apply_diff>
<path>templates/dashboard.html</path>
<diff>
<<<<<<< SEARCH
          // ── Sección 5: análisis del código pegado ───────────────────────
          if (analisisCodigoPersonalizado) {
            checkPage(18);
            sectionTitle("[CODIGO PERSONALIZADO] Métricas y alertas");

            doc.setFont("helvetica", "normal");
            doc.setFontSize(8.5);
            doc.setTextColor(...DARK);

            const analisis = analisisCodigoPersonalizado;
            const metricas = metricasCodigoPersonalizado || analisis.metricas || {};
            const alertas = alertasCodigoPersonalizado || analisis.alertas || [];

            const lineasResumen = [
              `Complejidad estimada: ${analisis.complejidad_estimada || 'N/D'}`,
              `Líneas: ${metricas.lineas_detectadas ?? 'N/D'} | Funciones: ${metricas.funciones_detectadas ?? 'N/D'}`,
              `Bucles: ${metricas.bucles_detectados ?? 'N/D'} | Profundidad máxima: ${metricas.profundidad_maxima_bucles ?? 'N/D'}`,
              `Recursiones: ${metricas.recursiones_detectadas ?? 'N/D'} | Comparaciones in/not in: ${metricas.comparaciones_in_detectadas ?? 'N/D'}`,
              `Factor de riesgo: ${metricas.factor_riesgo ?? 'N/D'}/100`,
            ];

            lineasResumen.forEach((texto) => {
              checkPage(5);
              doc.text(texto, margin, y);
              y += 4.8;
            });

            if (alertas.length > 0) {
              checkPage(8);
              doc.setFont("helvetica", "bold");
              doc.text("Alertas:", margin, y);
              y += 5;
              doc.setFont("helvetica", "normal");
              alertas.slice(0, 5).forEach((alerta) => {
                checkPage(6);
                const texto = `- ${alerta.icono || '•'} ${alerta.tipo || 'ALERTA'}: ${alerta.mensaje || ''}`;
                doc.text(doc.splitTextToSize(texto, W - margin * 2), margin, y);
                y += 5;
              });
            }
          }

          // ── Pie de página en todas las páginas ────────────────────────────
          const total = doc.getNumberOfPages();
          for (let p = 1; p <= total; p++) {
            doc.setPage(p);
            doc.setFillColor(...LGRAY);
            doc.rect(0, 290, W, 7, "F");
            doc.setFont("helvetica", "normal");
            doc.setFontSize(7);
            doc.setTextColor(...GRAY);
            doc.text(
              "OptiCode QA - Reporte de Auditoria de Algoritmos",
              margin,
              294.5,
            );
            doc.text(`Página ${p} / ${total}`, W - margin - 20, 294.5);
          }
=======
          // ── Sección 5: análisis del código pegado ───────────────────────
          if (analisisCodigoPersonalizado) {
            checkPage(18);
            sectionTitle("[CODIGO PERSONALIZADO] Métricas y alertas");

            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
            doc.setTextColor(...TEXT_DARK);

            const analisis = analisisCodigoPersonalizado;
            const metricas = metricasCodigoPersonalizado || analisis.metricas || {};
            const alertas = alertasCodigoPersonalizado || analisis.alertas || [];

            const lineasResumen = [
              `Complejidad estimada: ${analisis.complejidad_estimada || 'N/D'}`,
              `Líneas: ${metricas.lineas_detectadas ?? 'N/D'} | Funciones: ${metricas.funciones_detectadas ?? 'N/D'}`,
              `Bucles: ${metricas.bucles_detectados ?? 'N/D'} | Profundidad máxima: ${metricas.profundidad_maxima_bucles ?? 'N/D'}`,
              `Recursiones: ${metricas.recursiones_detectadas ?? 'N/D'} | Comparaciones in/not in: ${metricas.comparaciones_in_detectadas ?? 'N/D'}`,
              `Factor de riesgo: ${metricas.factor_riesgo ?? 'N/D'}/100`,
            ];

            lineasResumen.forEach((texto) => {
              checkPage(5);
              doc.text(texto, margin, y);
              y += 5.2;
            });

            if (alertas.length > 0) {
              checkPage(8);
              doc.setFont("helvetica", "bold");
              doc.setFontSize(9);
              doc.setTextColor(...NAVY_MEDIUM);
              doc.text("Alertas detectadas:", margin, y);
              y += 6;
              doc.setFont("helvetica", "normal");
              doc.setFontSize(8.5);
              doc.setTextColor(...TEXT_DARK);
              alertas.slice(0, 5).forEach((alerta) => {
                checkPage(6);
                const texto = `• ${alerta.tipo || 'ALERTA'}: ${alerta.mensaje || ''}`;
                doc.text(doc.splitTextToSize(texto, W - margin * 2), margin + 2, y);
                y += 5.5;
              });
            }
          }

          // ── Pie de página en todas las páginas ────────────────────────────
          const total = doc.getNumberOfPages();
          for (let p = 1; p <= total; p++) {
            doc.setPage(p);
            doc.setFillColor(...NAVY_DARK);
            doc.rect(0, 290, W, 7, "F");
            doc.setFont("helvetica", "normal");
            doc.setFontSize(7.5);
            doc.setTextColor(...WHITE);
            doc.text(
              "OptiCode QA - Reporte de Auditoria de Algoritmos",
              margin,
              294.5,
            );
            doc.text(`Página ${p} / ${total}`, W - margin - 20, 294.5);
          }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'templates/dashboard.html'] Result:
<file_write_result>
<path>templates/dashboard.html</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
templates\dashboard.html

# VSCode Open Tabs
src/servidor_paso1_web.py,.gitignore,templates/dashboard.html,src/motor_qa.py,src/integrador_watsonx.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T12:57:31.575Z
User time zone: America/Guayaquil, UTC-5:00

# Current Cost
$0.86

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Perfecto! Ahora voy a crear un resumen de los cambios realizados para que puedas verificar que el PDF se ve mucho mejor:

<attempt_completion>
<result>
✅ **PDF MEJORADO CON COLORES CORPORATIVOS AZUL MARINO**

He actualizado completamente el diseño del PDF con una paleta profesional de colores azul marino corporativos:

## 🎨 Nueva Paleta de Colores:
- **Azul Marino Oscuro** (13, 27, 62) - Portada y pie de página
- **Azul Marino Medio** (25, 55, 109) - Títulos de secciones y encabezados de tablas
- **Azul Corporativo** (41, 98, 255) - Acentos y elementos destacados
- **Texto Oscuro** (33, 37, 41) - Texto principal legible
- **Texto Gris** (108, 117, 125) - Texto secundario
- **Verde/Naranja/Rojo** - Alertas y estados (mejorados)

## 📋 Mejoras Implementadas:

### 1. **Portada**
   - Fondo azul marino oscuro profesional
   - Texto blanco contrastante y legible
   - Subtítulos más grandes y claros

### 2. **Títulos de Secciones**
   - Fondo azul marino medio con texto blanco
   - Tamaño de fuente aumentado (10pt)
   - Mejor espaciado vertical

### 3. **Tablas de Métricas**
   - Encabezado azul marino con texto blanco
   - Filas alternadas con fondo claro para mejor lectura
   - Texto más grande (8.5pt) y legible

### 4. **Alertas**
   - Barra lateral de color más ancha (4mm)
   - Texto más grande y espaciado
   - Mejor contraste de colores

### 5. **Código Fuente**
   - Números de línea en gris para mejor distinción
   - Fondo alternado más suave
   - Fuente más grande (7.5pt)

### 6. **Pie de Página**
   - Fondo azul marino oscuro corporativo
   - Texto blanco para máximo contraste
   - Información clara y legible

## ✨ Resultado:
El PDF ahora tiene un aspecto **profesional, corporativo y altamente legible** con colores azul marino que transmiten confianza y seriedad. Todos los textos son más grandes y tienen mejor contraste para facilitar la lectura.

Para probar los cambios, ejecuta el servidor y genera un nuevo PDF desde el dashboard.
</result>
</attempt_completion>

