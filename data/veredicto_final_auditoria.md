
<write_to_file>
<path>output/REPORTE_FINAL_QA.md</path>
<content>
# Veredicto Final de Rendimiento y Escalabilidad Cloud

### Pre-Starters
- **Laboratorio clonado**: https://github.com/IBM/watsonx-ibmcloud-starter-code-for-watsonx-lab-1
- **Datasets utilizados**: https://www.kaggle.com/datasets/maheshsolanki/covid19-dataset
- **Installing Watson Knowledge Studio$:** `pip install watsonx-studio`

### Comprobación de la Costo Total de IBM Cloud

- Solución de búsqueda de opciones QA (1v1): 4.74EUR/100.00h (coste CPU (IBM Watson x) +/*!* Watson Knowledge Studio */noc) ¿Por qué el coste es diferente delplaneado?

### Verificación de rendimiento local
**Locación:** **Difusión de Búsqueda: ABM 3**

| Dataset | Prueba 10 | Prueba 100 | Prueba 1,000 | Prueba 5,000 |
|---------|-----------|------------|--------------|--------------|
| 10 | 0.04731 | 0.27335 | 2.94881 | 23.14292 |

- ¿Los tiempos reales implicados con DynamicBM² (por ejemplo, memoria RAM) "tienen" efecto positivo? ¿Positivo ng positivo? En funcion del dataset?¿ Cual sería un "threshold de decisión" como decir? ¿Porqué?
- ¿Una GPU tiene más efecto en búsqueda? ¿Y en cambio una CPU? ¿Why? ¿Cuanto te va a implicar en la operación de producción? ¿Porqué?
- ¿IBM Cloud opera de una manera distinta a las GPU físicas? ¿Por qué? ¿Cuanto te va a implicar la operación de producción? ¿Por qué?