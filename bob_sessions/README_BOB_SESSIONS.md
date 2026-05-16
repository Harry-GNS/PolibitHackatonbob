# 📁 bob_sessions/ — Análisis Teórico de Bob IDE

## 📝 Propósito
Esta carpeta contiene **todos los análisis de complejidad** generados manualmente en **IBM Bob IDE**.

## 📋 Contenido Esperado

### Archivos .md (Análisis de Código)
```
bob_analisis_dfs.md
bob_analisis_bubble_sort.md
bob_analisis_busqueda_lineal.md
```

Cada archivo contiene:
- Análisis Big-O (complejidad asintótica)
- Cuellos de botella identificados
- Recomendaciones de optimización
- Consumo de Bobcoins utilizado

### Archivos .png (Capturas de Pantalla)
```
bob_sesion_dfs_consumo.png
bob_sesion_bubble_sort_tokens.png
```

Captura de:
- Panel de análisis en Bob IDE
- Consumo de Bobcoins
- Exportación de la sesión

## 🔄 Workflow

1. **En Bob IDE (VS Code Plugin):**
   - Abre tu archivo de código
   - Usa el chat de Bob para solicitar análisis Big-O
   - Copia el resultado en Markdown
   - Exporta la sesión

2. **En tu repositorio:**
   - Guarda el .md con nombre descriptivo: `bob_analisis_[algoritmo].md`
   - Guarda la captura de pantalla con nombre: `bob_sesion_[algoritmo]_consumo.png`
   - Confirma el commit en git

## ⚠️ Importante

- **NO simules estos archivos.** Deben ser generados manualmente en Bob IDE.
- **Estos archivos son evidencia oficial** para el jurado del hackathon.
- Guarda un archivo .md por cada algoritmo importante que analices.
- El máximo de análisis recomendado es 3-4 para no gastar todos los 40 Bobcoins.

## 📊 Ejemplo de Contenido .md

```markdown
# Análisis de Complejidad: DFS (Depth-First Search)

## Función Analizada
```python
def dfs(graph, start):
    visited = set()
    stack = [start]
    ...
```

## Complejidad Teórica
- **Tiempo:** O(V + E)
- **Espacio:** O(V)

## Cuellos de Botella
1. Línea 5: búsqueda lineal en lista (O(N))
2. Línea 8: operación en diccionario anidado

## Recomendaciones
- Usar deque en lugar de lista para stack
- Precalcular índices

---
*Generado por IBM Bob IDE - [timestamp]*
```

## 🎯 Próximos Pasos

1. Abre VS Code con Bob IDE
2. Carga tu algoritmo
3. Solicita análisis Big-O
4. Exporta resultado como `bob_analisis_[nombre].md`
5. Toma captura: `bob_sesion_[nombre]_consumo.png`
6. Commit a git
