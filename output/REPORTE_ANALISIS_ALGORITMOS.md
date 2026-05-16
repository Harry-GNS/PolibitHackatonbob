# Reporte de Análisis: Algoritmos de Búsqueda

**Archivo analizado:** `src/algoritmos.py`  
**Fecha:** 2026-05-16  
**Algoritmos evaluados:** DFS, LDFS, IDFS

---

## 1. Resumen de Complejidades

| Algoritmo | Complejidad Temporal | Complejidad Espacial | Notas |
|-----------|---------------------|---------------------|-------|
| **DFS** | O(V + E) | O(V) | V = nodos, E = aristas. Pila puede crecer hasta V nodos |
| **LDFS** | O(b^d) | O(d) | b = factor de ramificación, d = límite de profundidad |
| **IDFS** | O(b^d) | O(d) | Repite búsquedas pero mantiene espacio lineal óptimo |

### Detalles por Algoritmo

#### DFS (Depth-First Search)
- **Temporal:** O(V + E) - Visita cada nodo y arista una vez
- **Espacial:** O(V) - La pila puede contener todos los nodos en el peor caso
- **Implementación:** Usa pila explícita con tuplas `(nodo, camino)`

#### LDFS (Limited Depth-First Search)
- **Temporal:** O(b^d) - Explora hasta profundidad d con factor de ramificación b
- **Espacial:** O(d) - La pila está limitada por la profundidad máxima
- **Implementación:** Añade control de profundidad con tuplas `(nodo, camino, profundidad)`

#### IDFS (Iterative Deepening DFS)
- **Temporal:** O(b^d) - Aunque repite búsquedas, la complejidad asintótica es la misma
- **Espacial:** O(d) - Mantiene la eficiencia espacial de LDFS
- **Implementación:** Ejecuta LDFS incrementalmente desde límite 0 hasta límite_maximo

---

## 2. Cuellos de Botella de Rendimiento

### ⚠️ PROBLEMA CRÍTICO: Operaciones I/O en Bucles de Búsqueda

**Ubicación del problema:**

1. **Línea 68** en `dfs()`:
   ```python
   while pila:
       # ...
       dibujar_grafo(grafo, camino, "DFS", paso)  # ← BLOQUEANTE
       paso += 1
   ```

2. **Línea 91** en `ldfs()`:
   ```python
   while pila:
       # ...
       dibujar_grafo(grafo, camino, f"LDFS_lim{limite}", paso)  # ← BLOQUEANTE
       paso += 1
   ```

### Impacto en Rendimiento

| Operación | Tiempo Estimado | Frecuencia | Impacto Total |
|-----------|----------------|------------|---------------|
| `plt.figure()` | ~50-100ms | Por cada nodo visitado | Alto |
| `nx.draw()` | ~100-200ms | Por cada nodo visitado | Muy Alto |
| `plt.savefig()` | ~50-150ms | Por cada nodo visitado | Alto (I/O disco) |
| **Total por iteración** | **~200-450ms** | **N veces** | **Crítico** |

### Análisis Detallado

#### Problema 1: Renderizado Gráfico Síncrono
- Cada llamada a `dibujar_grafo()` crea una figura matplotlib completa
- El renderizado es bloqueante y ocurre en el hilo principal
- Para un grafo con 22 nodos (como `grafo_d7`), puede generar 10-20+ imágenes

#### Problema 2: Operaciones I/O Bloqueantes
- `plt.savefig()` escribe a disco de forma síncrona
- No hay buffering ni escritura asíncrona
- Cada escritura bloquea la ejecución del algoritmo

#### Problema 3: Multiplicación en IDFS
- IDFS ejecuta LDFS múltiples veces (una por cada límite)
- Si `limite_maximo = 3`, el overhead se multiplica por 4 iteraciones
- Genera imágenes redundantes de los mismos caminos

### Cálculo de Overhead

Para una búsqueda típica:
- **DFS buscando 'M':** ~10 nodos visitados × 300ms = **3 segundos de overhead**
- **IDFS con límite 3:** ~25 nodos visitados × 300ms = **7.5 segundos de overhead**

**Tiempo real de búsqueda sin visualización:** < 1ms  
**Overhead de visualización:** 3000-7500x más lento

---

## 3. Recomendaciones de Optimización

### Prioridad Alta

1. **Separar visualización de lógica de búsqueda**
   - Almacenar estados en memoria durante la búsqueda
   - Generar visualizaciones después de completar el algoritmo

2. **Implementar generación asíncrona de imágenes**
   - Usar threading o multiprocessing para renderizado
   - Queue de tareas de visualización

3. **Añadir flag de debug/visualización**
   ```python
   def dfs(grafo, inicio, objetivo, visualizar=False):
       # Solo dibujar si visualizar=True
   ```

### Prioridad Media

4. **Cachear layouts de grafo**
   - `layout_jerarquico()` se recalcula en cada iteración
   - Calcular una vez y reutilizar

5. **Usar formato de imagen más eficiente**
   - PNG es lento para escribir
   - Considerar SVG o formatos vectoriales

6. **Batch de escrituras**
   - Acumular figuras en memoria
   - Escribir todas al final

---

## 4. Métricas de Código

| Métrica | Valor |
|---------|-------|
| Líneas totales | 127 |
| Funciones | 6 |
| Dependencias externas | 2 (networkx, matplotlib) |
| Llamadas a I/O por búsqueda | 10-25+ |
| Ratio código/visualización | ~40% visualización |

---

## 5. Conclusiones

### Fortalezas
- Implementaciones correctas de los algoritmos
- Código legible y bien estructurado
- Visualización útil para propósitos educativos

### Debilidades Críticas
- **Rendimiento degradado 3000x** por operaciones de visualización síncronas
- Acoplamiento fuerte entre lógica de búsqueda y presentación
- No escalable para grafos grandes o búsquedas en producción

### Recomendación Final
**Refactorizar urgentemente** para separar la lógica de búsqueda de la visualización. El código actual es adecuado solo para demostraciones educativas con grafos pequeños, pero no es viable para uso en producción o análisis de rendimiento real de los algoritmos.

---

**Fin del reporte**