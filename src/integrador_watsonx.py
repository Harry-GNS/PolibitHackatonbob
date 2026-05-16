"""Script integrador que cruza teoría y práctica, y envía el contexto a watsonx.ai."""
import json
import sys
from pathlib import Path
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference

# Configuración de rutas
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
DATA_DIR = RAIZ_PROYECTO / 'data'
BOB_SESSIONS = RAIZ_PROYECTO / 'bob_sessions'

# =========================================================================
# 1. CREDENCIALES CONFIGURADAS CON EL SANDBOX PRE-CONECTADO
# =========================================================================
API_KEY = "r7N0t-5xbndvsYVshMeoE1Ax_SSbLrbAbh0UM6TrDgIu"
PROJECT_ID = "a4b3f3fe-9336-4169-8a54-d22d88de90a6"
URL_ENDPOINT = "https://us-south.ml.cloud.ibm.com" 

# =========================================================================
# 2. CARGA DE RESULTADOS DE LAS FASES 1 Y 2
# =========================================================================
def cargar_contexto():
    ruta_teoria = RAIZ_PROYECTO / 'reporte_analisis_algoritmo.md'
    ruta_practica = DATA_DIR / 'metricas_salida.json'

    # Búsqueda flexible por si el reporte tiene el nombre largo de Bob
    if not ruta_teoria.exists():
        archivos_md = list(RAIZ_PROYECTO.glob("*.md")) + list(BOB_SESSIONS.glob("*.md"))
        if archivos_md:
            ruta_teoria = archivos_md[0]

    if not ruta_teoria or not ruta_practica.exists():
        print("❌ Error: Asegúrate de tener el reporte Markdown y el archivo metricas_salida.json listos.")
        sys.exit(1)

    print(f"📄 Leyendo reporte teórico desde: {ruta_teoria.name}")
    with open(ruta_teoria, "r", encoding="utf-8") as f:
        teoria_md = f.read()

    print(f"📊 Leyendo métricas reales desde: {ruta_practica.name}")
    with open(ruta_practica, "r", encoding="utf-8") as f:
        practica_json = json.load(f)

    return teoria_md, practica_json

# =========================================================================
# 3. EJECUCIÓN E INTEGRACIÓN CON WATSONX
# =========================================================================
def generar_veredicto_final():
    print("📥 Cargando datos de auditoría...")
    teoria, practica = cargar_contexto()

    # Construcción del prompt unificado para el modelo de IBM
    prompt_conglomerado = f"""Actúa como un Ingeniero Principal de QA y DevOps en IBM Cloud. 
Tu misión es generar un "Veredicto Final de Rendimiento y Escalabilidad Cloud" cruzando un análisis teórico con métricas reales de un stress test.

=== 1. AUDITORÍA TEÓRICA DE COGNICIÓN (IBM Bob IDE) ===
{teoria}

=== 2. MÉTRICAS REALES DE RENDIMIENTO LOCAL (JSON) ===
{json.dumps(practica, indent=2)}

=== INSTRUCCIONES DE REDACCIÓN ===
1. **Validación Cruzada:** Determina si los tiempos promedios reales (time_ms_mean) del JSON concuerdan asintóticamente con la complejidad teórica Big O descrita.
2. **Impacto Cloud:** Explica cómo afectaría a la RAM en producción según los picos medidos (mem_bytes_peak_mean) en un entorno de tráfico masivo.
3. **Conclusión General:** Da una calificación de escalabilidad (Aprobado / No Aprobado) y una recomendación clave.

Por favor, genera tu respuesta en un formato Markdown impecable y ejecutivo.
"""

    print("🔌 Conectando con la API de watsonx.ai...")
    
    credentials = {
        "url": URL_ENDPOINT,
        "apikey": API_KEY
    }
    
    client = APIClient(credentials)
    
    # Cambiado al modelo Llama 3.3 70B que sí está soportado y es súper potente
    model_id = "meta-llama/llama-3-3-70b-instruct" 
    
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 1000,
        "repetition_penalty": 1.0
    }

    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=PROJECT_ID
    )

    print("🤖 El Agente de watsonx en la nube está cruzando y analizando tus datos...")
    resultado = model.generate_text(prompt=prompt_conglomerado)

    # Guardar el veredicto definitivo en la carpeta data
    ruta_salida = DATA_DIR / 'veredicto_final_auditoria.md'
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(resultado)

    print(f"\n🎉 ¡VEREDICTO GENERADO CON ÉXITO!")
    print(f"📁 Revisa tu archivo en: {ruta_salida}")

if __name__ == "__main__":
    generar_veredicto_final()