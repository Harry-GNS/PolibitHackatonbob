"""Motor local de QA — lógica de Alex integrada con la GUI de Harry.

Mide tiempo de ejecución y uso de memoria para DFS, LDFS e IDFS.
Genera data/metricas_salida.json compatible con el dashboard de Harry.
"""
import json
import time
import tracemalloc
import sys
from pathlib import Path
from statistics import mean

# Configuración automática de rutas (patrón de Alex)
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.algoritmos import dfs_puro, ldfs, idfs

DATA_DIR = RAIZ_PROYECTO / 'data'
OUT_FILE = DATA_DIR / 'metricas_salida.json'


# =========================================================================
# SISTEMA DE MEDICIÓN DE RENDIMIENTO (BENCHMARK) — de Alex
# =========================================================================
def measure_func(func, *args, repeats=3):
    """Mide tiempo (ms) y memoria (bytes) de una función en N repeticiones."""
    times = []
    peaks = []
    for _ in range(repeats):
        tracemalloc.start()
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append((t1 - t0) * 1000)  # ms
        peaks.append(peak)
    return {
        'time_ms_mean': round(mean(times), 4),
        'time_ms_samples': [round(t, 4) for t in times],
        'mem_bytes_peak_mean': int(mean(peaks)),
        'mem_bytes_peak_samples': peaks
    }


# =========================================================================
# EJECUCIÓN PRINCIPAL DEL STRESS TEST — estructura de Alex, datos de Harry
# =========================================================================
def run_benchmarks():
    """Ejecuta benchmarks para DFS, LDFS e IDFS y guarda métricas en JSON."""
    graph_file = DATA_DIR / 'grafos_prueba.json'

    if not graph_file.exists():
        print(f'Error: No se encontro el archivo de datos en: {graph_file}')
        return

    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)

    print("Iniciando Motor de Pruebas de Estres...")

    nodo_inicial = list(graph.keys())[0]
    nodo_final = list(graph.keys())[-1]

    sizes = [10, 100, 1000, 5000]
    results = {}

    for N in sizes:
        print(f"   -> Evaluando carga simulada N = {N}...")
        repeticiones = max(1, N // 10)

        # DFS puro
        res_dfs = measure_func(
            lambda: [dfs_puro(graph, nodo_inicial, nodo_final) for _ in range(repeticiones)]
        )

        # LDFS con límite razonable (profundidad del grafo ~6)
        res_ldfs = measure_func(
            lambda: [ldfs(graph, nodo_inicial, nodo_final, 6) for _ in range(repeticiones)]
        )

        # IDFS con límite máximo razonable
        res_idfs = measure_func(
            lambda: [idfs(graph, nodo_inicial, nodo_final, 6) for _ in range(repeticiones)]
        )

        results[N] = {
            'dfs':  res_dfs,
            'ldfs': res_ldfs,
            'idfs': res_idfs,
            # Compatibilidad con el parser del servidor de Harry:
            # usa los valores de DFS como métricas "generales"
            'time_ms_mean':         res_dfs['time_ms_mean'],
            'time_ms_samples':      res_dfs['time_ms_samples'],
            'mem_bytes_peak_mean':  res_dfs['mem_bytes_peak_mean'],
            'mem_bytes_peak_samples': res_dfs['mem_bytes_peak_samples'],
        }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'benchmarks': results}, f, indent=2)

    print(f'\nProceso terminado! Resultados guardados en: {OUT_FILE}')


if __name__ == '__main__':
    run_benchmarks()
