"""Interfaz visual para el Paso 1 de OptiCode QA.

La app permite cargar el código fuente, el reporte teórico de Bob IDE y las
métricas del motor local, para mostrarlos en un panel visual más útil que un
README y exportar un informe HTML presentable.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "src" / "algoritmos.py"
DEFAULT_BOB = ROOT / "bob_sessions" / "readme.md"
DEFAULT_METRICS = ROOT / "data" / "metricas_salida.json"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class MetricsRow:
    size: str
    time_ms: float
    memory_kb: float


class StepOneStudio(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("OptiCode QA | Step 1 Studio")
        self.geometry("1450x900")
        self.minsize(1320, 820)
        self.configure(bg="#0a1020")

        self.source_path = tk.StringVar(value=str(DEFAULT_SOURCE))
        self.bob_path = tk.StringVar(value=str(DEFAULT_BOB))
        self.metrics_path = tk.StringVar(value=str(DEFAULT_METRICS))
        self.status_text = tk.StringVar(value="Listo para cargar teoría, práctica y generar la vista final.")
        self.divergence_text = tk.StringVar(value="N/D")
        self.complexity_text = tk.StringVar(value="N/D")
        self.risk_text = tk.StringVar(value="N/D")

        self.source_code = ""
        self.bob_report = ""
        self.metrics_data = {}
        self.metrics_rows: list[MetricsRow] = []

        self._configure_style()
        self._build_shell()
        self._load_defaults()
        self._refresh_dashboard()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _configure_style(self) -> None:
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.colors = {
            "bg": "#0a1020",
            "panel": "#111a2f",
            "panel_alt": "#0e1628",
            "panel_soft": "#16213b",
            "text": "#eef4ff",
            "muted": "#8ea0c3",
            "accent": "#7c5cff",
            "accent_2": "#2fd5c8",
            "accent_3": "#ffb86b",
            "danger": "#ff6b6b",
            "good": "#47d18c",
            "line": "#24324d",
        }

        self.configure(bg=self.colors["bg"])
        self.style.configure(
            "Root.TFrame",
            background=self.colors["bg"],
        )
        self.style.configure(
            "Panel.TFrame",
            background=self.colors["panel"],
        )
        self.style.configure(
            "Soft.TFrame",
            background=self.colors["panel_soft"],
        )
        self.style.configure(
            "Sidebar.TFrame",
            background="#0c1326",
        )
        self.style.configure(
            "TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Title.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI Semibold", 18),
        )
        self.style.configure(
            "Section.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI Semibold", 12),
        )
        self.style.configure(
            "Muted.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Accent.TButton",
            background=self.colors["accent"],
            foreground="white",
            borderwidth=0,
            padding=(14, 10),
            font=("Segoe UI Semibold", 10),
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", "#8d72ff")],
            foreground=[("active", "white")],
        )
        self.style.configure(
            "Ghost.TButton",
            background=self.colors["panel_soft"],
            foreground=self.colors["text"],
            borderwidth=0,
            padding=(12, 9),
            font=("Segoe UI", 10),
        )
        self.style.map(
            "Ghost.TButton",
            background=[("active", self.colors["line"])],
        )
        self.style.configure(
            "Header.TEntry",
            fieldbackground=self.colors["panel_alt"],
            foreground=self.colors["text"],
            insertcolor=self.colors["text"],
            bordercolor=self.colors["line"],
            lightcolor=self.colors["line"],
            darkcolor=self.colors["line"],
            padding=8,
        )
        self.style.configure(
            "Treeview",
            background=self.colors["panel_alt"],
            fieldbackground=self.colors["panel_alt"],
            foreground=self.colors["text"],
            rowheight=28,
            bordercolor=self.colors["line"],
            borderwidth=0,
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Treeview.Heading",
            background=self.colors["panel_soft"],
            foreground=self.colors["text"],
            relief="flat",
            font=("Segoe UI Semibold", 9),
        )
        self.style.map("Treeview", background=[("selected", self.colors["accent"])])

    def _build_shell(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", padding=(22, 20))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.configure(width=295)

        self.main = ttk.Frame(self, style="Root.TFrame", padding=(20, 18))
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=1)

        self._build_sidebar()
        self._build_header()
        self._build_content()

    def _build_sidebar(self) -> None:
        brand = tk.Frame(self.sidebar, bg="#0c1326")
        brand.pack(fill="x", pady=(0, 18))

        title = tk.Label(
            brand,
            text="OptiCode QA",
            bg="#0c1326",
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 22),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            brand,
            text="Step 1 Studio · Bob + Motor Local",
            bg="#0c1326",
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        tagline = tk.Label(
            self.sidebar,
            text="Una vista tipo dossier para comparar teoría, práctica y riesgo real.",
            wraplength=240,
            justify="left",
            bg="#0c1326",
            fg="#b8c4df",
            font=("Segoe UI", 10),
        )
        tagline.pack(fill="x", pady=(0, 18))

        actions = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        actions.pack(fill="x", pady=(0, 20))

        ttk.Button(actions, text="Abrir código fuente", style="Accent.TButton", command=self.load_source_dialog).pack(fill="x", pady=6)
        ttk.Button(actions, text="Abrir reporte Bob", style="Ghost.TButton", command=self.load_bob_dialog).pack(fill="x", pady=6)
        ttk.Button(actions, text="Abrir métricas", style="Ghost.TButton", command=self.load_metrics_dialog).pack(fill="x", pady=6)
        ttk.Button(actions, text="Exportar panel HTML", style="Accent.TButton", command=self.export_html).pack(fill="x", pady=(14, 6))
        ttk.Button(actions, text="Cargar demo", style="Ghost.TButton", command=self._load_defaults).pack(fill="x", pady=6)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=18)

        quick = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        quick.pack(fill="x")

        ttk.Label(quick, text="Rutas activas", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        self.path_labels = {}
        for key, label in (("source", self.source_path), ("bob", self.bob_path), ("metrics", self.metrics_path)):
            box = tk.Frame(quick, bg="#10192d", highlightthickness=1, highlightbackground=self.colors["line"])
            box.pack(fill="x", pady=5)
            tk.Label(
                box,
                textvariable=label,
                wraplength=235,
                justify="left",
                bg="#10192d",
                fg=self.colors["text"],
                font=("Consolas", 8),
                padx=10,
                pady=8,
            ).pack(fill="x")
            self.path_labels[key] = box

    def _build_header(self) -> None:
        header = ttk.Frame(self.main, style="Root.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.columnconfigure(0, weight=1)

        banner = tk.Canvas(header, height=148, highlightthickness=0, bg=self.colors["bg"])
        banner.grid(row=0, column=0, sticky="ew")
        self._paint_banner(banner)

        overlay = tk.Frame(banner, bg="")
        overlay.place(relx=0.03, rely=0.18, relwidth=0.7, relheight=0.72)

        tk.Label(
            overlay,
            text="Paso 1 · Dossier visual de auditoría",
            bg=self.colors["bg"],
            fg=self.colors["accent_2"],
            font=("Segoe UI Semibold", 11),
        ).pack(anchor="w")
        tk.Label(
            overlay,
            text="Bob IDE genera la teoría. El motor local genera la práctica.\nEsta interfaz convierte ambos en una vista ejecutiva más clara.",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Segoe UI Semibold", 19),
            justify="left",
        ).pack(anchor="w", pady=(8, 8))
        tk.Label(
            overlay,
            text="Carga el código, el reporte de Bob y las métricas. El panel calcula divergencia, riesgo y genera un HTML de entrega.",
            bg=self.colors["bg"],
            fg="#d4def4",
            font=("Segoe UI", 10),
            justify="left",
        ).pack(anchor="w")

        status = tk.Frame(banner, bg=self.colors["panel_soft"], highlightthickness=1, highlightbackground=self.colors["line"])
        status.place(relx=0.74, rely=0.16, relwidth=0.23, relheight=0.68)
        tk.Label(
            status,
            text="Estado del panel",
            bg=self.colors["panel_soft"],
            fg=self.colors["muted"],
            font=("Segoe UI Semibold", 9),
        ).pack(anchor="w", padx=14, pady=(12, 6))
        tk.Label(
            status,
            textvariable=self.status_text,
            bg=self.colors["panel_soft"],
            fg=self.colors["text"],
            wraplength=250,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=14, pady=(0, 10))
        ttk.Separator(status, orient="horizontal").pack(fill="x", padx=14, pady=10)
        self._mini_metric(status, "Divergencia", self.divergence_text, self.colors["accent_2"])
        self._mini_metric(status, "Complejidad", self.complexity_text, self.colors["accent"])
        self._mini_metric(status, "Riesgo", self.risk_text, self.colors["accent_3"])

    def _build_content(self) -> None:
        content = ttk.Frame(self.main, style="Root.TFrame")
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        left = ttk.Frame(content, style="Root.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        right = ttk.Frame(content, style="Root.TFrame")
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        self._build_code_panel(left)
        self._build_bob_panel(left)
        self._build_metrics_panel(right)
        self._build_insights_panel(right)

    def _build_code_panel(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        frame.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        top = ttk.Frame(frame, style="Panel.TFrame")
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="Código fuente conejillo de indias", style="Section.TLabel").pack(side="left")
        ttk.Button(top, text="Recargar", style="Ghost.TButton", command=self._load_source_default).pack(side="right")

        controls = ttk.Frame(frame, style="Panel.TFrame")
        controls.grid(row=1, column=0, sticky="ew", pady=(10, 8))
        controls.columnconfigure(0, weight=1)
        ttk.Label(controls, text="Archivo activo", style="Muted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.source_path, style="Header.TEntry").grid(row=1, column=0, sticky="ew", pady=(4, 0))

        code_box = tk.Frame(frame, bg=self.colors["panel_alt"], highlightthickness=1, highlightbackground=self.colors["line"])
        code_box.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        code_box.rowconfigure(0, weight=1)
        code_box.columnconfigure(0, weight=1)
        self.code_text = tk.Text(
            code_box,
            bg=self.colors["panel_alt"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            wrap="none",
            font=("Consolas", 10),
            padx=14,
            pady=14,
        )
        self.code_text.grid(row=0, column=0, sticky="nsew")
        self._add_scrollbars(code_box, self.code_text)

    def _build_bob_panel(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        frame.grid(row=1, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        top = ttk.Frame(frame, style="Panel.TFrame")
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="Reporte de Bob IDE", style="Section.TLabel").pack(side="left")
        ttk.Button(top, text="Recargar", style="Ghost.TButton", command=self._load_bob_default).pack(side="right")

        subtitle = ttk.Label(frame, text="Resumen teórico exportado en Markdown o texto plano.", style="Muted.TLabel")
        subtitle.grid(row=1, column=0, sticky="w", pady=(8, 8))

        bob_box = tk.Frame(frame, bg=self.colors["panel_alt"], highlightthickness=1, highlightbackground=self.colors["line"])
        bob_box.grid(row=2, column=0, sticky="nsew")
        bob_box.rowconfigure(0, weight=1)
        bob_box.columnconfigure(0, weight=1)
        self.bob_text = tk.Text(
            bob_box,
            bg=self.colors["panel_alt"],
            fg="#dfe9ff",
            insertbackground=self.colors["text"],
            relief="flat",
            wrap="word",
            font=("Segoe UI", 10),
            padx=14,
            pady=14,
        )
        self.bob_text.grid(row=0, column=0, sticky="nsew")
        self._add_scrollbars(bob_box, self.bob_text)

    def _build_metrics_panel(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        frame.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

        top = ttk.Frame(frame, style="Panel.TFrame")
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="Métricas de práctica", style="Section.TLabel").pack(side="left")
        ttk.Button(top, text="Recargar", style="Ghost.TButton", command=self._load_metrics_default).pack(side="right")

        subtitle = ttk.Label(frame, text="Resultados del motor local con tiempos y memoria estimados.", style="Muted.TLabel")
        subtitle.grid(row=1, column=0, sticky="w", pady=(8, 8))

        table_wrap = tk.Frame(frame, bg=self.colors["panel_alt"], highlightthickness=1, highlightbackground=self.colors["line"])
        table_wrap.grid(row=2, column=0, sticky="nsew")
        table_wrap.columnconfigure(0, weight=1)
        table_wrap.rowconfigure(0, weight=1)

        columns = ("size", "time", "memory")
        self.metrics_tree = ttk.Treeview(table_wrap, columns=columns, show="headings", height=10)
        self.metrics_tree.heading("size", text="N")
        self.metrics_tree.heading("time", text="Tiempo ms")
        self.metrics_tree.heading("memory", text="Memoria KB")
        self.metrics_tree.column("size", width=120, anchor="center")
        self.metrics_tree.column("time", width=140, anchor="center")
        self.metrics_tree.column("memory", width=140, anchor="center")
        self.metrics_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=self.metrics_tree.yview)
        self.metrics_tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.grid(row=0, column=1, sticky="ns")

    def _build_insights_panel(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        frame.grid(row=1, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

        top = ttk.Frame(frame, style="Panel.TFrame")
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="Lectura ejecutiva", style="Section.TLabel").pack(side="left")
        ttk.Button(top, text="Generar HTML", style="Accent.TButton", command=self.export_html).pack(side="right")

        subtitle = ttk.Label(frame, text="Hallazgos automáticos para comparar teoría y práctica.", style="Muted.TLabel")
        subtitle.grid(row=1, column=0, sticky="w", pady=(8, 8))

        insight_box = tk.Frame(frame, bg=self.colors["panel_alt"], highlightthickness=1, highlightbackground=self.colors["line"])
        insight_box.grid(row=2, column=0, sticky="nsew")
        insight_box.columnconfigure(0, weight=1)
        insight_box.rowconfigure(0, weight=1)
        self.insights_text = tk.Text(
            insight_box,
            bg=self.colors["panel_alt"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            wrap="word",
            font=("Segoe UI", 10),
            padx=14,
            pady=14,
        )
        self.insights_text.grid(row=0, column=0, sticky="nsew")
        self._add_scrollbars(insight_box, self.insights_text)

    def _mini_metric(self, parent: tk.Widget, label: str, variable: tk.StringVar, color: str) -> None:
        wrapper = tk.Frame(parent, bg=self.colors["panel_soft"])
        wrapper.pack(fill="x", padx=14, pady=5)
        dot = tk.Frame(wrapper, bg=color, width=8, height=8)
        dot.pack(side="left", padx=(0, 10), pady=5)
        dot.pack_propagate(False)
        text = tk.Frame(wrapper, bg=self.colors["panel_soft"])
        text.pack(side="left", fill="x", expand=True)
        tk.Label(text, text=label, bg=self.colors["panel_soft"], fg=self.colors["muted"], font=("Segoe UI", 8)).pack(anchor="w")
        tk.Label(text, textvariable=variable, bg=self.colors["panel_soft"], fg=self.colors["text"], font=("Segoe UI Semibold", 10)).pack(anchor="w")

    def _add_scrollbars(self, parent: tk.Widget, text_widget: tk.Text) -> None:
        y_scroll = ttk.Scrollbar(parent, orient="vertical", command=text_widget.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll = ttk.Scrollbar(parent, orient="horizontal", command=text_widget.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        text_widget.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    def _paint_banner(self, canvas: tk.Canvas) -> None:
        width = 1600
        height = 148
        left = (124, 92, 255)
        right = (20, 193, 170)
        for x in range(width):
            ratio = x / max(1, width - 1)
            r = int(left[0] * (1 - ratio) + right[0] * ratio)
            g = int(left[1] * (1 - ratio) + right[1] * ratio)
            b = int(left[2] * (1 - ratio) + right[2] * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(x, 0, x, height, fill=color)
        canvas.create_oval(1040, -40, 1360, 280, fill="#ffffff", outline="")
        canvas.create_oval(1150, 20, 1440, 300, fill="#2b1fff", outline="", stipple="gray25")
        canvas.create_oval(1240, 20, 1570, 310, fill="#14c1aa", outline="", stipple="gray25")

    # ------------------------------------------------------------------
    # Data handling
    # ------------------------------------------------------------------
    def _load_defaults(self) -> None:
        self._load_source_default()
        self._load_bob_default()
        self._load_metrics_default()
        self.status_text.set("Demo cargada con la base local del proyecto.")
        self._refresh_dashboard()

    def _load_source_default(self) -> None:
        if DEFAULT_SOURCE.exists():
            self._load_source_file(DEFAULT_SOURCE)

    def _load_bob_default(self) -> None:
        if DEFAULT_BOB.exists():
            self._load_bob_file(DEFAULT_BOB)

    def _load_metrics_default(self) -> None:
        if DEFAULT_METRICS.exists():
            self._load_metrics_file(DEFAULT_METRICS)

    def load_source_dialog(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de código fuente",
            filetypes=[("Python", "*.py"), ("Todos", "*.*")],
        )
        if path:
            self._load_source_file(Path(path))

    def load_bob_dialog(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar reporte de Bob IDE",
            filetypes=[("Markdown", "*.md"), ("Texto", "*.txt"), ("Todos", "*.*")],
        )
        if path:
            self._load_bob_file(Path(path))

    def load_metrics_dialog(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar métricas del motor local",
            filetypes=[("JSON", "*.json"), ("CSV", "*.csv"), ("Todos", "*.*")],
        )
        if path:
            self._load_metrics_file(Path(path))

    def _load_source_file(self, path: Path) -> None:
        try:
            self.source_code = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self.source_code = path.read_text(encoding="latin-1")
        self.source_path.set(str(path))
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, self.source_code)
        self.status_text.set(f"Código cargado desde {path.name}.")
        self._refresh_dashboard()

    def _load_bob_file(self, path: Path) -> None:
        try:
            self.bob_report = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self.bob_report = path.read_text(encoding="latin-1")
        self.bob_path.set(str(path))
        self.bob_text.delete("1.0", tk.END)
        self.bob_text.insert(tk.END, self.bob_report)
        self.status_text.set(f"Reporte de Bob cargado desde {path.name}.")
        self._refresh_dashboard()

    def _load_metrics_file(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        self.metrics_path.set(str(path))
        if path.suffix.lower() == ".csv":
            self.metrics_data = {"csv": text}
            self.metrics_rows = self._parse_csv_metrics(text)
        else:
            try:
                self.metrics_data = json.loads(text)
            except json.JSONDecodeError as exc:
                messagebox.showerror("Error", f"No se pudo leer el JSON: {exc}")
                return
            self.metrics_rows = self._parse_json_metrics(self.metrics_data)
        self._render_metrics_table()
        self.status_text.set(f"Métricas cargadas desde {path.name}.")
        self._refresh_dashboard()

    def _parse_json_metrics(self, payload: dict) -> list[MetricsRow]:
        rows: list[MetricsRow] = []
        benchmarks = payload.get("benchmarks", payload)
        if isinstance(benchmarks, dict):
            for key, value in benchmarks.items():
                if not isinstance(value, dict):
                    continue
                time_ms = value.get("time_ms_mean") or value.get("time_ms") or value.get("tiempo_ms") or 0
                memory_raw = value.get("mem_bytes_peak_mean") or value.get("ram_kb") or value.get("memory_kb") or 0
                memory_kb = memory_raw / 1024 if memory_raw and memory_raw > 2048 else memory_raw
                rows.append(MetricsRow(size=str(key), time_ms=float(time_ms), memory_kb=float(memory_kb)))
        return rows

    def _parse_csv_metrics(self, text: str) -> list[MetricsRow]:
        rows: list[MetricsRow] = []
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return rows
        header = [item.strip().lower() for item in lines[0].split(",")]
        index_map = {name: idx for idx, name in enumerate(header)}
        for line in lines[1:]:
            cols = [item.strip() for item in line.split(",")]
            size = cols[index_map.get("n", 0)] if len(cols) > index_map.get("n", 0) else "?"
            time_ms = float(cols[index_map.get("time_ms", 1)]) if len(cols) > index_map.get("time_ms", 1) else 0
            memory_kb = float(cols[index_map.get("ram_kb", 2)]) if len(cols) > index_map.get("ram_kb", 2) else 0
            rows.append(MetricsRow(size=size, time_ms=time_ms, memory_kb=memory_kb))
        return rows

    def _render_metrics_table(self) -> None:
        for item in self.metrics_tree.get_children():
            self.metrics_tree.delete(item)
        for row in self.metrics_rows:
            self.metrics_tree.insert("", tk.END, values=(row.size, f"{row.time_ms:.2f}", f"{row.memory_kb:.2f}"))

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------
    def _refresh_dashboard(self) -> None:
        code_stats = self._analyze_code(self.source_code)
        bob_stats = self._analyze_bob(self.bob_report)
        metric_stats = self._analyze_metrics(self.metrics_rows)

        divergence = self._compute_divergence(metric_stats)
        self.divergence_text.set(f"{divergence:.0f}/100")
        self.complexity_text.set(code_stats["complexity_label"])
        self.risk_text.set(metric_stats["risk_label"])

        insights = self._build_insights(code_stats, bob_stats, metric_stats, divergence)
        self.insights_text.delete("1.0", tk.END)
        self.insights_text.insert(tk.END, insights)

    def _analyze_code(self, code: str) -> dict:
        lines = code.splitlines()
        line_count = len(lines)
        def_count = len(re.findall(r"^\s*def\s+", code, flags=re.M))
        loop_count = len(re.findall(r"^\s*(for|while)\s+", code, flags=re.M))
        branch_count = len(re.findall(r"^\s*(if|elif|else)\b", code, flags=re.M))
        nesting_score = loop_count * 2 + branch_count + max(0, def_count - 1)

        if nesting_score >= 8:
            label = "Alta fricción algorítmica"
        elif nesting_score >= 4:
            label = "Complejidad moderada"
        elif nesting_score >= 1:
            label = "Complejidad controlada"
        else:
            label = "Flujo plano"

        return {
            "line_count": line_count,
            "def_count": def_count,
            "loop_count": loop_count,
            "branch_count": branch_count,
            "nesting_score": nesting_score,
            "complexity_label": label,
        }

    def _analyze_bob(self, report: str) -> dict:
        lines = [line.strip() for line in report.splitlines() if line.strip()]
        headings = sum(1 for line in lines if line.startswith("#"))
        bullets = sum(1 for line in lines if line.startswith("-") or line.startswith("*"))
        mentions = [token for token in ("O(N)", "O(N^2)", "O(N^3)", "Big-O", "complejidad") if token.lower() in report.lower()]
        return {
            "headings": headings,
            "bullets": bullets,
            "mentions": mentions,
            "size": len(report),
        }

    def _analyze_metrics(self, rows: list[MetricsRow]) -> dict:
        if not rows:
            return {
                "count": 0,
                "avg_time": 0.0,
                "avg_memory": 0.0,
                "time_growth": 0.0,
                "memory_growth": 0.0,
                "risk_label": "Sin datos",
            }

        avg_time = sum(r.time_ms for r in rows) / len(rows)
        avg_memory = sum(r.memory_kb for r in rows) / len(rows)
        first = rows[0]
        last = rows[-1]
        time_growth = (last.time_ms - first.time_ms) / max(first.time_ms, 1)
        memory_growth = (last.memory_kb - first.memory_kb) / max(first.memory_kb, 1)

        score = time_growth + memory_growth / 2
        if score >= 5:
            risk = "Riesgo alto"
        elif score >= 2:
            risk = "Riesgo medio"
        else:
            risk = "Riesgo bajo"

        return {
            "count": len(rows),
            "avg_time": avg_time,
            "avg_memory": avg_memory,
            "time_growth": time_growth,
            "memory_growth": memory_growth,
            "risk_label": risk,
        }

    def _compute_divergence(self, metric_stats: dict) -> float:
        if metric_stats["count"] == 0:
            return 0.0
        score = abs(metric_stats["time_growth"] * 20) + abs(metric_stats["memory_growth"] * 12)
        return max(0.0, min(100.0, score))

    def _build_insights(self, code_stats: dict, bob_stats: dict, metric_stats: dict, divergence: float) -> str:
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        bob_hint = ", ".join(bob_stats["mentions"]) if bob_stats["mentions"] else "sin menciones explícitas de Big-O"
        divergence_msg = self._divergence_message(divergence)

        lines = [
            f"Diagnóstico generado: {now}",
            "",
            "Resumen rápido",
            f"- Código: {code_stats['line_count']} líneas, {code_stats['def_count']} funciones, {code_stats['loop_count']} bucles.",
            f"- Bob: {bob_stats['headings']} títulos, {bob_stats['bullets']} bullets, referencias detectadas: {bob_hint}.",
            f"- Métricas: {metric_stats['count']} muestras, tiempo promedio {metric_stats['avg_time']:.2f} ms, memoria promedio {metric_stats['avg_memory']:.2f} KB.",
            "",
            f"Lectura ejecutiva: {divergence_msg}",
            f"Nivel de complejidad visual: {code_stats['complexity_label']}.",
            f"Riesgo actual: {metric_stats['risk_label']}.",
            "",
            "Siguiente paso recomendado",
            "- Exportar esta vista como HTML para el expediente del equipo.",
            "- Compartir el análisis de Bob y las métricas del motor local con el agente watsonx.ai.",
            "- Usar esta UI como evidencia visual en vez de depender solo de archivos Markdown.",
        ]
        return "\n".join(lines)

    def _divergence_message(self, divergence: float) -> str:
        if divergence >= 65:
            return "Hay una discrepancia fuerte entre la teoría y la práctica; conviene revisar cuellos de botella ocultos o sobrecarga del entorno."
        if divergence >= 35:
            return "La teoría y la práctica se parecen, pero todavía hay diferencia suficiente para justificar refactorización o micro-optimización."
        return "La práctica acompaña bastante bien la teoría; el caso parece estable para presentar al jurado."

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------
    def export_html(self) -> None:
        code_stats = self._analyze_code(self.source_code)
        bob_stats = self._analyze_bob(self.bob_report)
        metric_stats = self._analyze_metrics(self.metrics_rows)
        divergence = self._compute_divergence(metric_stats)
        divergence_msg = self._divergence_message(divergence)
        insights = self._build_insights(code_stats, bob_stats, metric_stats, divergence)

        html_path = OUTPUT_DIR / "step1_dashboard.html"
        json_path = OUTPUT_DIR / "step1_dashboard_summary.json"

        rows_html = "\n".join(
            f"<tr><td>{row.size}</td><td>{row.time_ms:.2f}</td><td>{row.memory_kb:.2f}</td></tr>"
            for row in self.metrics_rows
        ) or "<tr><td colspan='3'>Sin métricas cargadas</td></tr>"

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OptiCode QA · Step 1 Studio</title>
  <style>
    :root {{
      --bg: #0a1020;
      --panel: #111a2f;
      --soft: #16213b;
      --text: #eef4ff;
      --muted: #8ea0c3;
      --accent: #7c5cff;
      --accent2: #2fd5c8;
      --accent3: #ffb86b;
      --danger: #ff6b6b;
      --line: #24324d;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Segoe UI, system-ui, sans-serif; background: radial-gradient(circle at top left, #16213b 0%, #0a1020 45%, #050912 100%); color: var(--text); }}
    .wrap {{ max-width: 1400px; margin: 0 auto; padding: 28px; }}
    .hero {{ border: 1px solid var(--line); border-radius: 24px; overflow: hidden; background: linear-gradient(135deg, rgba(124,92,255,.94), rgba(47,213,200,.88)); box-shadow: 0 28px 70px rgba(0,0,0,.35); }}
    .hero-inner {{ display: grid; grid-template-columns: 1.7fr .9fr; gap: 24px; padding: 28px; align-items: stretch; }}
    .card, .panel {{ border: 1px solid var(--line); border-radius: 22px; background: rgba(17,26,47,.92); box-shadow: 0 18px 50px rgba(0,0,0,.22); }}
    .card {{ padding: 20px; }}
    h1 {{ margin: 0 0 10px; font-size: 42px; line-height: 1.02; }}
    h2 {{ margin: 0 0 16px; font-size: 20px; }}
    p {{ color: var(--muted); line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: 18px; margin-top: 18px; }}
    .span-8 {{ grid-column: span 8; }}
    .span-4 {{ grid-column: span 4; }}
    .span-6 {{ grid-column: span 6; }}
    .span-12 {{ grid-column: span 12; }}
    .metric {{ padding: 18px; border-radius: 18px; background: rgba(22,33,59,.82); border: 1px solid var(--line); }}
    .metric label {{ display:block; color: var(--muted); font-size: 12px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: .08em; }}
    .metric strong {{ font-size: 28px; }}
    table {{ width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 18px; }}
    th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid var(--line); }}
    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: #0c1326; padding: 16px; border-radius: 18px; border: 1px solid var(--line); color: #dfe9ff; }}
    .tag {{ display:inline-flex; padding: 8px 12px; border-radius: 999px; background: rgba(124,92,255,.18); border: 1px solid rgba(124,92,255,.4); margin-right: 8px; margin-bottom: 8px; }}
    @media (max-width: 1040px) {{ .hero-inner, .grid {{ grid-template-columns: 1fr; }} .span-8, .span-4, .span-6, .span-12 {{ grid-column: span 1; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="hero-inner">
        <div>
          <h1>OptiCode QA<br/>Step 1 Studio</h1>
          <p>Teoría, práctica y lectura ejecutiva en una sola vista. Exportado desde la interfaz visual local para reemplazar el flujo de archivos sueltos.</p>
          <div>
            <span class="tag">Divergencia: {divergence:.0f}/100</span>
            <span class="tag">Complejidad: {code_stats['complexity_label']}</span>
            <span class="tag">Riesgo: {metric_stats['risk_label']}</span>
          </div>
        </div>
        <div class="card">
          <h2>Lectura ejecutiva</h2>
          <p>{divergence_msg}</p>
          <p><strong>Bob:</strong> {bob_stats['headings']} títulos, {bob_stats['bullets']} bullets, {bob_hint}.</p>
          <p><strong>Motor local:</strong> {metric_stats['count']} muestras, media {metric_stats['avg_time']:.2f} ms.</p>
        </div>
      </div>
    </section>

    <section class="grid">
      <div class="panel span-4 card">
        <h2>Métricas clave</h2>
        <div class="metric"><label>Líneas de código</label><strong>{code_stats['line_count']}</strong></div>
        <div style="height:12px"></div>
        <div class="metric"><label>Bucles detectados</label><strong>{code_stats['loop_count']}</strong></div>
        <div style="height:12px"></div>
        <div class="metric"><label>Promedio RAM KB</label><strong>{metric_stats['avg_memory']:.2f}</strong></div>
      </div>
      <div class="panel span-8 card">
        <h2>Métricas del motor local</h2>
        <table>
          <thead><tr><th>N</th><th>Tiempo ms</th><th>Memoria KB</th></tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
      </div>
      <div class="panel span-6 card">
        <h2>Resumen Bob IDE</h2>
        <pre>{self.bob_report or 'No se cargó ningún reporte de Bob.'}</pre>
      </div>
      <div class="panel span-6 card">
        <h2>Insights automáticos</h2>
        <pre>{insights}</pre>
      </div>
    </section>
  </div>
</body>
</html>"""

        summary = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_path": str(self.source_path.get()),
            "bob_path": str(self.bob_path.get()),
            "metrics_path": str(self.metrics_path.get()),
            "code_stats": code_stats,
            "bob_stats": bob_stats,
            "metric_stats": metric_stats,
            "divergence": divergence,
            "insights": insights,
        }

        html_path.write_text(html, encoding="utf-8")
        json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        self.status_text.set(f"Panel exportado a {html_path.name} y {json_path.name}.")
        messagebox.showinfo("Exportación lista", f"Se generó:\n{html_path}\n{json_path}")


def main() -> None:
    app = StepOneStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
