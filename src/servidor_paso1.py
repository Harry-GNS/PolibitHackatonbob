"""Servidor Flask REAL para PASO 1 - Bob IDE + Motor Local + watsonx.ai

Flujo:
1. Carga análisis .md de bob_sessions (creado manualmente en Bob IDE)
2. Ejecuta motor_qa.py para benchmarks prácticos
3. Integra con watsonx.ai para reporte final
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import json
import traceback
import sys

# Añadir el directorio raíz al path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from motor_qa import run_benchmarks
from integrador_watsonx import summarize_metrics

app = Flask(__name__)
CORS(app)

BOB_SESSIONS_DIR = ROOT / "bob_sessions"
OUTPUT_DIR = ROOT / "output"
DATA_DIR = ROOT / "data"

# Crear directorios si no existen
BOB_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


@app.route('/')
def index():
    """Sirve página de bienvenida."""
    return jsonify({
        "sistema": "OptiCode QA — PASO 1 Real",
        "flujo": "Bob IDE (manual) → Motor Local (benchmarks) → watsonx.ai (reporte)",
        "endpoints": {
            "bob_sessions": "GET /api/bob-sessions - Lista análisis de Bob IDE",
            "benchmarks": "POST /api/ejecutar-benchmarks - Ejecuta benchmarks locales",
            "integracion": "POST /api/integrar-watsonx - Integra teoría + práctica",
            "reportes": "GET /api/reportes - Lista reportes finales"
        }
    })


@app.route('/api/bob-sessions', methods=['GET'])
def listar_bob_sessions():
    """Lista todos los análisis .md generados por Bob IDE en bob_sessions/"""
    try:
        archivos = []
        
        if BOB_SESSIONS_DIR.exists():
            for archivo in sorted(BOB_SESSIONS_DIR.glob('*.md')):
                contenido = archivo.read_text(encoding='utf-8')
                archivos.append({
                    "nombre": archivo.name,
                    "ruta": str(archivo),
                    "contenido": contenido[:500],  # Primeros 500 caracteres
                    "tamaño": len(contenido),
                    "tipo": "Bob IDE Analysis"
                })
        
        return jsonify({
            "success": True,
            "total": len(archivos),
            "archivos": archivos
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


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
            "ruta": str(ruta),
            "contenido": contenido
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/ejecutar-benchmarks', methods=['POST'])
def ejecutar_benchmarks():
    """Ejecuta motor_qa.py para benchmarks prácticos.
    
    Body JSON esperado:
    {
        "archivo_codigo": "src/algoritmos.py" (opcional)
    }
    """
    try:
        print("⚡ Iniciando benchmarks locales...")
        
        # Ejecutar motor_qa
        resultados = run_benchmarks()
        
        # Los resultados se guardan en data/metricas_salida.json
        metricas_path = DATA_DIR / "metricas_salida.json"
        
        if metricas_path.exists():
            metricas = json.loads(metricas_path.read_text(encoding='utf-8'))
        else:
            metricas = {}
        
        return jsonify({
            "success": True,
            "mensaje": "Benchmarks completados exitosamente",
            "archivo_metricas": str(metricas_path),
            "metricas": metricas
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/integrar-watsonx', methods=['POST'])
def integrar_watsonx():
    """Integra análisis de Bob IDE + benchmarks locales en watsonx.ai.
    
    Body JSON esperado:
    {
        "bob_analysis_file": "bob_task_...md",
        "codigo": "código fuente Python"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'bob_analysis_file' not in data:
            return jsonify({"error": "Falta campo 'bob_analysis_file'"}), 400
        
        bob_file = data['bob_analysis_file']
        codigo = data.get('codigo', '')
        
        # Cargar análisis de Bob
        bob_path = BOB_SESSIONS_DIR / bob_file
        if not bob_path.exists():
            return jsonify({"error": f"Archivo Bob no encontrado: {bob_file}"}), 404
        
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

## ⚡ Métricas Prácticas
```json
{json.dumps(metricas, indent=2)}
```

## 🤖 Resumen de watsonx.ai
{resultado_watsonx if resultado_watsonx else "Integración aún no configurada."}

---
**Generado automáticamente por OptiCode QA**
"""
        
        # Guardar reporte
        reporte_path = OUTPUT_DIR / "REPORTE_FINAL_QA.md"
        reporte_path.write_text(reporte_final, encoding='utf-8')
        
        return jsonify({
            "success": True,
            "mensaje": "Integración completada",
            "archivo_reporte": str(reporte_path),
            "resumen_watsonx": resultado_watsonx
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/reportes', methods=['GET'])
def listar_reportes():
    """Lista reportes finales generados."""
    try:
        reportes = []
        
        if OUTPUT_DIR.exists():
            for archivo in sorted(OUTPUT_DIR.glob('*.md')):
                reportes.append({
                    "nombre": archivo.name,
                    "ruta": str(archivo),
                    "tamaño": archivo.stat().st_size
                })
        
        return jsonify({
            "success": True,
            "total": len(reportes),
            "reportes": reportes
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


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
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Servidor OptiCode QA — PASO 1 REAL iniciado")
    print("=" * 60)
    print("📁 Flujo: Bob IDE (manual) → Motor Local → watsonx.ai")
    print("=" * 60)
    print("\n🔗 Endpoints disponibles:\n")
    print("  GET  /api/bob-sessions - Lista análisis de Bob IDE")
    print("  GET  /api/bob-sessions/<nombre> - Obtiene análisis completo")
    print("  POST /api/ejecutar-benchmarks - Ejecuta benchmarks locales")
    print("  POST /api/integrar-watsonx - Integra todo en reporte final")
    print("  GET  /api/reportes - Lista reportes finales")
    print("  GET  /api/reportes/<nombre> - Descarga reporte")
    print("\n📊 Dashboard disponible en: http://localhost:5000")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
