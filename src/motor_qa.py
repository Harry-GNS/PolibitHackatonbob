"""Motor local de QA que mide tiempo de ejecución y uso de memoria para funciones."""
import json
import time
import tracemalloc
import sys
from pathlib import Path
from statistics import mean

# Configuración automática de rutas para evitar el ModuleNotFoundError
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.append(str(RAIZ_PROYECTO))

DATA_DIR = RAIZ_PROYECTO / 'data'
OUT_FILE = DATA_DIR / 'metricas_salida.json'

# =========================================================================
# 1. ALGORITMOS PURIFICADOS (Lógica pura independiente)
# =========================================================================
def dfs_puro(graph, start, objective):
    """Recorre el grafo en profundidad iterativo sin bloqueos visuales."""
    pila = [(start, [start])]
    while pila:
        (nodo, camino) = pila.pop()
        if nodo == objective:
            return camino
        for vecino in reversed(graph.get(nodo, [])):
            if vecino not in camino:
                pila.append((vecino, camino + [vecino]))
    return None

# =========================================================================
# 2. SISTEMA DE MEDICIÓN DE RENDIMIENTO (BENCHMARK)
# =========================================================================
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
        times.append((t1 - t0) * 1000) # Conversión a milisegundos
        peaks.append(peak)
    return {
        'time_ms_mean': round(mean(times), 4),
        'time_ms_samples': [round(t, 4) for t in times],
        'mem_bytes_peak_mean': int(mean(peaks)),
        'mem_bytes_peak_samples': peaks
    }

# =========================================================================
# 3. EJECUCIÓN PRINCIPAL DEL STRESS TEST
# =========================================================================
def run_benchmarks():
    graph_file = DATA_DIR / 'grafos_prueba.json'
    
    if not graph_file.exists():
        print(f'❌ Error: No se encontró el archivo de datos en: {graph_file}')
        print('Asegúrate de haber creado el archivo data/grafos_prueba.json primero.')
        return
        
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph = json.load(f)

    print("🚀 Iniciando Motor de Pruebas de Estrés en Local...")
    
    sizes = [10, 100, 1000, 5000]
    results = {}
    
    nodo_inicial = list(graph.keys())[0]
    nodo_final = list(graph.keys())[-1]

    for N in sizes:
        print(f"-> Evaluando carga simulada para tamaño N = {N}...")
        
        # Ejecutamos el algoritmo dfs_puro simulando múltiples llamadas según la carga N
        res = measure_func(lambda: [dfs_puro(graph, nodo_inicial, nodo_final) for _ in range(max(1, N // 10))])
        results[N] = res

    # Asegurar que la carpeta 'data' exista
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Guardar métricas en el JSON final
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'benchmarks': results}, f, indent=2)
        
    print(f'\n✅ ¡Proceso terminado con éxito!')
    print(f'Resultados guardados en: {OUT_FILE}')

if __name__ == '__main__':
    run_benchmarks()