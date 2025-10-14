from google.cloud import bigquery
import pandas as pd
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\sebas\AppData\Roaming\gcloud\application_default_credentials.json'

# Crear cliente con project_id
client = bigquery.Client(project="predictive-health-resources")

# Tu consulta: ajusta según tu dataset y tabla reales
query = """
SELECT *
FROM `predictive-health-resources.healht_analytics_gold.fact_table_beds`
LIMIT 10
"""

# Ejecutar consulta y guardar resultados en un DataFrame
query_job = client.query(query)

# Mostrar resultados
for row in query_job.result():
    print(row)
