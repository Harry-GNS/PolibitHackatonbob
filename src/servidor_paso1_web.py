"""Servidor Flask con interfaz web bonita para PASO 1 Real

Flujo: Bob IDE (manual) → Motor Local → watsonx.ai
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
<<<<<<< HEAD
import ast
=======
>>>>>>> f070f6795f7f9920715de3874a4d1595fa6f3425
import json
import traceback
import sys
import re
from datetime import datetime

# Añadir el directorio raíz al path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.motor_qa import run_benchmarks
from src.integrador_watsonx import summarize_metrics

app = Flask(__name__, template_folder=str(ROOT / "templates"))
CORS(app)

# Directorio de análisis de Bob IDE - USAR SOLO output/informesbob
BOB_SESSIONS_DIR = ROOT / "output" / "informesbob"
OUTPUT_DIR = ROOT / "output"
DATA_DIR = ROOT / "data"
SRC_DIR = ROOT / "src"

# Crear directorios si no existen
BOB_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================
# RUTAS HTML (Frontend)
# ============================================

@app.route('/')
def index():
    """Sirve el dashboard principal."""
    return render_template('dashboard.html')


@app.route('/LOGOQA.png')
def logo_qa():
    """Sirve el logo del dashboard."""
    return send_from_directory(str(ROOT), 'LOGOQA.png')


# ============================================
# API REST (Backend)
# ============================================

@app.route('/api/bob-sessions', methods=['GET'])
def listar_bob_sessions():
    """Lista todos los análisis .md de Bob IDE."""
    try:
        archivos = []
        
        if BOB_SESSIONS_DIR.exists():
            for archivo in sorted(BOB_SESSIONS_DIR.glob('*.md')):
                # Saltar archivos README
                if 'README' in archivo.name:
                    continue
                    
                contenido = archivo.read_text(encoding='utf-8')
                archivos.append({
                    "nombre": archivo.name,
                    "contenido_preview": contenido[:200],
                    "tamaño": len(contenido),
                    "tipo": "Bob IDE Analysis"
                })
        
        return jsonify({
            "success": True,
            "total": len(archivos),
            "archivos": archivos
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/bob-sessions/<nombre>', methods=['GET'])
def obtener_bob_analysis(nombre):
    """Obtiene el contenido completo de un análisis de Bob IDE."""
    try:
        ruta = BOB_SESSIONS_DIR / nombre
        
        if not ruta.exists():
            return jsonify({"error": f"Archivo no encontrado: {nombre}"}), 404
        
        contenido = ruta.read_text(encoding='utf-8')
        
        return jsonify({
            "success": True,
            "nombre": nombre,
            "contenido": contenido
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/codigos', methods=['GET'])
def listar_codigos():
    """Lista archivos .py disponibles para benchmarks."""
    try:
        archivos = []
        
        # Buscar en src/
        if SRC_DIR.exists():
            for archivo in sorted(SRC_DIR.glob('*.py')):
                if archivo.name.startswith('__'):
                    continue
                    
                contenido = archivo.read_text(encoding='utf-8')
                archivos.append({
                    "nombre": archivo.name,
                    "ruta": f"src/{archivo.name}",
                    "contenido_preview": contenido[:200]
                })
        
        # Buscar en src/examples/
        examples_dir = SRC_DIR / "examples"
        if examples_dir.exists():
            for archivo in sorted(examples_dir.glob('*.py')):
                if archivo.name.startswith('__'):
                    continue
                    
                contenido = archivo.read_text(encoding='utf-8')
                archivos.append({
                    "nombre": archivo.name,
                    "ruta": f"src/examples/{archivo.name}",
                    "contenido_preview": contenido[:200]
                })
        
        return jsonify({
            "success": True,
            "total": len(archivos),
            "archivos": archivos
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/codigos/<nombre>', methods=['GET'])
def obtener_codigo(nombre):
    """Obtiene el contenido de un archivo .py."""
    try:
        # Buscar en src/
        rutas_posibles = [
            SRC_DIR / nombre,
            SRC_DIR / "examples" / nombre
        ]
        
        for ruta in rutas_posibles:
            if ruta.exists():
                contenido = ruta.read_text(encoding='utf-8')
                return jsonify({
                    "success": True,
                    "nombre": nombre,
                    "contenido": contenido
                })
        
        return jsonify({"error": f"Archivo no encontrado: {nombre}"}), 404
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


<<<<<<< HEAD
@app.route('/api/analizar-codigo-personalizado', methods=['POST'])
def analizar_codigo_personalizado():
    """Analiza código Python pegado por el usuario con heurísticas estáticas simples."""
    try:
        data = request.get_json(silent=True) or {}
        codigo = (data.get('codigo') or '').strip()
        nombre = (data.get('nombre') or 'codigo_pegado.py').strip()

        if not codigo:
            return jsonify({
                "success": False,
                "error": "El campo 'codigo' está vacío."
            }), 400

        lineas = codigo.splitlines()

        try:
            tree = ast.parse(codigo)
        except SyntaxError as exc:
            return jsonify({
                "success": False,
                "error": f"Error de sintaxis en línea {exc.lineno}: {exc.msg}",
                "nombre": nombre,
                "codigo": codigo,
                "analisis": {
                    "titulo": "Código pegado con errores de sintaxis",
                    "complejidad_estimada": "No evaluable",
                    "puntos_clave": [
                        f"La línea {exc.lineno or '?'} tiene un error de sintaxis: {exc.msg}",
                    ],
                    "cuellos_botella": [],
                    "recomendaciones": [
                        "Corrige la sintaxis antes de ejecutar el análisis de complejidad.",
                        "Verifica sangrías, paréntesis y dos puntos en funciones y bucles."
                    ],
                    "metricas": {
                        "lineas_detectadas": len(lineas),
                        "errores_sintaxis": True,
                    }
                }
            }), 200

        class HeuristicaVisitor(ast.NodeVisitor):
            def __init__(self):
                self.funciones = []
                self.bucles = []
                self.comparaciones_in = []
                self.comprehensions = []
                self.recursivas = []
                self.max_profundidad_bucles = 0
                self._profundidad_bucle = 0
                self._pila_funciones = []

            def visit_FunctionDef(self, node):
                self.funciones.append({
                    "nombre": node.name,
                    "linea": node.lineno,
                })
                self._pila_funciones.append(node.name)
                self.generic_visit(node)
                self._pila_funciones.pop()

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_For(self, node):
                self._profundidad_bucle += 1
                self.max_profundidad_bucles = max(self.max_profundidad_bucles, self._profundidad_bucle)
                self.bucles.append({
                    "tipo": "for",
                    "linea": node.lineno,
                    "anidado": self._profundidad_bucle > 1,
                })
                self.generic_visit(node)
                self._profundidad_bucle -= 1

            def visit_While(self, node):
                self._profundidad_bucle += 1
                self.max_profundidad_bucles = max(self.max_profundidad_bucles, self._profundidad_bucle)
                self.bucles.append({
                    "tipo": "while",
                    "linea": node.lineno,
                    "anidado": self._profundidad_bucle > 1,
                })
                self.generic_visit(node)
                self._profundidad_bucle -= 1

            def visit_Call(self, node):
                if self._pila_funciones and isinstance(node.func, ast.Name):
                    if node.func.id == self._pila_funciones[-1]:
                        self.recursivas.append({
                            "funcion": node.func.id,
                            "linea": node.lineno,
                        })
                self.generic_visit(node)

            def visit_Compare(self, node):
                if any(isinstance(op, (ast.In, ast.NotIn)) for op in node.ops):
                    self.comparaciones_in.append(node.lineno)
                self.generic_visit(node)

            def visit_ListComp(self, node):
                self.comprehensions.append({"tipo": "listcomp", "linea": node.lineno})
                self.generic_visit(node)

            def visit_SetComp(self, node):
                self.comprehensions.append({"tipo": "setcomp", "linea": node.lineno})
                self.generic_visit(node)

            def visit_DictComp(self, node):
                self.comprehensions.append({"tipo": "dictcomp", "linea": node.lineno})
                self.generic_visit(node)

            def visit_GeneratorExp(self, node):
                self.comprehensions.append({"tipo": "genexp", "linea": node.lineno})
                self.generic_visit(node)

        visitor = HeuristicaVisitor()
        visitor.visit(tree)

        if visitor.max_profundidad_bucles >= 3:
            complejidad = 'O(N^3) o peor'
        elif visitor.max_profundidad_bucles == 2:
            complejidad = 'O(N^2)'
        elif visitor.max_profundidad_bucles == 1:
            complejidad = 'O(N)'
        else:
            complejidad = 'O(1) a O(N) según las operaciones internas'

        puntos_clave = []
        if visitor.funciones:
            puntos_clave.append(f"Se detectaron {len(visitor.funciones)} función(es) en el código pegado.")
        if visitor.max_profundidad_bucles > 0:
            puntos_clave.append(f"Profundidad máxima de bucles detectada: {visitor.max_profundidad_bucles}.")
        if visitor.recursivas:
            nombres_recursivos = ', '.join(sorted({r['funcion'] for r in visitor.recursivas}))
            puntos_clave.append(f"Se detectó recursión directa en: {nombres_recursivos}.")
        if visitor.comparaciones_in:
            puntos_clave.append(f"Se hallaron {len(visitor.comparaciones_in)} comparaciones 'in/not in', posibles cuellos de botella en listas.")
        if visitor.comprehensions:
            puntos_clave.append(f"Se detectaron {len(visitor.comprehensions)} comprensiones de datos.")

        cuellos_botella = []
        recomendaciones = []
        alertas = []

        for bucle in visitor.bucles:
            etiqueta = f"Línea {bucle['linea']} ({bucle['tipo']})"
            if bucle['anidado']:
                cuellos_botella.append(f"{etiqueta}: bucle anidado que puede elevar la complejidad.")
                recomendaciones.append("Revisa si el bucle interno puede eliminarse, indexarse o precalcularse.")
                alertas.append({
                    'tipo': 'BUCLE_ANIDADO',
                    'nivel': 'warning',
                    'icono': '⚠️',
                    'mensaje': f"Bucle anidado detectado en la línea {bucle['linea']}",
                    'linea': bucle['linea']
                })

        for rec in visitor.recursivas:
            cuellos_botella.append(f"Línea {rec['linea']}: llamada recursiva a {rec['funcion']}().")
            recomendaciones.append("Verifica el caso base y evalúa una versión iterativa si la profundidad puede crecer mucho.")
            alertas.append({
                'tipo': 'RECURSION',
                'nivel': 'info',
                'icono': '🔁',
                'mensaje': f"Recursión detectada en {rec['funcion']}() línea {rec['linea']}",
                'linea': rec['linea']
            })

        for linea in visitor.comparaciones_in:
            cuellos_botella.append(f"Línea {linea}: comparación de membresía en una estructura lineal.")
            recomendaciones.append("Si la estructura crece, cambia la lista por un set o dict para búsquedas O(1).")
            alertas.append({
                'tipo': 'MEMBRESIA_LINEAL',
                'nivel': 'warning',
                'icono': '🔎',
                'mensaje': f"Posible búsqueda lineal con 'in/not in' en la línea {linea}",
                'linea': linea
            })

        if visitor.comprehensions:
            cuellos_botella.append("Se detectaron comprensiones de datos que pueden duplicar trabajo si se usan dentro de bucles frecuentes.")
            recomendaciones.append("Mantén las comprensiones solo si aportan claridad y no se ejecutan en rutas críticas repetidas.")
            alertas.append({
                'tipo': 'COMPRENSIONES',
                'nivel': 'info',
                'icono': '🧩',
                'mensaje': f"Se detectaron {len(visitor.comprehensions)} comprensiones de datos",
                'cantidad': len(visitor.comprehensions)
            })

        if not cuellos_botella:
            cuellos_botella.append("No se detectaron cuellos de botella obvios con las heurísticas básicas.")
            recomendaciones.append("Complementa este análisis con benchmarks locales si el código se ejecuta en rutas críticas.")
            alertas.append({
                'tipo': 'SIN_ALERTAS_CRITICAS',
                'nivel': 'success',
                'icono': '✅',
                'mensaje': 'No se detectaron patrones críticos evidentes con las heurísticas básicas.'
            })

        metricas = {
            'lineas_detectadas': len(lineas),
            'funciones_detectadas': len(visitor.funciones),
            'bucles_detectados': len(visitor.bucles),
            'profundidad_maxima_bucles': visitor.max_profundidad_bucles,
            'recursiones_detectadas': len(visitor.recursivas),
            'comparaciones_in_detectadas': len(visitor.comparaciones_in),
            'comprehensions_detectadas': len(visitor.comprehensions),
            'complejidad_heuristica': complejidad,
            'factor_riesgo': min(100, (visitor.max_profundidad_bucles * 25) + (len(visitor.recursivas) * 15) + (len(visitor.comparaciones_in) * 10) + (len(visitor.comprehensions) * 5))
        }

        markdown = [
            f"# Análisis de código pegado: {nombre}",
            "",
            "## Complejidad estimada",
            f"- **Estimación global:** {complejidad}",
            f"- **Líneas analizadas:** {len(lineas)}",
            f"- **Funciones detectadas:** {len(visitor.funciones)}",
            f"- **Profundidad máxima de bucles:** {visitor.max_profundidad_bucles}",
            f"- **Factor de riesgo heurístico:** {metricas['factor_riesgo']}/100",
            "",
            "## Cuellos de botella",
            *[f"- {item}" for item in cuellos_botella],
            "",
            "## Métricas detalladas",
            f"- **Bucles detectados:** {metricas['bucles_detectados']}",
            f"- **Recursiones detectadas:** {metricas['recursiones_detectadas']}",
            f"- **Comparaciones in/not in:** {metricas['comparaciones_in_detectadas']}",
            f"- **Comprensiones detectadas:** {metricas['comprehensions_detectadas']}",
            "",
            "## Recomendaciones",
            *[f"- {item}" for item in recomendaciones[:6]],
        ]

        return jsonify({
            "success": True,
            "nombre": nombre,
            "codigo": codigo,
            "analisis": {
                "titulo": f"Análisis de código pegado: {nombre}",
                "complejidad_estimada": complejidad,
                "puntos_clave": puntos_clave[:5],
                "cuellos_botella": cuellos_botella[:6],
                "recomendaciones": recomendaciones[:6],
                "metricas": metricas,
                "alertas": alertas[:8],
            },
            "markdown": "\n".join(markdown),
            "metricas": metricas,
            "alertas": alertas[:8],
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


=======
>>>>>>> f070f6795f7f9920715de3874a4d1595fa6f3425
@app.route('/api/ejecutar-benchmarks', methods=['POST'])
def ejecutar_benchmarks():
    """Ejecuta motor_qa.py para benchmarks prácticos."""
    try:
        print("⚡ Iniciando benchmarks locales...")
        
        # Ejecutar motor_qa
        run_benchmarks()
        
        # Cargar y procesar métricas generadas
        metricas_path = DATA_DIR / "metricas_salida.json"
        
        if not metricas_path.exists():
            return jsonify({
                "success": False,
                "error": "No se generó archivo de métricas"
            }), 500
        
        metricas_raw = json.loads(metricas_path.read_text(encoding='utf-8'))
        benchmarks = metricas_raw.get('benchmarks', {})
        
<<<<<<< HEAD
        # Procesar para formato visual, preservando estructura de algoritmos
        metricas_procesadas = {}
        for size_str in sorted(benchmarks.keys(), key=lambda x: int(x)):
            metrics = benchmarks[size_str]
            metricas_procesadas[size_str] = {}
            
            # Copiar estructura de algoritmos (dfs, ldfs, idfs)
            for algo in ['dfs', 'ldfs', 'idfs']:
                if algo in metrics and isinstance(metrics[algo], dict):
                    algo_data = metrics[algo]
                    metricas_procesadas[size_str][algo] = {
                        'time_ms_mean': round(float(algo_data.get('time_ms_mean', 0)), 2),
                        'mem_bytes_peak_mean': round(float(algo_data.get('mem_bytes_peak_mean', 0)), 2),
                        'time_ms_samples': [round(float(t), 2) for t in algo_data.get('time_ms_samples', [])],
                        'mem_bytes_peak_samples': [round(float(m), 2) for m in algo_data.get('mem_bytes_peak_samples', [])]
                    }
            
            # Agregar promedios a nivel de tamaño para compatibilidad con detectar_alertas
            all_times = []
            all_mems = []
            for algo in ['dfs', 'ldfs', 'idfs']:
                if algo in metricas_procesadas[size_str]:
                    all_times.append(metricas_procesadas[size_str][algo]['time_ms_mean'])
                    all_mems.append(metricas_procesadas[size_str][algo]['mem_bytes_peak_mean'] / (1024 * 1024))
            
            if all_times:
                metricas_procesadas[size_str]['time_ms'] = round(sum(all_times) / len(all_times), 2)
                metricas_procesadas[size_str]['memory_mb'] = round(sum(all_mems) / len(all_mems), 2)



=======
        # Procesar para formato visual
        metricas_procesadas = {}
        for size_str, metrics in benchmarks.items():
            size = int(size_str)
            metricas_procesadas[size] = {
                'n': size,
                'time_ms': round(metrics['time_ms_mean'], 2),
                'memory_mb': round(metrics['mem_bytes_peak_mean'] / (1024 * 1024), 2),
                'samples_time': [round(t, 2) for t in metrics.get('time_ms_samples', [])],
                'samples_memory': [round(m / (1024 * 1024), 2) for m in metrics.get('mem_bytes_peak_samples', [])]
            }
>>>>>>> f070f6795f7f9920715de3874a4d1595fa6f3425
        
        # Detectar alertas de rendimiento
        alertas = detectar_alertas(metricas_procesadas)
        
        # Obtener resumen del análisis si está disponible
        resumen_analisis = None
        bob_files = list(BOB_SESSIONS_DIR.glob('*.md'))
        if bob_files:
            # Tomar el archivo más reciente
            archivo_mas_reciente = sorted(bob_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
            contenido_md = archivo_mas_reciente.read_text(encoding='utf-8')
            resumen_analisis = resumir_analisis_md(contenido_md)
        
        return jsonify({
            "success": True,
            "mensaje": "✅ Benchmarks completados exitosamente",
            "metricas": metricas_procesadas,
            "alertas": alertas,
            "resumen_analisis": resumen_analisis,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"❌ Error en benchmarks: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/resumen-analisis/<nombre>', methods=['GET'])
def obtener_resumen_analisis(nombre):
    """Obtiene el resumen procesado de un análisis MD."""
    try:
        ruta = BOB_SESSIONS_DIR / nombre
        
        if not ruta.exists():
            return jsonify({"error": f"Archivo no encontrado: {nombre}"}), 404
        
        contenido = ruta.read_text(encoding='utf-8')
        resumen = resumir_analisis_md(contenido)
        
        return jsonify({
            "success": True,
            "nombre": nombre,
            "resumen": resumen,
            "contenido_completo": contenido  # También devolver para PDF si es necesario
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def detectar_alertas(metricas):
    """Detecta problemas de rendimiento y genera alertas."""
    alertas = []
    
    if not metricas:
        return alertas
    
<<<<<<< HEAD
    # Obtener valores ordenados por tamaño (convertir a int para ordenar correctamente)
    sizes = sorted(metricas.keys(), key=lambda x: int(x) if isinstance(x, str) else x)
    valores_tiempo = [metricas[s]['time_ms'] for s in sizes]
    valores_memoria = [metricas[s]['memory_mb'] for s in sizes]
    
    # Convertir tamaños a int para comparaciones
    sizes_int = [int(s) if isinstance(s, str) else s for s in sizes]
    
=======
    # Obtener valores ordenados por tamaño
    sizes = sorted(metricas.keys())
    valores_tiempo = [metricas[s]['time_ms'] for s in sizes]
    valores_memoria = [metricas[s]['memory_mb'] for s in sizes]
    
>>>>>>> f070f6795f7f9920715de3874a4d1595fa6f3425
    # Detectar crecimiento exponencial
    if len(valores_tiempo) >= 2:
        for i in range(1, len(valores_tiempo)):
            tiempo_actual = valores_tiempo[i]
            tiempo_anterior = valores_tiempo[i-1]
<<<<<<< HEAD
            size_actual = sizes_int[i]
            size_anterior = sizes_int[i-1]
=======
            size_actual = sizes[i]
            size_anterior = sizes[i-1]
>>>>>>> f070f6795f7f9920715de3874a4d1595fa6f3425
            
            if tiempo_anterior > 0:
                ratio_tiempo = tiempo_actual / tiempo_anterior
                ratio_tamaño = size_actual / size_anterior
                
                # Si el tiempo crece mucho más que linealmente
                if ratio_tiempo > ratio_tamaño * 2:
                    alertas.append({
                        'tipo': 'COMPLEJIDAD_ALTA',
                        'nivel': 'warning',
                        'icono': '⚠️',
                        'mensaje': f'Crecimiento no lineal: N={size_anterior}→{size_actual}, tiempo crece {ratio_tiempo:.1f}x (esperado ~{ratio_tamaño:.1f}x)',
                        'tamaños': [size_anterior, size_actual]
                    })
                
                # Si el tiempo supera 1 segundo
                if tiempo_actual > 1000:
                    alertas.append({
                        'tipo': 'TIEMPO_CRITICO',
                        'nivel': 'error',
                        'icono': '🔴',
                        'mensaje': f'Tiempo crítico en N={size_actual}: {tiempo_actual:.0f}ms (>1s)',
                        'tamaño': size_actual
                    })
    
    # Alertas de memoria
    max_memoria = max(valores_memoria) if valores_memoria else 0
    if max_memoria > 100:
        alertas.append({
            'tipo': 'MEMORIA_ALTA',
            'nivel': 'warning',
            'icono': '💾',
            'mensaje': f'Consumo de memoria elevado: {max_memoria:.1f} MB',
            'valor_mb': max_memoria
        })
    
    # Estimar complejidad basándose en el patrón de crecimiento
    if len(valores_tiempo) >= 3:
        ratios = []
        for i in range(1, len(valores_tiempo)):
            if valores_tiempo[i-1] > 0:
                ratios.append(valores_tiempo[i] / valores_tiempo[i-1])
        
        promedio_ratio = sum(ratios) / len(ratios) if ratios else 1
        
        if promedio_ratio > 10:
            alertas.append({
                'tipo': 'COMPLEJIDAD_ESTIMADA',
                'nivel': 'info',
                'icono': '📊',
                'mensaje': f'Complejidad estimada: O(N³) o peor (ratio promedio: {promedio_ratio:.1f}x)',
                'ratio': promedio_ratio
            })
        elif promedio_ratio > 2.5:
            alertas.append({
                'tipo': 'COMPLEJIDAD_ESTIMADA',
                'nivel': 'info',
                'icono': '📊',
                'mensaje': f'Complejidad estimada: O(N²) (ratio promedio: {promedio_ratio:.1f}x)',
                'ratio': promedio_ratio
            })
    
    return alertas


def resumir_analisis_md(contenido_md, max_puntos=5):
    """Extrae y resume los puntos clave del análisis MD.
    
    Args:
        contenido_md: Contenido del archivo markdown
        max_puntos: Máximo número de puntos clave a extraer
    
    Returns:
        dict con resumen estructurado
    """
    resumen = {
        'titulo': '',
        'puntos_clave': [],
        'cuellos_botella': [],
        'recomendaciones': [],
        'metricas': {}
    }
    
    lineas = contenido_md.split('\n')
    
    # Extraer título principal
    for linea in lineas:
        if linea.startswith('# '):
            resumen['titulo'] = linea.replace('# ', '').strip()
            break
    
    # Extraer secciones principales
    seccion_actual = None
    buffer = []
    
    for linea in lineas:
        if linea.startswith('## '):
            # Procesar sección anterior
            if seccion_actual and buffer:
                texto = '\n'.join(buffer).strip()
                if seccion_actual == 'CUELLOS DE BOTELLA':
                    # Extraer problemas marcados con 🔴
                    if '🔴' in texto:
                        problemas = re.findall(r'🔴.*?(?=🔴|$)', texto, re.DOTALL)
                        for p in problemas:
                            linea_problema = p.strip().split('\n')[0]
                            resumen['cuellos_botella'].append(linea_problema.replace('🔴', '').strip())
                elif seccion_actual == 'RECOMENDACIONES':
                    # Extraer recomendaciones numeradas
                    recs = re.findall(r'\d+\.\s+(.*?)(?=\d+\.|$)', texto, re.DOTALL)
                    for r in recs[:max_puntos]:
                        resumen['recomendaciones'].append(r.strip().split('\n')[0])
            
            seccion_actual = linea.replace('## ', '').strip().split(' ')[0]
            buffer = []
        else:
            buffer.append(linea)
    
    # Extraer complejidades
    complejidades = re.findall(r'O\([^)]+\)', contenido_md)
    resumen['metricas']['complejidades_encontradas'] = list(set(complejidades))
    
    # Si no encontramos suficientes puntos clave, extraer del resumen general
    if not resumen['puntos_clave']:
        # Buscar líneas que empiezan con "**" o "- "
        for linea in lineas:
            if (linea.startswith('**') or linea.startswith('- ')) and len(resumen['puntos_clave']) < max_puntos:
                punto = linea.replace('**', '').replace('- ', '').strip()
                if punto and len(punto) > 10:
                    resumen['puntos_clave'].append(punto[:100] + '...' if len(punto) > 100 else punto)
    
    return resumen


@app.route('/api/integrar-watsonx', methods=['POST'])
def integrar_watsonx():
    """Integra análisis de Bob IDE + benchmarks con watsonx.ai."""
    try:
        data = request.get_json()
        
        if not data or 'bob_analysis_file' not in data:
            return jsonify({"error": "Falta campo 'bob_analysis_file'"}), 400
        
        bob_file = data['bob_analysis_file']
        codigo = data.get('codigo', '')
        
        # Cargar análisis de Bob
        bob_path = BOB_SESSIONS_DIR / bob_file
        if not bob_path.exists():
            return jsonify({"error": f"❌ Archivo Bob no encontrado: {bob_file}"}), 404
        
        bob_analysis = bob_path.read_text(encoding='utf-8')
        
        # Cargar métricas locales
        metricas_path = DATA_DIR / "metricas_salida.json"
        metricas = {}
        if metricas_path.exists():
            metricas = json.loads(metricas_path.read_text(encoding='utf-8'))
        
        # Enviar a watsonx.ai
        print("🔗 Integrando con watsonx.ai...")
        resultado_watsonx = summarize_metrics(bob_analysis)
        
        # Generar reporte final
        reporte_final = f"""# 📊 REPORTE FINAL QA — OptiCode

## 🔍 Análisis de Bob IDE

{bob_analysis}

---

## ⚡ Métricas Prácticas (Motor Local)

```json
{json.dumps(metricas, indent=2)}
```

---

## 🤖 Resumen de watsonx.ai

{resultado_watsonx if resultado_watsonx else "Integración aún no configurada."}

---

**Generado automáticamente por OptiCode QA**
**Fecha:** {datetime.now().isoformat()}
"""
        
        # Guardar reporte
        reporte_path = OUTPUT_DIR / "REPORTE_FINAL_QA.md"
        reporte_path.write_text(reporte_final, encoding='utf-8')
        
        return jsonify({
            "success": True,
            "mensaje": "✅ Integración completada exitosamente",
            "archivo_reporte": str(reporte_path),
            "resumen_watsonx": resultado_watsonx or "Resumen disponible después de integración completa"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"❌ Error en integración: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/reportes', methods=['GET'])
def listar_reportes():
    """Lista reportes finales generados."""
    try:
        reportes = []
        
        if OUTPUT_DIR.exists():
            for archivo in sorted(OUTPUT_DIR.glob('*.md')):
                contenido = archivo.read_text(encoding='utf-8')
                reportes.append({
                    "nombre": archivo.name,
                    "contenido_preview": contenido[:300],
                    "tamaño": len(contenido)
                })
        
        return jsonify({
            "success": True,
            "total": len(reportes),
            "reportes": reportes
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/reportes/<nombre>', methods=['GET'])
def descargar_reporte(nombre):
    """Descarga un reporte específico."""
    try:
        ruta = OUTPUT_DIR / nombre
        
        if not ruta.exists():
            return jsonify({"error": f"Reporte no encontrado: {nombre}"}), 404
        
        contenido = ruta.read_text(encoding='utf-8')
        
        return jsonify({
            "success": True,
            "nombre": nombre,
            "contenido": contenido
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/estado', methods=['GET'])
def estado():
    """Devuelve estado del sistema."""
    try:
        bob_files = len(list(BOB_SESSIONS_DIR.glob('*.md')))
        reportes = len(list(OUTPUT_DIR.glob('*.md')))
        metricas_existe = (DATA_DIR / "metricas_salida.json").exists()
        
        return jsonify({
            "success": True,
            "sistema": "OptiCode QA — PASO 1 Real",
            "estado": "✅ Operacional",
            "archivos_bob": bob_files,
            "reportes_generados": reportes,
            "metricas_disponibles": metricas_existe,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 SERVIDOR OptiCode QA — PASO 1 REAL")
    print("=" * 70)
    print("\n📁 Flujo: Bob IDE (manual) → Motor Local → watsonx.ai")
    print("\n🌐 Dashboard disponible en: http://localhost:5000")
    print("\n🔗 API Endpoints:")
    print("   GET  /api/bob-sessions - Lista análisis de Bob IDE")
    print("   GET  /api/codigos - Lista códigos disponibles")
<<<<<<< HEAD
    print("   POST /api/analizar-codigo-personalizado - Analiza código pegado")
=======
>>>>>>> f070f6795f7f9920715de3874a4d1595fa6f3425
    print("   POST /api/ejecutar-benchmarks - Ejecuta benchmarks")
    print("   POST /api/integrar-watsonx - Integra y genera reporte")
    print("   GET  /api/reportes - Lista reportes finales")
    print("   GET  /api/estado - Estado del sistema")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)
