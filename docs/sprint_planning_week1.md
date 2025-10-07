# 📊 Proyecto: Análisis y Relación de Egresos Hospitalarios con Recursos Institucionales

## 🏭 Integrantes:

- Luis Flores *(Data Analyst)*
- Juan Mora *(Data Analyst)*

## 🧾 Diccionario de Datos

### 📁 Dataset 1: Egresos Hospitalarios (`egresos_hospitalarios_issste2024.csv`)

- [FUENTE](https://datos.gob.mx/dataset/datos_egresos_hospitalarios/resource/9997a641-3c0e-4a76-95d2-32e765c61487): Datos abiertos de México

| Columna                     | Tipo       | Descripción                                     |
| --------------------------- | ---------- | ----------------------------------------------- |
| entidad                     | Texto      | Estado de la república                          |
| unidad                      | Texto      | Nombre de la unidad médica                      |
| clues                       | Texto      | CLUES (identificador único del establecimiento) |
| edad_anios                  | Numérico   | Edad del paciente en años                       |
| sexo                        | Texto      | Sexo del paciente (`hombre` / `mujer`)          |
| servicio_troncal            | Texto      | Servicio principal (ej. Cirugía General)        |
| tipo_derechohabiente        | Texto      | Tipo de afiliación al ISSSTE                    |
| fecha_ingreso               | Fecha-Hora | Fecha de ingreso hospitalario                   |
| fecha_egreso                | Fecha-Hora | Fecha de alta hospitalaria                      |
| diagnostico_principal_cie10 | Texto      | Código CIE-10 del diagnóstico                   |
| descripcion_cie_010         | Texto      | Descripción del diagnóstico                     |

---

### 📁 Dataset 2: Recursos Institucionales (`conjunto_de_datos_recursos_esep_2024.csv`)

- [FUENTE](https://www.inegi.org.mx/app/buscador/default.html?q=camas+hospitalarias): INEGI datos abiertos

> Contiene información detallada sobre recursos humanos, camas, equipos médicos, consultorios y más, por unidad médica y AGEB.

| Campo               | Tipo   | Descripción Resumida                                |
| ------------------- | ------ | --------------------------------------------------- |
| sreanio             | Entero | Año del reporte (2024)                              |
| sreentidad          | Texto  | Entidad federativa                                  |
| sremunic            | Texto  | Municipio o alcaldía                                |
| sreageb             | Texto  | AGEB de la unidad                                   |
| sretipoest          | Entero | Tipo de establecimiento (clínica, hospital, etc.)   |
| sre407              | Entero | Camas censables                                     |
| sre413              | Entero | Camas no censables                                  |
| sre423              | Entero | Número de quirófanos                                |
| sre404 - sre406     | Entero | Consultorios generales y de especialidad            |
| sre378_* a sre391_* | Entero | Personal médico por especialidad (nómina y acuerdo) |
| sre392 - sre403     | Entero | Personal no médico                                  |
| sre419 - sre444     | Entero | Equipamiento médico e instrumental                  |

### 📁 Dataset 3: Archivo CLUES (`ESTABLECIMIENTO_SALUD_202508.xlsx`)

- [FUENTE](http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html): Secretaría de Salud México

> Este archivo contiene información oficial y detallada de cada establecimiento de salud, con campos administrativos, geográficos y operativos.

| Columna                        | Tipo      | Descripción                                                                            |
| ------------------------------ | --------- | -------------------------------------------------------------------------------------- |
| CLUES                          | Texto     | Clave Única de Establecimientos de Salud (identificador oficial del establecimiento).  |
| CLAVE DE LA INSTITUCIÓN        | Texto     | Código numérico de la institución (ej. ISSSTE, IMSS, SSA, etc.)                        |
| NOMBRE DE LA INSTITUCIÓN       | Texto     | Nombre completo de la institución de salud (ej. Instituto Mexicano del Seguro Social). |
| CLAVE DE LA ENTIDAD            | Texto     | Clave numérica del estado donde se ubica la unidad.                                    |
| ENTIDAD                        | Texto     | Nombre del estado.                                                                     |
| CLAVE DEL MUNICIPIO            | Texto     | Clave numérica del municipio.                                                          |
| MUNICIPIO                      | Texto     | Nombre del municipio o alcaldía.                                                       |
| CLAVE DE LA LOCALIDAD          | Texto     | Código INEGI de la localidad.                                                          |
| LOCALIDAD                      | Texto     | Nombre de la localidad.                                                                |
| CLAVE DEL TIPO ESTABLECIMIENTO | Texto     | Código del tipo de establecimiento.                                                    |
| NOMBRE TIPO ESTABLECIMIENTO    | Texto     | Ejemplo: Hospital General, Centro de Salud, Clínica.                                   |
| NOMBRE DE LA UNIDAD            | Texto     | Nombre oficial de la unidad médica.                                                    |
| NOMBRE COMERCIAL               | Texto     | Nombre alternativo o comercial (si aplica).                                            |
| DIRECCIÓN                      | Compuesta | Campos: tipo de vialidad, vialidad, número, colonia, código postal.                    |
| ESTATUS DE OPERACIÓN           | Texto     | Estatus actual (Activo, Inactivo, En transición).                                      |
| FECHA DE INICIO DE OPERACIÓN   | Fecha     | Fecha en la que la unidad comenzó a operar.                                            |
| LATITUD / LONGITUD             | Numérico  | Coordenadas geográficas.                                                               |
| NIVEL DE ATENCIÓN              | Texto     | Nivel 1, 2 o 3 según la complejidad de servicios ofrecidos.                            |
| TIPOLOGÍA / SUBTIPOLOGÍA       | Texto     | Clasificación del establecimiento según su especialidad o alcance.                     |

---

# Relación del archivo CLUES con otros datasets

## 1. Relación con egresos hospitalarios (`egresos_hospitalarios_issste2024.csv`)
- **Clave de relación:** `CLUES`
- Cada registro de egreso está asociado a una unidad médica identificada por `CLUES`.
- El archivo CLUES se usa para enriquecer los datos de egresos con información sobre:
  - Ubicación (estado, municipio, localidad)
  - Tipo y nivel del establecimiento
  - Coordenadas geográficas
  - Tipología de la unidad médica

## 2. Relación con recursos institucionales (`conjunto_de_datos_recursos_esep_2024.csv`)
- **Clave de relación:** Idealmente `CLUES` si está presente.
- Si no, se puede usar una relación aproximada con:
  - Entidad + Municipio + Tipo de establecimiento + AGEB
  - Comprobación con nombre de la unidad para mayor precisión.

---

## Beneficios de integrar el archivo CLUES
- Estandariza nombres y tipos de unidades médicas en todos los datasets.
- Facilita el análisis geoespacial y la visualización de datos.
- Agrega contexto para análisis comparativos entre unidades similares.
- Ayuda a construir modelos predictivos más robustos y contextualizados.


---

## 🎯 Objetivo del Proyecto

**Relacionar la infraestructura hospitalaria y recursos médicos (por unidad de salud) con los egresos hospitalarios registrados.**  
Esto permitirá:

- Entender si hay una correlación entre la disponibilidad de recursos y los egresos.
- Estimar necesidades de personal, camas o quirófanos por unidad médica.
- Identificar posibles carencias o saturaciones por entidad o servicio.

---

## 🧭 Plan de Acción

### 1. 🔗 Unificación de datasets
- Relacionar ambos datasets mediante el campo `CLUES` (clave única del establecimiento de salud).
- Verificar correspondencia entre nombre de unidad, entidad y tipo de establecimiento si CLUES faltara en algún registro.

### 2. 📉 Resumen del dataset de recursos
- Agregar variables resumen por unidad médica:
  - `camas_totales = camas_censables + no_censables`
  - `personal_medico_total = suma de todas las especialidades`
  - `consultorios_totales = generales + especialidad`
  - `equipos_diagnostico = suma de rayos X, resonancia, ultrasonido, etc.`
  - `quirofanos = sre423`

### 3. 🧮 Análisis exploratorio (EDA)
- Distribución de egresos por:
  - Edad
  - Sexo
  - Servicio troncal
  - Diagnóstico (CIE-10)
  - Entidad / unidad
- Cruce con recursos disponibles por unidad:
  - ¿Más camas = más egresos?
  - ¿Faltan recursos donde hay muchos pacientes?

### 4. 🤖 Modelos predictivos
- Predecir egresos o requerimientos de recursos con modelos de regresión.
- Variables predictoras: tipo de unidad, camas, personal, ubicación, etc.

---

## 📌 Resultado Esperado

- Dataset final unificado con egresos y recursos por `CLUES`.
- Gráficos y tablas que muestren patrones y relaciones entre egresos y capacidad instalada.
- Base para tomar decisiones de asignación de recursos o evaluar eficiencia hospitalaria.

---

## 🎯 Pasos realizados

- [X] Buscar información relacionada con sistemas hospitalarios
- [X] Validar la veracidad de la información con fuentes oficiales
- [X] Planear el curso de acción con los datos

## ✨ Próximos pasos

- [ ] Asignar tareas para cada integrante **(2 integrantes)**
- [ ] Validar calidad de los datos (valores nulos, errores de codificación)
- [ ] Terminar de resumir recursos por unidad
- [ ] Unir datasets y comenzar análisis
- [ ] Implementar visualizaciones con seaborn / matplotlib / plotly