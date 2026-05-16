"""Colección completa de algoritmos de búsqueda en grafos.

Lógica de Alex integrada en la GUI de Harry.
Incluye: DFS, LDFS (Depth-Limited), IDFS (Iterative Deepening).
"""

# =========================================================================
# ALGORITMOS PURIFICADOS — Lógica pura sin bloqueos visuales ni prints
# Compatibles con el motor de benchmarks y la GUI de Harry
# =========================================================================

def dfs(graph, start, objective=None):
    """Recorre el grafo en profundidad (DFS iterativo).

    - Sin objective: devuelve el orden de visita completo (compatibilidad Harry).
    - Con objective: devuelve el camino hasta el nodo objetivo o None.
    """
    if objective is None:
        # Modo recorrido completo — compatibilidad con motor_qa de Harry
        visited = set()
        order = []

        def _dfs_rec(u):
            visited.add(u)
            order.append(u)
            for v in graph.get(u, []):
                if v not in visited:
                    _dfs_rec(v)

        _dfs_rec(start)
        return order
    else:
        # Modo búsqueda con objetivo — lógica completa de Alex
        pila = [(start, [start])]
        while pila:
            (nodo, camino) = pila.pop()
            if nodo == objective:
                return camino
            for vecino in reversed(graph.get(nodo, [])):
                if vecino not in camino:
                    pila.append((vecino, camino + [vecino]))
        return None


def dfs_puro(graph, start, objective=None):
    """Alias de dfs() — nombre usado internamente por el motor QA de Alex."""
    return dfs(graph, start, objective)


def ldfs(graph, start, objective, limit):
    """DFS con límite de profundidad (Depth-Limited DFS).

    Retorna el camino hasta objective o None si no se alcanza dentro del límite.
    """
    pila = [(start, [start], 0)]
    while pila:
        (nodo, camino, prof) = pila.pop()
        if nodo == objective:
            return camino
        if prof < limit:
            for vecino in reversed(graph.get(nodo, [])):
                if vecino not in camino:
                    pila.append((vecino, camino + [vecino], prof + 1))
    return None


def idfs(graph, start, objective, max_limit):
    """Iterative Deepening DFS — llama a ldfs con límite creciente 0..max_limit.

    Retorna el camino en cuanto lo encuentra, o None si no existe.
    """
    for limit in range(max_limit + 1):
        resultado = ldfs(graph, start, objective, limit)
        if resultado is not None:
            return resultado
    return None


def iddfs(graph, start, max_depth):
    """Variante de IDFS para recorrido completo sin objetivo explícito.
    Compatibilidad con el algoritmos.py original de Harry.
    """
    def dls(node, depth, visited, order):
        if depth == 0:
            visited.add(node)
            order.append(node)
            return True
        for v in graph.get(node, []):
            if v not in visited:
                if dls(v, depth - 1, visited, order):
                    return True
        return False

    order = []
    for depth in range(max_depth + 1):
        visited = set()
        if dls(start, depth, visited, order):
            return order
    return order
