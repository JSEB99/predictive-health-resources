# 🧠 API de Predicción de Pacientes

## 🎯 Objetivo
Esta API permite **predecir la cantidad esperada de pacientes** en un hospital o institución médica, según su ubicación, características internas y fecha específica.  
Está diseñada para integrarse con **aplicaciones web o dashboards** (como la app de Streamlit) y así **apoyar la planificación hospitalaria y la asignación de recursos**.

---

## ⚙️ Funcionamiento general

1. **Recepción de datos**  
   La API recibe una solicitud con información detallada sobre el establecimiento de salud, que incluye:
   - Personal médico y hospitalario (médicos, enfermeras, cirujanos, etc.).  
   - Recursos disponibles (camas, laboratorios, pasantes).  
   - Variables estadísticas (`lag_1`, `delta_1`, `rolling_mean_3`).  
   - Datos temporales (año, mes, día, trimestre, día de la semana).  
   - Ubicación del hospital (entidad, municipio, localidad, código postal).

   Todos estos valores se definen en el modelo `PatientPredictionRequest` usando **Pydantic**, lo que asegura validación y formato correcto antes del procesamiento.

---

2. **Estructura técnica**
   - La API se desarrolla con **FastAPI**, un framework de alto rendimiento para servicios REST en Python.  
   - Define un endpoint principal:  
     ```
     GET /v1/predict/
     ```
     bajo la etiqueta `predictions`.

---

3. **Proceso interno de predicción**
   Cuando llega una petición:
   - Los datos del hospital se convierten en un `DataFrame` de **pandas**.  
   - Se carga un modelo previamente entrenado (guardado en `model.pkl`) mediante **joblib**.  
   - El modelo realiza la **predicción del número de pacientes esperados** para ese conjunto de características.  
   - El resultado se devuelve en formato JSON:
     ```json
     { "No. of Patients": 154.2 }
     ```

---

4. **Descripción del modelo**
   Según la documentación (`description`):
   - El modelo usa **series temporales** entrenadas con datos históricos de salud.  
   - Toma en cuenta la fecha, ubicación y variables operativas del hospital.  
   - Sirve para **optimizar la planificación de personal, camas y recursos médicos**.

---

## 🔗 Integración con la aplicación Streamlit
La app de Streamlit envía los datos ingresados por el usuario a este endpoint (`/v1/predict/`) y muestra en pantalla el valor que la API devuelve, cerrando el ciclo de **predicción en tiempo real**.

---

## 🧩 Beneficios principales
- **Rápida y ligera:** construida con FastAPI, responde en milisegundos.  
- **Validada:** garantiza que los datos de entrada sean del tipo correcto.  
- **Escalable:** puede integrarse con múltiples aplicaciones, dashboards o servicios hospitalarios.  
- **Modular:** el modelo de predicción (`model.pkl`) puede actualizarse sin modificar la API.  

---

# 🩺 Predictor de cantidad de pacientes

## 🎯 Objetivo
Esta aplicación web permite **predecir cuántos pacientes atenderá un establecimiento de salud** en una fecha determinada.  
Su propósito es ayudar a hospitales y clínicas a **anticipar la demanda de atención médica**, optimizar sus recursos y mejorar la planificación operativa.

---

## ⚙️ Cómo funciona

1. **Ingreso de datos**  
   El usuario selecciona:
   - La **fecha** para la que desea hacer la predicción.  
   - El **lugar** (entidad, municipio, localidad, código postal).  
   - Datos del establecimiento, como:
     - Cantidad promedio de médicos generales y especialistas.  
     - Número de enfermeras, cirujanos, pediatras, anestesiólogos, odontólogos y pasantes.  
     - Disponibilidad de camas, laboratorios y personal hospitalario.  
     - Variables históricas como `lag`, `delta` y `media móvil`.

2. **Procesamiento**  
   Al presionar **“Predecir”**, la aplicación envía toda esta información a un **modelo de regresión alojado en una API**.  
   Este modelo analiza los datos y estima la cantidad probable de pacientes para la fecha y lugar seleccionados.

3. **Resultado**  
   La aplicación muestra el **número estimado de pacientes** que se espera atender, permitiendo anticipar:
   - Sobrecarga o baja de demanda.  
   - Necesidades de personal médico.  
   - Capacidad hospitalaria requerida (camas, recursos, equipos).  

---

## 🧠 Beneficios
- **Planificación preventiva:** permite asignar mejor el personal y los recursos antes de los picos de atención.  
- **Optimización de operaciones:** ayuda a reducir tiempos de espera y mejorar la atención al paciente.  
- **Apoyo a decisiones estratégicas:** facilita un manejo más inteligente de los recursos hospitalarios.  
