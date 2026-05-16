"""Ejemplo de algoritmo ineficiente O(N^2) para pruebas."""
import random
import time
from statistics import mean


def bubble_sort(arr):
    n = len(arr)
    a = arr.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def generate_random_list(n):
    return [random.randint(0, 1000000) for _ in range(n)]


def measure_sizes(sizes=(10, 100, 500, 1000)):
    results = {}
    for n in sizes:
        times = []
        for _ in range(3):
            arr = generate_random_list(n)
            t0 = time.perf_counter()
            bubble_sort(arr)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000)
        results[n] = {"time_ms_mean": mean(times), "time_ms_samples": times}
    return results


if __name__ == "__main__":
    print("Midiendo bubble_sort...")
    res = measure_sizes()
    for k, v in res.items():
        print(f"N={k}: {v['time_ms_mean']:.2f} ms (samples: {v['time_ms_samples']})")
