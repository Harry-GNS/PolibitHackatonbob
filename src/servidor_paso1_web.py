"""Servidor Flask con interfaz web bonita para PASO 1 Real

Flujo: Bob IDE (manual) → Motor Local → watsonx.ai
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import json
import traceback
import sys
from datetime import datetime

# Añadir el directorio raíz al path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from motor_qa import run_benchmarks
from integrador_watsonx import summarize_metrics

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
        
        # Detectar alertas de rendimiento
        alertas = detectar_alertas(metricas_procesadas)
        
        return jsonify({
            "success": True,
            "mensaje": "✅ Benchmarks completados exitosamente",
            "metricas": metricas_procesadas,
            "alertas": alertas,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"❌ Error en benchmarks: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500


def detectar_alertas(metricas):
    """Detecta problemas de rendimiento y genera alertas."""
    alertas = []
    
    if not metricas:
        return alertas
    
    # Obtener valores ordenados por tamaño
    sizes = sorted(metricas.keys())
    valores_tiempo = [metricas[s]['time_ms'] for s in sizes]
    valores_memoria = [metricas[s]['memory_mb'] for s in sizes]
    
    # Detectar crecimiento exponencial
    if len(valores_tiempo) >= 2:
        for i in range(1, len(valores_tiempo)):
            tiempo_actual = valores_tiempo[i]
            tiempo_anterior = valores_tiempo[i-1]
            size_actual = sizes[i]
            size_anterior = sizes[i-1]
            
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
    print("   POST /api/ejecutar-benchmarks - Ejecuta benchmarks")
    print("   POST /api/integrar-watsonx - Integra y genera reporte")
    print("   GET  /api/reportes - Lista reportes finales")
    print("   GET  /api/estado - Estado del sistema")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)
