"""GUI REAL del PASO 1 - Integración de Bob IDE + Motor Local + watsonx.ai

Flujo correcto:
1. Carga análisis .md de bob_sessions (creado manualmente en Bob IDE)
2. Ejecuta motor_qa.py para benchmarks prácticos
3. Integra con watsonx.ai para reporte final
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from motor_qa import run_benchmarks
from integrador_watsonx import summarize_metrics


class PasoUnoGUI:
    """GUI para PASO 1 real con Bob IDE + Motor Local + watsonx.ai"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OptiCode QA — PASO 1 (Bob IDE + Motor Local + watsonx.ai)")
        self.root.geometry("1200x700")
        
        self.bob_analysis_path = None
        self.metrics_path = None
        self.codigo = None
        
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        
        self._build_ui()
    
    def _build_ui(self):
        """Construye la interfaz."""
        
        # Header
        header = ttk.Frame(self.root, relief='sunken')
        header.pack(fill='x', padx=10, pady=10)
        
        title = ttk.Label(header, text="🎯 PASO 1: Análisis Teórico + Práctico + Integración Final", 
                         font=('Arial', 14, 'bold'))
        title.pack()
        
        subtitle = ttk.Label(header, text="Flujo: Bob IDE (manual) → Motor Local (benchmarks) → watsonx.ai (reporte)",
                            font=('Arial', 10))
        subtitle.pack()
        
        # Main layout
        main = ttk.Frame(self.root)
        main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ========== LEFT: INPUTS ==========
        left = ttk.LabelFrame(main, text="📥 ENTRADAS", padding=10)
        left.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # 1. Bob IDE Analysis
        ttk.Label(left, text="1️⃣ Análisis de Bob IDE (.md)", font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)
        ttk.Label(left, text="Archivo generado manualmente en Bob IDE y guardado en bob_sessions/",
                 font=('Arial', 9), foreground='gray').pack(anchor='w')
        
        bob_frame = ttk.Frame(left)
        bob_frame.pack(fill='x', pady=5)
        ttk.Button(bob_frame, text="📂 Cargar .md de bob_sessions", 
                  command=self._load_bob_analysis).pack(side='left', padx=5)
        self.bob_status = ttk.Label(bob_frame, text="No cargado", foreground='red')
        self.bob_status.pack(side='left', padx=5)
        
        # 2. Source Code
        ttk.Label(left, text="2️⃣ Código Fuente para Benchmarks", font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)
        
        code_frame = ttk.Frame(left)
        code_frame.pack(fill='x', pady=5)
        ttk.Button(code_frame, text="📂 Cargar .py (algoritmos)", 
                  command=self._load_code).pack(side='left', padx=5)
        self.code_status = ttk.Label(code_frame, text="No cargado", foreground='red')
        self.code_status.pack(side='left', padx=5)
        
        # 3. Credentials for watsonx
        ttk.Label(left, text="3️⃣ Credenciales watsonx.ai (del .env)", font=('Arial', 10, 'bold')).pack(anchor='w', pady=5)
        ttk.Label(left, text="Se cargan automáticamente de .env. Verifica que existan.",
                 font=('Arial', 9), foreground='gray').pack(anchor='w')
        
        ttk.Button(left, text="✓ Verificar credenciales", 
                  command=self._verify_credentials).pack(fill='x', pady=5)
        
        # ========== CENTER: CONTROLS ==========
        center = ttk.LabelFrame(main, text="⚙️ CONTROLES", padding=10)
        center.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        ttk.Button(center, text="▶️ PASO 1: Ejecutar Benchmarks Locales", 
                  command=self._execute_benchmarks,
                  width=30).pack(fill='x', pady=10)
        
        ttk.Separator(center, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Button(center, text="🔗 PASO 2: Integrar con watsonx.ai", 
                  command=self._integrate_watsonx,
                  width=30).pack(fill='x', pady=10)
        
        ttk.Separator(center, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Button(center, text="📊 Ver Reporte Final", 
                  command=self._view_report,
                  width=30).pack(fill='x', pady=10)
        
        ttk.Button(center, text="🎥 Abrir Bob IDE en VS Code", 
                  command=self._open_bob_ide,
                  width=30).pack(fill='x', pady=10)
        
        # ========== RIGHT: LOG ==========
        right = ttk.LabelFrame(main, text="📋 LOG", padding=10)
        right.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        
        self.log = tk.Text(right, height=20, width=40, font=('Courier', 9))
        self.log.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(right, command=self.log.yview)
        self.log.config(yscrollcommand=scrollbar.set)
        
        ttk.Button(right, text="🗑️ Limpiar Log", command=lambda: self.log.delete('1.0', 'end')).pack(pady=5)
        
        # Configure grid weights
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=1)
        main.rowconfigure(0, weight=1)
    
    def _log(self, message):
        """Añade mensaje al log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.insert('end', f"[{timestamp}] {message}\n")
        self.log.see('end')
        self.root.update()
    
    def _load_bob_analysis(self):
        """Carga archivo .md de bob_sessions."""
        file = filedialog.askopenfilename(
            initialdir=str(ROOT / "bob_sessions"),
            filetypes=[("Markdown", "*.md"), ("Todos", "*.*")]
        )
        if file:
            self.bob_analysis_path = file
            self.bob_status.config(text=f"✓ {Path(file).name}", foreground='green')
            self._log(f"Bob IDE analysis cargado: {Path(file).name}")
    
    def _load_code(self):
        """Carga archivo .py para benchmarks."""
        file = filedialog.askopenfilename(
            initialdir=str(ROOT / "src"),
            filetypes=[("Python", "*.py"), ("Todos", "*.*")]
        )
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                self.codigo = f.read()
            self.code_status.config(text=f"✓ {Path(file).name}", foreground='green')
            self._log(f"Código cargado: {Path(file).name}")
    
    def _verify_credentials(self):
        """Verifica credenciales de watsonx.ai."""
        try:
            from dotenv import load_dotenv
            import os
            
            load_dotenv(ROOT / ".env")
            
            creds = {
                "ibm_cloud_auth_url": os.getenv("IBM_CLOUD_AUTH_URL"),
                "project_id": os.getenv("PROJECT_ID"),
                "model_id": os.getenv("MODEL_ID"),
            }
            
            if all(creds.values()):
                self._log("✅ Credenciales watsonx.ai OK")
                messagebox.showinfo("OK", "Credenciales verificadas ✓")
            else:
                self._log("❌ Credenciales incompletas. Verifica .env")
                messagebox.showerror("Error", "Faltan credenciales en .env")
        except Exception as e:
            self._log(f"❌ Error al verificar: {e}")
            messagebox.showerror("Error", str(e))
    
    def _execute_benchmarks(self):
        """Ejecuta motor_qa.py para benchmarks."""
        if not self.codigo:
            messagebox.showwarning("Advertencia", "Carga primero el código")
            return
        
        self._log("⚡ Iniciando benchmarks locales...")
        try:
            # Ejecutar motor_qa
            metricas = run_benchmarks()
            self.metrics_path = ROOT / "data" / "metricas_salida.json"
            self._log(f"✅ Benchmarks completados. Métricas: {self.metrics_path}")
        except Exception as e:
            self._log(f"❌ Error en benchmarks: {e}")
            messagebox.showerror("Error", str(e))
    
    def _integrate_watsonx(self):
        """Integra con watsonx.ai para reporte final."""
        if not self.bob_analysis_path:
            messagebox.showwarning("Advertencia", "Carga primero el análisis de Bob IDE")
            return
        if not self.metrics_path:
            messagebox.showwarning("Advertencia", "Ejecuta primero los benchmarks")
            return
        
        self._log("🔗 Integrando con watsonx.ai...")
        try:
            # Leer análisis de Bob
            with open(self.bob_analysis_path, 'r', encoding='utf-8') as f:
                bob_analysis = f.read()
            
            # Leer métricas locales
            with open(self.metrics_path, 'r', encoding='utf-8') as f:
                metrics = json.load(f)
            
            # Enviar a watsonx.ai
            resultado = summarize_metrics(bob_analysis, self.codigo, metrics)
            
            # Guardar reporte final
            reporte_path = ROOT / "output" / "REPORTE_FINAL_QA.md"
            reporte_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(reporte_path, 'w', encoding='utf-8') as f:
                f.write(resultado)
            
            self._log(f"✅ Reporte final guardado: {reporte_path}")
            messagebox.showinfo("Éxito", f"Reporte generado:\n{reporte_path}")
        
        except Exception as e:
            self._log(f"❌ Error en integración: {e}")
            messagebox.showerror("Error", str(e))
    
    def _view_report(self):
        """Abre el reporte final."""
        reporte_path = ROOT / "output" / "REPORTE_FINAL_QA.md"
        if reporte_path.exists():
            import webbrowser
            webbrowser.open(f"file://{reporte_path}")
        else:
            messagebox.showwarning("Advertencia", "Reporte no encontrado. Ejecuta primero la integración.")
    
    def _open_bob_ide(self):
        """Abre VS Code con Bob IDE para análisis manual."""
        self._log("🎯 Abriendo Bob IDE en VS Code...")
        try:
            subprocess.Popen(["code", str(ROOT)])
            self._log("✅ VS Code abierto. Usa Bob IDE manualmente para analizar.")
        except Exception as e:
            self._log(f"⚠️ No se pudo abrir VS Code automáticamente: {e}")
            messagebox.showwarning("Info", "Abre VS Code manualmente y usa Bob IDE")


if __name__ == "__main__":
    root = tk.Tk()
    gui = PasoUnoGUI(root)
    root.mainloop()
