# Análisis de Complejidad: DFS (Depth-First Search)

## Función Analizada
```python
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

## Complejidad Teórica

### Big-O Analysis
- **Tiempo:** O(V + E) - V = vértices, E = aristas
- **Espacio:** O(V) - Stack de recursión + conjunto visitados

### Desglose

#### Operaciones
- **Visita cada vértice:** V iteraciones
- **Explora cada arista:** E iteraciones (cada arista se toca 1 vez)
- **Búsquedas en conjunto:** O(1) promedio en hash set

**Total:** O(V + E)

#### Ejemplos Concretos
- Grafo con V=100 nodos, E=150 aristas → 250 operaciones
- Grafo con V=1,000 nodos, E=1,500 aristas → 2,500 operaciones
- Grafo densamente conectado V=1,000, E=500,000 → 501,000 operaciones

## Análisis Detallado

### Stack de Recursión
```
Profundidad máxima = altura del árbol
En el peor caso (grafo en cadena): profundidad = V

Consumo de memoria: ~V elementos en stack
```

### Casos de Uso
| Tipo de Grafo | Tiempo | Espacio | Comportamiento |
|---------------|--------|---------|----------------|
| Árbol (E=V-1) | O(V) | O(V) | Óptimo |
| Denso (E≈V²) | O(V²) | O(V) | Lento en grafos densos |
| Sparse (E≈V) | O(V) | O(V) | Eficiente |

## Cuellos de Botella

1. **Recursión Profunda:** Si el grafo es muy profundo, puede causar stack overflow
2. **Grafos Densos:** Con muchas aristas, el tiempo crece hacia O(V²)
3. **Overhead de Set:** Búsquedas en conjunto pueden ser lentas si no es hash set

## Optimizaciones Posibles

1. **DFS Iterativo:** Evita stack overflow
   ```python
   def dfs_iterative(graph, start):
       stack = [start]
       visited = set()
       while stack:
           node = stack.pop()
           if node not in visited:
               visited.add(node)
               stack.extend(graph[node])
       return visited
   ```

2. **BFS en lugar de DFS:** Mejor para grafos amplios

3. **Bit Array en lugar de Set:** Si nodos son numerados 0-N

## Impacto en Rendimiento

| Métrica | Riesgo | Notas |
|---------|--------|-------|
| Tiempo | ✅ BAJO | O(V+E) es óptimo para traverse |
| Memoria | ⚠️ MEDIO | Stack puede ser problema en grafos profundos |
| Escalabilidad | ✅ BUENO | Escala linealmente con tamaño del grafo |
| Densidad | ⚠️ CRÍTICO | Mucho peor con grafos densos |

## Recomendaciones para QA

✅ **Usar DFS cuando:**
- Necesitas recorrer/explorar todo el grafo
- El grafo es sparse (pocas aristas)
- La profundidad es manejable

❌ **Evitar DFS cuando:**
- Grafo es muy profundo (usa iterativo)
- Grafo es extremadamente denso
- Necesitas la ruta más corta (usa BFS)

## Conclusión

DFS es **eficiente para traversal de grafos** con complejidad óptima O(V+E). El riesgo principal es:
- Stack overflow en grafos profundos → solución: usar versión iterativa
- Rendimiento pobre en grafos densos → aceptable según contexto

**Para producción:** Usar versión iterativa con manejo de excepciones.
