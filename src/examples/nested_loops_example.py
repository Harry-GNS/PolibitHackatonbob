"""Ejemplo de bucles anidados para demostrar complejidad O(N^3) si se desea."""
import time


def cubic_work(n):
    s = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                s += (i * j * k) % 7
    return s


def measure(n):
    t0 = time.perf_counter()
    cubic_work(n)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000


if __name__ == "__main__":
    for n in [10, 20]:
        print(f"N={n} -> {measure(n):.2f} ms")
