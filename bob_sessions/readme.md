# OptiCode QA — Auditor Autónomo de Rendimiento y Coste Computacional

## 🎯 1. ¿Qué es nuestro proyecto?
OptiCode QA es una herramienta de aseguramiento de calidad (QA) enfocada en optimizar el coste computacional y la eficiencia algorítmica del software antes de que vaya a producción. 

En lugar de hacer lo mismo que el 90% de la competencia (quienes solo explican código o automatizan manuales de usuario genéricos), nosotros atacamos un dolor real en la industria: **el gasto excesivo de servidores en la nube debido a código matemáticamente ineficiente.**

---

## 🛠️ 2. Arquitectura y Herramientas del Proyecto
Para que la solución sea viable y no nos gastemos los recursos antes de tiempo, el proyecto se divide en tres capas claras utilizando las siguientes herramientas:

### A. Capa de Análisis Teórico (IBM Bob) — **EL NÚCLEO OBLIGATORIO**
* **Herramienta:** **IBM Bob IDE** (en modo `Advanced` o `Code`).
* **Qué hace:** Actúa como nuestro Ingeniero de Rendimiento Senior. Bob analiza funciones específicas en Python y determina de forma matemática su **notación de complejidad (Big-O)** (ej. detecta si el código es un ineficiente $O(N^2)$ en lugar de un óptimo $O(N \log N)$). Además, usamos la función nativa **Bob tips** para rastrear en tiempo real las partes más complejas del código.
* **Estrategia de Bobcoins:** **¡Ojo! Solo tenemos 40 Bobcoins por cuenta.** No le pasen repositorios enteros a Bob. Invoquen a la IA únicamente de forma quirúrgica sobre los archivos o funciones de algoritmos complejos que queremos auditar.

### B. Capa de Motor de QA (Despliegue Local)
* **Herramienta:** **Nuestro propio entorno local** (Python / Scripts locales).
* **Qué hace:** Como la guía aclara que las cuentas de la nube no permiten desplegar la solución final, ejecutamos este motor localmente en nuestras máquinas. El script toma el algoritmo analizado y le inyecta vectores de datos simulados a escala exponencial ($N = 10, 100, 1000, 5000$). Mide y registra el **tiempo de ejecución real en milisegundos** y el **pico de memoria RAM**.

### C. Capa de Inteligencia y Reporte Extendido (watsonx.ai) — **OPCIONAL RECOMENDADO**
* **Herramienta:** **IBM watsonx.ai** (usando la API/SDK en Python conectada a la región de **Dallas**).
* **Qué hace:** Enviamos las métricas recolectadas localmente a un modelo fundacional pequeño de **IBM Granite** mediante código. El modelo procesa la discrepancia entre la teoría matemática de Bob y la práctica de nuestro script local para redactar las conclusiones del reporte final de QA.
* **Estrategia de Créditos:** Usamos modelos micro/pequeños porque consumen poquísimos tokens (medidos en Resource Units) y rinden más para estructurar texto plano, protegiendo los **\$80 USD de presupuesto**.

watsonx-Hackathon WS (watsonx.ai Studio)
watsonx-Hackathon WML (Watson Machine Learning)

---

## 📋 3. ¿Qué tiene que hacer cada miembro del equipo? (Flujo de Trabajo)

1. **Aislar e Identificar:** Escoger del repositorio un conjunto de algoritmos complejos de procesamiento o búsquedas (ej. del material de laboratorios) para usarlos como conejillos de indias.
2. **Auditar con Bob:** Abrir esos archivos en **Bob IDE**, pedirle el análisis Big-O y capturar las optimizaciones lógicas sugeridas.
3. **Correr Pruebas de Carga:** Pasar esas funciones por nuestro script local de medición para obtener las curvas de tiempo reales y picos de RAM.
4. **Exportar Evidencias para el Jurado (¡VITAL!):**
   * Antes de hacer nada, **limpien todas las credenciales y API Keys del código** para evitar que Seguridad de IBM nos suspenda la cuenta.
   * Creen una carpeta en la raíz llamada **`bob_sessions`**.
   * En el chat de Bob IDE, vayan a *History*, abran las tareas del proyecto, desplieguen el cuadro de consumo del encabezado y tomen una **captura de pantalla**.
   * En esa misma vista, hagan clic en **Export task history** para guardar las conversaciones con la IA en formato Markdown (`.md`).
   * Suban todas las capturas y archivos `.md` dentro de la carpeta `bob_sessions`. **Si no está esa carpeta, el jurado nos descalifica.**

---

## 📦 4. Entregables Finales de la Sumisión
Para cumplir con las reglas estrictas de Lablab.ai, debemos tener listos:
1. **Descripción del Producto:** (Este mismo enfoque de OptiCode QA).
2. **Repositorio de GitHub:** Estrictamente **PÚBLICO** (si es privado, restan puntos), incluyendo el código del motor local y la carpeta obligatoria `bob_sessions`.
3. **Video de Presentación / Demo:** Con una duración máxima e improrrogable de **5 minutos**.

## Usar

