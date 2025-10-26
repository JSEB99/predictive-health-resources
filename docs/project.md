# Modelo Predictivo de Deterioro de Salud en Pacientes Hospitalizados

## Necesidad del cliente

Los hospitales y centros de salud deben anticipar la demanda de servicios para gestionar adecuadamente:
- Camas.
- Personal.
- Quirófanos.
- Inventarios.

La falta de previsión provoca saturación en emergencias o, al contrario, recursos ociosos y costes innecesarios.
Se requiere un modelo que analice tendencias y patrones para planificar turnos, compras y disponibilidad de recursos.

## Validación de mercado

Las soluciones de salud predictiva utilizan datos de:
- Historias clínicas electrónicas.
- *Wearables*.
- Factores externos.

Esto permite anticipar eventos y mejorar la eficiencia operativa.

Además, el 60 % de los hospitales estará utilizando alguna herramienta de análisis predictivo en 2025, lo que confirma el creciente interés por modelos que optimicen la planificación de recursos y logísticas.

## Expectativa

Diseñar un sistema de *machine learning* que pronostique la demanda de:
- Camas.
- Consultas.
- Procedimientos en distintos servicios (urgencias, cirugía, consultorios externos).

A partir de:
- Datos históricos.
- Calendarios de eventos.
- Variables climáticas.
- Tendencias epidemiológicas.

Las predicciones permitirán ajustar agendas, dimensionar personal y aprovisionar insumos.


## Entregables deseados

- Conjunto de *datasets* históricos consolidados (ocupación de camas, consultas, intervenciones, variables estacionales).
- Modelos de predicción de series temporales (p. ej., ARIMA, Prophet, LSTM) con métricas de rendimiento.
- API para consultar las proyecciones y dashboards visuales de demanda por servicio y fecha.
- Informe con recomendaciones de planificación basada en los resultados y documentación técnica.

## Funcionalidades

### Must-have
- Ingesta y limpieza de datos de admisiones, procedimientos y calendarios.
- Entrenamiento y validación de modelos de pronóstico con capacidad para actualizarse periódicamente.
- Visualización de predicciones en un dashboard interactivo, con filtros por área hospitalaria.
- Alertas automáticas a gestores cuando se detectan picos de demanda futuros.

### Nice-to-have
- Inclusión de variables externas (clima, eventos locales) para mejorar la precisión.
- Simulación de escenarios (p. ej., brotes epidémicos, feriados) para planificar recursos adicionales.
- Exportación de los datos y predicciones a formatos abiertos (CSV, Excel).
- Módulo de recomendaciones para redistribución de personal y horarios. 