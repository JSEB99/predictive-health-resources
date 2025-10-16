# Sprint Planning Week 3

## 📘 **Diccionario de Datos**

### 🧩 `dim_patient_history`

| Campo                         | Tipo   | Descripción                                        |
| ----------------------------- | ------ | -------------------------------------------------- |
| `id_hist`                     | int64  | Identificador del paciente o registro clínico      |
| `diagnostico_principal_cie10` | string | Código CIE10 del diagnóstico principal             |
| `descripcion_diagnostico`     | string | Descripción textual del diagnóstico                |
| `servicio_troncal`            | string | Servicio médico principal (ej. urgencias, cirugía) |
| `sexo`                        | string | Sexo del paciente                                  |
| `edad`                        | string | Edad o rango etario del paciente                   |

---

### 🗺️ `dim_place`

| Campo                        | Tipo   | Descripción                                                      |
| ---------------------------- | ------ | ---------------------------------------------------------------- |
| `id_place`                   | int64  | Identificador de la ubicación o institución                      |
| `clave_entidad`              | int64  | Código del estado o departamento                                 |
| `nombre_entidad`             | string | Nombre del estado o departamento                                 |
| `clave_municipio`            | int64  | Código del municipio                                             |
| `nombre_municipio`           | string | Nombre del municipio                                             |
| `clave_localidad`            | int64  | Código de localidad                                              |
| `nombre_localidad`           | string | Nombre de la localidad                                           |
| `lat_decimal`, `lon_decimal` | float  | Coordenadas geográficas                                          |
| `codigo_postal`              | int64  | Código postal                                                    |
| `clues`                      | string | Clave del hospital o unidad médica                               |
| `nivel_atencion`             | string | Nivel de atención hospitalaria (primario, secundario, terciario) |

---

### ⏰ `dim_time`

| Campo                                        | Tipo   | Descripción                          |
| -------------------------------------------- | ------ | ------------------------------------ |
| `id_time`                                    | int64  | Identificador de fecha               |
| `fecha`                                      | string | Fecha en formato YYYY-MM-DD          |
| `year`, `quarter`, `month`, `day`, `weekday` | int    | Desglose temporal para análisis OLAP |

---

### 🌦️ `dim_weather`

| Campo                                                                      | Tipo  | Descripción                                |
| -------------------------------------------------------------------------- | ----- | ------------------------------------------ |
| `id_weather`                                                               | int64 | Identificador del registro climático       |
| Temperaturas y humedad (`temperature_2m_mean`, `temperature_2m_max`, etc.) | float | Datos climáticos medios, máximos y mínimos |
| `precipitation_sum`, `precipitation_hours`                                 | float | Precipitación total y horas de lluvia      |
| `wind_speed_10m_max`, `shortwave_radiation_sum`, `daily_cloud_cover_mean`  | float | Indicadores atmosféricos                   |

---

### 🏥 `fact_table_beds`

| Campo                                      | Tipo         | Descripción                             |
| ------------------------------------------ | ------------ | --------------------------------------- |
| `id_time`, `id_place`, `id_weather`        | int          | Claves foráneas hacia dimensiones       |
| Variables `avg_...`                        | float        | Promedios de personal médico y recursos |
| `total_atencion_medica`                    | int          | Total de atenciones médicas             |
| `pacientes_hospital`                       | int          | Pacientes atendidos                     |
| `indicador_escasez_camas`, `nivel_escasez` | float/string | Métricas de saturación hospitalaria     |

---

### 🧾 `fact_table_days`

| Campo                               | Tipo  | Descripción                            |
| ----------------------------------- | ----- | -------------------------------------- |
| `id_time_ingreso`, `id_time_egreso` | int   | Claves de fechas de ingreso y egreso   |
| `id_place`, `id_hist`, `id_weather` | int   | Relaciones con lugar, paciente y clima |
| Variables `avg_...`                 | float | Recursos hospitalarios por día         |
| `total_atencion_medica`             | int   | Total de atenciones diarias            |
| `avg_dias_estancia`                 | float | Promedio de días de hospitalización    |

---

## 🧮 **Modelos OLAP**

### 🧊 **Modelo OLAP 1: Gestión de Recursos Hospitalarios**

**Tabla de hechos:** `fact_table_beds`
**Dimensiones:**

* `dim_place` (geografía y hospital)
* `dim_time` (fecha de registro)
* `dim_weather` (condiciones climáticas)

📊 **Posibles análisis:**

* Tasa de escasez de camas por mes, hospital o clima.
* Disponibilidad de personal médico por región.
* Correlación entre condiciones meteorológicas y saturación hospitalaria.
* Evolución temporal de los recursos hospitalarios.

> [!TIP]
> Ideal para paneles de control de **gestión hospitalaria** o **predicción de saturación de camas**.

---

### 🧊 **Modelo OLAP 2: Flujo de Pacientes y Estancias Hospitalarias**

**Tabla de hechos:** `fact_table_days`
**Dimensiones:**

* `dim_patient_history` (perfil clínico)
* `dim_place` (hospital o municipio)
* `dim_time` (fechas de ingreso/egreso)
* `dim_weather` (condiciones al momento del ingreso)

📈 **Posibles análisis:**

* Duración media de hospitalización por diagnóstico o clima.
* Cantidad de pacientes atendidos por municipio y servicio médico.
* Relación entre condiciones climáticas y número de ingresos.
* Estacionalidad de enfermedades (por mes o estación del año).

> [!IMPORTANT]
> Este modelo permite realizar análisis clínico-operativos para **optimizar la atención hospitalaria** y detectar **picos de demanda**.

---

## Almacenamiento

- Se usa [BigQuery](https://cloud.google.com/bigquery) como data warehouse del proyecto, para poder trabajar colaborativamente y simplificar el uso de SQL junto con un lenguaje como Python

# Actividades Semana 3

- [X] Análisis exploratorio de datos
- [X] ETL Scripts
- [X] Data warehouse on Big Query


## Actividades para la siguiente semana

- [ ] Hipótesis & Gráficos
- [ ] Interfaz de usuario
- [ ] Modelo predictivo

> Everything is uploaded to out [GitHub project](https://github.com/JSEB99/predictive-health-resources)
