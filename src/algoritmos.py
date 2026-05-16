"""Colección de algoritmos de ejemplo para auditar."""
from collections import deque

def dfs(graph, start):
    """Recorre el grafo en profundidad y devuelve el orden de visita."""
    visited = set()
    order = []

    def _dfs(u):
        visited.add(u)
        order.append(u)
        for v in graph.get(u, []):
            if v not in visited:
                _dfs(v)

    _dfs(start)
    return order

def iddfs(graph, start, max_depth):
    """Iterative deepening depth-first search (retorna primer recorrido alcanzable)."""
    def dls(node, depth, visited, order):
        if depth == 0:
            visited.add(node)
            order.append(node)
            return True
        for v in graph.get(node, []):
            if v not in visited:
                if dls(v, depth-1, visited, order):
                    return True
        return False

    order = []
    for depth in range(max_depth + 1):
        visited = set()
        if dls(start, depth, visited, order):
            return order
    return order
