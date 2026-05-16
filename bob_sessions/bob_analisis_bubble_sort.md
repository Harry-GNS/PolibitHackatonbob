# Análisis de Complejidad: Bubble Sort

## Función Analizada
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

## Complejidad Teórica

### Big-O Analysis
- **Peor caso:** O(N²) - Array completamente invertido
- **Caso promedio:** O(N²) - Distribución aleatoria
- **Mejor caso:** O(N) - Array ya ordenado (con optimización de flag)

### Análisis Detallado

#### Operaciones Principales
- **Comparaciones:** máximo (N-1) + (N-2) + ... + 1 = N(N-1)/2 ≈ N²/2
- **Intercambios:** hasta N(N-1)/2 en el peor caso
- **Espacios adicionales:** O(1) - in-place sorting

#### Crecimiento Esperado
- Con N=100: ~5,000 comparaciones
- Con N=1,000: ~500,000 comparaciones  
- Con N=10,000: ~50,000,000 comparaciones

## Cuello de Botella Principal

Los **bucles anidados** son el problema:
```
for i in range(n):              # N iteraciones
    for j in range(0, n-i-1):   # N iteraciones en promedio
        if arr[j] > arr[j+1]:   # 1 comparación
            swap...             # 1-3 operaciones
```

**Impacto:** Cada incremento de N multiplica el tiempo por ~N, no por una constante.

## Posibles Optimizaciones

1. **Usar Merge Sort o Quick Sort:** O(N log N) - 100x más rápido para N=10,000
2. **Agregar flag de detección:** Si no hay intercambios, el array está ordenado
3. **Cocktail Sort:** Mejora mínima, sigue siendo O(N²)
4. **Paralelización:** Difícil para Bubble Sort, mejor con otros algoritmos

## Recomendaciones para QA

| Métrica | Riesgo | Acción |
|---------|--------|--------|
| Tiempo  | ⚠️ ALTO | Evitar en arrays > 1,000 elementos |
| Memoria | ✅ BAJO | O(1) - No hay problema de RAM |
| CPU     | ⚠️ ALTO | Puede saturar CPU en datos grandes |
| Escalabilidad | 🔴 CRÍTICO | No escala. Reemplazar por Merge/Quick Sort |

## Conclusión

Bubble Sort es **educativo pero ineficiente en producción**. En sistemas reales:
- Para N < 50: Aceptable
- Para N = 100-1000: Considerar alternativas
- Para N > 1000: Reemplazar inmediatamente

**Recomendación:** Usar `sorted()` de Python o `Collections.sort()` de Java.
