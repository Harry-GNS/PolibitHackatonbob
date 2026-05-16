"""Script simple para iniciar el servidor OptiCode QA."""

import sys
import os
from pathlib import Path

# Añadir src al path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

# Cambiar al directorio del proyecto
os.chdir(ROOT)

# Importar y ejecutar servidor
from servidor_paso1 import app

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 OptiCode QA - PASO 1 Automático")
    print("=" * 70)
    print("\n📊 Dashboard disponible en: http://localhost:5000")
    print("🔌 API REST disponible en: http://localhost:5000/api/")
    print("\n💡 Abre tu navegador en: http://localhost:5000")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
