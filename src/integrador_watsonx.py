"""Integrador con watsonx.ai — lógica completa de Alex adaptada para la GUI de Harry.

Cruza el análisis teórico de Bob IDE con las métricas del motor QA
y genera un veredicto final usando IBM watsonx.ai (Llama 3.3 70B).
"""
import json
import sys
from pathlib import Path

# Configuración de rutas
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
DATA_DIR = RAIZ_PROYECTO / 'data'
BOB_SESSIONS_DIR = RAIZ_PROYECTO / 'output' / 'informesbob'

# =========================================================================
# CREDENCIALES — Leer SOLO desde variables de entorno (.env)
# =========================================================================
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    API_KEY    = os.getenv('WATSONX_API_KEY')
    PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
    URL_ENDPOINT = os.getenv('WATSONX_URL')
    
    if not all([API_KEY, PROJECT_ID, URL_ENDPOINT]):
        raise ValueError("Faltan credenciales en .env: WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL")
except ImportError:
    print("ERROR: python-dotenv no instalado. Instala con: pip install python-dotenv")
    sys.exit(1)


# =========================================================================
# FUNCIÓN PRINCIPAL — llamada desde servidor_paso1_web.py de Harry
# Firma: summarize_metrics(bob_analysis_text: str) -> str | None
# =========================================================================
def summarize_metrics(bob_analysis_text: str) -> str | None:
    """Envía el análisis de Bob IDE + métricas locales a watsonx.ai y retorna el veredicto."""
    # Cargar métricas del motor QA
    metricas_path = DATA_DIR / 'metricas_salida.json'
    practica_json = {}
    if metricas_path.exists():
        with open(metricas_path, 'r', encoding='utf-8') as f:
            practica_json = json.load(f)

    # Construcción del prompt (igual que en Alex)
    prompt = f"""Actúa como un Ingeniero Principal de QA y DevOps en IBM Cloud.
Tu misión es generar un "Veredicto Final de Rendimiento y Escalabilidad Cloud" cruzando un análisis teórico con métricas reales de un stress test.

=== 1. AUDITORÍA TEÓRICA DE COGNICIÓN (IBM Bob IDE) ===
{bob_analysis_text}

=== 2. MÉTRICAS REALES DE RENDIMIENTO LOCAL (JSON) ===
{json.dumps(practica_json, indent=2)}

=== INSTRUCCIONES DE REDACCIÓN ===
1. **Validación Cruzada:** Determina si los tiempos promedios reales (time_ms_mean) del JSON concuerdan asintóticamente con la complejidad teórica Big O descrita.
2. **Comparación DFS vs LDFS vs IDFS:** Si existen métricas diferenciadas, compara el comportamiento de los tres algoritmos.
3. **Impacto Cloud:** Explica cómo afectaría a la RAM en producción según los picos medidos (mem_bytes_peak_mean) en un entorno de tráfico masivo.
4. **Conclusión General:** Da una calificación de escalabilidad (Aprobado / No Aprobado) y una recomendación clave.

Por favor, genera tu respuesta en un formato Markdown impecable y ejecutivo.
"""

    try:
        from ibm_watsonx_ai import APIClient
        from ibm_watsonx_ai.foundation_models import ModelInference

        credentials = {"url": URL_ENDPOINT, "apikey": API_KEY}

        model = ModelInference(
            model_id = "ibm/granite-8b-code-instruct",
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 1000,
                "repetition_penalty": 1.0
            },
            credentials=credentials,
            project_id=PROJECT_ID
        )

        print("Conectando con watsonx.ai (Llama 3.3 70B)...")
        resultado = model.generate_text(prompt=prompt)

        # Guardar veredicto en data/
        ruta_salida = DATA_DIR / 'veredicto_final_auditoria.md'
        ruta_salida.write_text(resultado, encoding='utf-8')
        print(f"Veredicto guardado en: {ruta_salida}")

        return resultado

    except ImportError:
        print("WARNING: ibm-watsonx-ai no instalado. Retornando resumen simulado.")
        return _resumen_simulado(practica_json)
    except Exception as e:
        print(f"Error en watsonx.ai: {e}")
        return _resumen_simulado(practica_json)


def _resumen_simulado(practica_json: dict) -> str:
    """Genera un resumen local cuando watsonx no está disponible."""
    benchmarks = practica_json.get('benchmarks', {})
    lineas = ["## Resumen Local (watsonx no disponible)\n"]
    for size, m in sorted(benchmarks.items(), key=lambda x: int(x[0])):
        t = m.get('time_ms_mean', m.get('dfs', {}).get('time_ms_mean', 0))
        mem = m.get('mem_bytes_peak_mean', m.get('dfs', {}).get('mem_bytes_peak_mean', 0))
        lineas.append(f"- **N={size}**: tiempo promedio `{t:.4f} ms`, memoria pico `{mem // 1024} KB`")
    lineas.append("\n> Configura `ibm-watsonx-ai` para el análisis completo con IA.")
    return "\n".join(lineas)


# =========================================================================
# EJECUCIÓN DIRECTA (opcional, igual que en Alex)
# =========================================================================
def generar_veredicto_final():
    """Ejecuta la integración completa desde línea de comandos."""
    # Buscar reporte teórico
    ruta_teoria = None
    for ruta in [RAIZ_PROYECTO / 'reporte_analisis_algoritmo.md',
                 *list(BOB_SESSIONS_DIR.glob('*.md')),
                 *list(RAIZ_PROYECTO.glob('*.md'))]:
        if ruta.exists() and 'README' not in ruta.name:
            ruta_teoria = ruta
            break

    if not ruta_teoria:
        print("Error: No se encontro reporte teorico (.md). Genera uno primero.")
        sys.exit(1)

    print(f"Leyendo reporte teorico: {ruta_teoria.name}")
    teoria = ruta_teoria.read_text(encoding='utf-8')

    resultado = summarize_metrics(teoria)
    if resultado:
        print("\n--- VEREDICTO ---\n")
        print(resultado[:500], "...\n(ver archivo completo en data/veredicto_final_auditoria.md)")


if __name__ == '__main__':
    generar_veredicto_final()
