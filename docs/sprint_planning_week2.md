# Sprint - Plan semana 2

Despues de los resultados de la [semana 1](sprint_planning_week1.md), se obtuvo el siguiente conjunto de datos consolidado con los datos de los egresos del 2024 y recursos a 2024 de instituciones de salud en México.

Aquí tienes un **diccionario de datos en formato Markdown** para los campos que proporcionaste. Este diccionario describe cada columna de manera clara y concisa.

---

# 📘 Diccionario de Datos

| Campo                         | Descripción                                                 | Tipo de Dato        |
| ----------------------------- | ----------------------------------------------------------- | ------------------- |
| `lat_decimal`                 | Latitud geográfica en coordenadas decimales.                | `float`             |
| `lon_decimal`                 | Longitud geográfica en coordenadas decimales.               | `float`             |
| `clues`                       | Clave Única de Establecimientos de Salud.                   | `string`            |
| `servicio_troncal`            | Servicio médico principal.                                  | `string`            |
| `sexo`                        | Sexo del paciente.                                          | `string`            |
| `diagnostico_principal_cie10` | Código CIE-10 del diagnóstico principal.                    | `string`            |
| `descripcion_diagnostico`     | Descripción del diagnóstico principal.                      | `string`            |
| `clave_entidad_egresos`       | Clave numérica de la entidad federativa.                    | `int`               |
| `nombre_entidad`              | Nombre de la entidad federativa.                            | `string`            |
| `clave_municipio_egresos`     | Clave numérica del municipio.                               | `int`               |
| `nombre_municipio`            | Nombre del municipio.                                       | `string`            |
| `clave_localidad`             | Clave numérica de la localidad.                             | `int`               |
| `nombre_localidad`            | Nombre de la localidad.                                     | `string`            |
| `codigo_postal`               | Código postal (puede contener decimales si se importa mal). | `float` / `string`* |
| `nivel_atencion`              | Nivel de atención médica (ej. Segundo Nivel).               | `string`            |
| `edad_categoria`              | Rango de edad del paciente.                                 | `string`            |
| `year_ingreso`                | Año de ingreso hospitalario.                                | `int`               |
| `mes_ingreso`                 | Mes de ingreso hospitalario (1–12).                         | `int`               |
| `dia_sem_ingreso`             | Día de la semana del ingreso (0 = domingo).                 | `int`               |
| `year_egreso`                 | Año de egreso hospitalario.                                 | `int`               |
| `mes_egreso`                  | Mes de egreso hospitalario (1–12).                          | `int`               |
| `dia_sem_egreso`              | Día de la semana del egreso (0 = domingo).                  | `int`               |

---

### 👩‍⚕️ Recursos Humanos Médicos

| Campo                     | Descripción                      | Tipo de Dato |
| ------------------------- | -------------------------------- | ------------ |
| `personal_medico_general` | Número de médicos generales.     | `int`        |
| `personal_medico_esp`     | Número de médicos especialistas. | `int`        |
| `ginecoobstetras`         | Número de gineco-obstetras.      | `int`        |
| `pediatras`               | Número de pediatras.             | `int`        |
| `cirujanos`               | Número de cirujanos.             | `int`        |
| `internistas`             | Número de internistas.           | `int`        |
| `anestesiologos`          | Número de anestesiólogos.        | `int`        |
| `odontologos`             | Número de odontólogos.           | `int`        |
| `pasantes`                | Número de médicos pasantes.      | `int`        |
| `personal_hospital`       | Total de personal hospitalario.  | `int`        |

---

### 🧑‍⚕️ Enfermería

| Campo                | Descripción                         | Tipo de Dato |
| -------------------- | ----------------------------------- | ------------ |
| `enfermeras_general` | Número de enfermeras generales.     | `int`        |
| `enfermeras_esp`     | Número de enfermeras especialistas. | `int`        |

---

### 🏥 Infraestructura y Servicios

| Campo                                   | Descripción                                        | Tipo de Dato |
| --------------------------------------- | -------------------------------------------------- | ------------ |
| `atencion_medica`                       | Total de servicios de atención médica.             | `int`        |
| `camas_hospitalizacion`                 | Camas disponibles para hospitalización.            | `int`        |
| `camas_atencion_temporal`               | Camas temporales habilitadas.                      | `int`        |
| `labs`                                  | Laboratorios disponibles.                          | `int`        |
| `infraestructura_imagenologia`          | Servicios de imagenología.                         | `int`        |
| `infraestructura_radioterapia`          | Infraestructura para radioterapia.                 | `int`        |
| `infraestructura_quirurgica_obstetrica` | Salas quirúrgicas y obstétricas.                   | `int`        |
| `infraestructura_neonatal_pediatrica`   | Infraestructura para atención neonatal/pediátrica. | `int`        |
| `infraestructura_uci`                   | Unidades de Cuidados Intensivos.                   | `int`        |
| `infraestructura_urgencias_aislamiento` | Servicios de urgencias con aislamiento.            | `int`        |
| `infraestructura_diagnostico_funcional` | Diagnóstico funcional (ej. electrocardiograma).    | `int`        |
| `infraestructura_dialisis`              | Servicios de diálisis.                             | `int`        |
| `infraestructura_banco_sangre`          | Banco de sangre disponible.                        | `int`        |
| `infraestructura_odontologia`           | Servicios de odontología.                          | `int`        |

---

## 🎯 Objetivos para la siguiente semana

- [ ] Scripts para ETL
  - [ ] Extraer los datos automaticamente
  - [ ] Transformarlos y crear modelo OLAP
  - [ ] Cargarlos a la base de datos
- [ ] Análisis Exploratorio de los Datos
- [ ] Hipótesis para el análisis final
- [ ] Análisis inicial para el modelo predictivo

## 📚 Investigación

- Revisar servicios para desplegar la base de datos y mostrar los datos *(Supabase, firebase)*