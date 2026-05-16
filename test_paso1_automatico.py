"""Script de prueba rápida para el sistema PASO 1 automático.

Ejecuta el análisis completo sin necesidad de la interfaz web,
útil para testing y debugging.
"""

from pathlib import Path
import sys

# Añadir src al path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from paso1_automatico import ejecutar_paso1_desde_archivo

def main():
    """Ejecuta una prueba completa del PASO 1."""
    print("=" * 70)
    print("🧪 TEST: OptiCode QA - PASO 1 Automático")
    print("=" * 70)
    
    # Ruta del código a analizar
    root = Path(__file__).parent
    codigo_path = root / "src" / "algoritmos.py"
    
    if not codigo_path.exists():
        print(f"❌ Error: No se encontró {codigo_path}")
        print("   Asegúrate de que el archivo existe.")
        return
    
    print(f"\n📂 Analizando: {codigo_path}")
    print(f"📊 Grafo de prueba: data/grafos_prueba.json")
    print("\n" + "-" * 70)
    
    try:
        # Ejecutar PASO 1 completo
        resultado = ejecutar_paso1_desde_archivo(str(codigo_path))
        
        print("\n" + "=" * 70)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE RESULTADOS:")
        print("-" * 70)
        
        if resultado.get('analisis_teorico'):
            resumen = resultado['analisis_teorico']['resumen']
            print(f"\n🔍 Análisis Teórico:")
            print(f"   • Funciones analizadas: {resumen['total_funciones']}")
            print(f"   • Cuellos de botella: {resumen['total_cuellos_botella']}")
            print(f"   • Críticos (P0): {resumen['criticos']}")
            print(f"   • Altos (P1): {resumen['altos']}")
            print(f"   • Función más compleja: {resumen['funcion_mas_compleja']}")
            print(f"   • Complejidad máxima: {resumen['complejidad_maxima']}")
        
        if resultado.get('metricas_practicas'):
            metricas = resultado['metricas_practicas']
            print(f"\n⚡ Benchmarks Prácticos:")
            print(f"   • Tamaños probados: {len(metricas['benchmarks'])}")
            print(f"   • Función probada: {metricas.get('funcion_probada', 'N/A')}")
            
            # Mostrar tabla de benchmarks
            print("\n   Resultados:")
            print("   " + "-" * 50)
            print(f"   {'N':>6} | {'Tiempo (ms)':>12} | {'Memoria (KB)':>12}")
            print("   " + "-" * 50)
            
            for n in sorted([int(k) for k in metricas['benchmarks'].keys()]):
                bench = metricas['benchmarks'][str(n)]
                tiempo = bench['time_ms_mean']
                memoria = bench['mem_bytes_peak_mean'] / 1024
                print(f"   {n:>6} | {tiempo:>12.2f} | {memoria:>12.2f}")
            print("   " + "-" * 50)
        
        if resultado.get('comparacion'):
            comp = resultado['comparacion']
            print(f"\n🔬 Comparación Teoría vs Práctica:")
            print(f"   • Complejidad teórica: {comp['complejidad_teorica']}")
            print(f"   • Complejidad práctica: {comp['complejidad_practica']}")
            print(f"   • Divergencia: {comp['divergencia']:.1f}%")
            print(f"   • Crecimiento observado: {comp['crecimiento_observado']:.2f}x")
            print(f"   • Tiempo promedio: {comp['tiempo_promedio_ms']:.2f} ms")
            print(f"   • Memoria promedio: {comp['memoria_promedio_kb']:.2f} KB")
            
            # Interpretación de divergencia
            div = comp['divergencia']
            if div >= 65:
                print(f"\n   ⚠️  DIVERGENCIA ALTA - Refactorización urgente recomendada")
            elif div >= 35:
                print(f"\n   ⚡ DIVERGENCIA MODERADA - Optimización recomendada")
            else:
                print(f"\n   ✅ DIVERGENCIA BAJA - Código estable")
        
        if resultado.get('rutas_exportadas'):
            print(f"\n📄 Reportes Generados:")
            for nombre, ruta in resultado['rutas_exportadas'].items():
                print(f"   • {nombre}: {ruta}")
        
        print("\n" + "=" * 70)
        print("🎉 Todos los componentes funcionan correctamente")
        print("=" * 70)
        
        print("\n💡 Próximos pasos:")
        print("   1. Revisa los reportes generados en output/ y bob_sessions/")
        print("   2. Inicia el servidor web: python src/servidor_paso1.py")
        print("   3. Abre http://localhost:5000 en tu navegador")
        print("   4. Usa la interfaz gráfica para análisis interactivos")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR EN LA PRUEBA")
        print("=" * 70)
        print(f"\n{type(e).__name__}: {e}")
        
        import traceback
        print("\n📋 Traceback completo:")
        print("-" * 70)
        traceback.print_exc()
        print("-" * 70)
        
        print("\n💡 Posibles soluciones:")
        print("   • Verifica que todas las dependencias estén instaladas:")
        print("     pip install -r requirements.txt")
        print("   • Asegúrate de que el archivo algoritmos.py existe")
        print("   • Revisa que la estructura de directorios sea correcta")


if __name__ == "__main__":
    main()

# Made with Bob
