"""Motor local de QA que mide tiempo de ejecución y uso de memoria para funciones."""
import json
import time
import tracemalloc
from pathlib import Path
from statistics import mean

from src.algoritmos import dfs

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
OUT_FILE = DATA_DIR / 'metricas_salida.json'

def measure_func(func, *args, repeats=3):
    times = []
    peaks = []
    for _ in range(repeats):
        tracemalloc.start()
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append((t1 - t0) * 1000)
        peaks.append(peak)
    return {'time_ms_mean': mean(times), 'time_ms_samples': times, 'mem_bytes_peak_mean': int(mean(peaks)), 'mem_bytes_peak_samples': peaks}

def run_benchmarks():
    # Ejemplo usando el DFS en data/grafos_prueba.json
    import json
    graph_file = DATA_DIR / 'grafos_prueba.json'
    if not graph_file.exists():
        print('No se encontró', graph_file)
        return
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)

    sizes = [10, 100, 1000, 5000]
    results = {}
    for N in sizes:
        # Para este ejemplo, simplemente repetimos el DFS N veces para simular carga
        res = measure_func(lambda: [dfs(graph, list(graph.keys())[0]) for _ in range(max(1, N//10))])
        results[N] = res

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'benchmarks': results}, f, indent=2)
    print('Resultados guardados en', OUT_FILE)

if __name__ == '__main__':
    run_benchmarks()
