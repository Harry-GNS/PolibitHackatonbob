#!/usr/bin/env python3
"""Script para iniciar el servidor web de OptiCode QA PASO 1

Uso:
    python iniciar_web.py

Luego abre: http://localhost:5000
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

# Directorio del proyecto
ROOT = Path(__file__).resolve().parent

print("\n" + "=" * 70)
print("🚀 INICIANDO OptiCode QA — PASO 1 Web")
print("=" * 70)

# Verificar que Flask está instalado
try:
    import flask
except ImportError:
    print("\n❌ Flask no está instalado")
    print("   Instala con: pip install -r requirements.txt")
    sys.exit(1)

# Iniciar servidor
print("\n📁 Directorio del proyecto:", ROOT)
print("🔗 URL: http://localhost:5000")
print("\n⏳ Iniciando servidor Flask...\n")

# Cambiar a directorio del proyecto
os.chdir(ROOT)

# Esperar un poco y abrir navegador
def abrir_navegador():
    time.sleep(2)
    print("🌐 Abriendo navegador...")
    webbrowser.open('http://localhost:5000')

import threading
threading.Thread(target=abrir_navegador, daemon=True).start()

# Ejecutar servidor
try:
    subprocess.run([sys.executable, 'src/servidor_paso1_web.py'])
except KeyboardInterrupt:
    print("\n\n✋ Servidor detenido por el usuario")
    sys.exit(0)
