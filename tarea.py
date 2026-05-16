import networkx as nx
import matplotlib.pyplot as plt

# 1. Definición del grafo (Diapositiva 7)
grafo_d7 = {
    'A': ['B', 'C', 'D'], 'B': ['E', 'F'], 'C': ['G', 'H', 'I'], 'D': ['J'],
    'E': ['K', 'L'], 'F': ['M'], 'G': [], 'H': ['N', 'O'], 'I': [], 'J': ['P', 'Q'],
    'K': [], 'L': [], 'M': [], 'N': [], 'O': ['R', 'S', 'T'], 'P': [], 'Q': ['U'],
    'R': [], 'S': ['V'], 'T': [], 'U': [], 'V': []
}

# 2. Función matemática para ordenar el árbol jerárquicamente
def layout_jerarquico(grafo, raiz, x_centro=0, y_inicio=0, ancho_total=20):
    posiciones = {}
    
    def asignar_coordenadas(nodo, x, y, ancho_disponible):
        posiciones[nodo] = (x, y)
        hijos = grafo.get(nodo, [])
        if not hijos:
            return
        
        espacio_por_hijo = ancho_disponible / len(hijos)
        x_actual = x - (ancho_disponible / 2) + (espacio_por_hijo / 2)
        
        for hijo in hijos:
            asignar_coordenadas(hijo, x_actual, y - 1, espacio_por_hijo)
            x_actual += espacio_por_hijo
            
    asignar_coordenadas(raiz, x_centro, y_inicio, ancho_total)
    return posiciones

# 3. Función para dibujar y guardar el grafo
def dibujar_grafo(grafo, camino, algoritmo, iteracion):
    G = nx.DiGraph(grafo)
    pos = layout_jerarquico(grafo, 'A') 
    
    plt.figure(figsize=(10, 8))
    plt.title(f"{algoritmo} - Paso {iteracion}\nCamino Actual: {' -> '.join(camino)}", fontsize=14)
    
    # Nodos base
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='lightgray', 
            node_size=700, font_weight='bold', font_size=10, arrows=False)
    
    # Nodos visitados
    nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='lightgreen', node_size=700)
    
    # Aristas recorridas
    if len(camino) > 1:
        aristas_camino = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, edge_color='red', width=3, arrows=True)
    
    plt.savefig(f"{algoritmo}_paso_{iteracion}.png")
    plt.close()

# 4. Algoritmo DFS
def dfs(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]
    paso = 1
    
    print(f"\n=== Iniciando DFS buscando '{objetivo}' ===")
    while pila:
        nodos_pila = [n for n, c in pila]
        print(f"Pila actual: {list(reversed(nodos_pila))}") 
        
        (nodo, camino) = pila.pop()
        print(f"-> Visitando: {nodo} | Camino: {camino}\n")
        
        dibujar_grafo(grafo, camino, "DFS", paso)
        paso += 1
        
        if nodo == objetivo:
            return camino
            
        for vecino in reversed(grafo.get(nodo, [])):
            if vecino not in camino:
                pila.append((vecino, camino + [vecino]))
    return None

# 5. Algoritmo LDFS
def ldfs(grafo, inicio, objetivo, limite):
    pila = [(inicio, [inicio], 0)]
    paso = 1
    
    while pila:
        nodos_pila = [n for n, c, p in pila]
        print(f"Pila actual: {list(reversed(nodos_pila))}")
        
        (nodo, camino, prof) = pila.pop()
        print(f"-> Visitando: {nodo} (Prof {prof}) | Camino: {camino}\n")
        
        dibujar_grafo(grafo, camino, f"LDFS_lim{limite}", paso)
        paso += 1
        
        if nodo == objetivo:
            return camino
            
        if prof < limite:
            for vecino in reversed(grafo.get(nodo, [])):
                if vecino not in camino:
                    pila.append((vecino, camino + [vecino], prof + 1))
    return None

# 6. Algoritmo IDFS
def idfs(grafo, inicio, objetivo, limite_maximo):
    print(f"\n=== Iniciando IDFS buscando '{objetivo}' ===")
    for limite in range(limite_maximo + 1):
        print(f"\n*** Iteración IDFS con Límite = {limite} ***")
        resultado = ldfs(grafo, inicio, objetivo, limite)
        if resultado:
            print(f"\n¡Objetivo '{objetivo}' encontrado en límite {limite}!")
            return resultado
    return None

# ==========================================
# BLOQUE DE EJECUCIÓN (PRUEBAS)
# ==========================================
if __name__ == "__main__":
    # Prueba de DFS buscando 'M'
    dfs(grafo_d7, 'A', 'M')
    
    # Prueba de IDFS buscando 'M' (con límite 3 es suficiente)
    idfs(grafo_d7, 'A', 'M', limite_maximo=3)




    