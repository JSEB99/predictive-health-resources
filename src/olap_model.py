# Libraries
import polars as pl
from datetime import date
import os

# Link resources & weather API
# 1.Read data
egresos_resources = pl.scan_csv('../data/egresos_resources_final.csv')
weather = pl.scan_csv('../data/weather_api.csv')

# 2. Join data
data = egresos_resources.join(
    weather,
    left_on=['fecha_ingreso', 'lat_decimal', 'lon_decimal'],
    right_on=['date', 'lat', 'lon'],
    how='left'
)

# Prepare dimensions
# 1. Time Dimension
inicio = data.select(pl.col('fecha_ingreso').min()).collect()[0, 0]
fin = data.select(pl.col('fecha_egreso').max()).collect()[0, 0]

year, month, day = inicio[:4], inicio[5:7], inicio[8:]
yearf, monthf, dayf = fin[:4], fin[5:7], fin[8:]

rango_fechas = pl.date_range(
    start=date(int(year), 1, 1),
    end=date(int(yearf), int(monthf), int(dayf)),
    interval='1d',
    closed='both',
    eager=True
)

dim_time = pl.DataFrame({
    'fecha': rango_fechas
}).lazy()

dim_time = dim_time.with_columns([
    pl.col('fecha').dt.year().alias('year'),
    pl.col('fecha').dt.quarter().alias('quarter'),
    pl.col('fecha').dt.month().alias('month'),
    pl.col('fecha').dt.day().alias('day'),
    pl.col('fecha').dt.weekday().alias('weekday')
])

dim_time = dim_time.with_columns(
    pl.col('fecha').cast(pl.Date)
).sort('fecha').with_row_index('id_time', offset=1)

# 2. Place dimension
dim_place = data.select([
    'clave_entidad', 'nombre_entidad', 'clave_municipio', 'nombre_municipio',
    'clave_localidad', 'nombre_localidad', 'lat_decimal', 'lon_decimal', 'codigo_postal',
    'clues', 'nivel_atencion'
]).unique().sort(['clave_entidad', 'clave_municipio', 'clave_localidad', 'clues', 'lat_decimal', 'lon_decimal', 'codigo_postal', 'nivel_atencion'])\
    .with_row_index('id_place', offset=1)

# 3. Hospital history dimension
dim_patient_history = data.select([
    'diagnostico_principal_cie10', 'descripcion_diagnostico', 'servicio_troncal', 'sexo', 'edad'
]).unique().sort(
    ['diagnostico_principal_cie10', 'servicio_troncal', 'sexo', 'edad']
).with_row_index('id_hist', offset=1)

# 4. Weather dimension
dim_weather = data.select([
    'temperature_2m_mean', 'temperature_2m_max', 'apparent_temperature_max', 'temperature_2m_min',
    'apparent_temperature_min', 'daily_wet_bulb_temperature_2m_mean', 'wind_speed_10m_max',
    'shortwave_radiation_sum', 'precipitation_sum', 'precipitation_hours', 'daily_dew_point_2m_mean',
    'daily_relative_humidity_2m_mean', 'daily_cloud_cover_mean',
]).unique().sort(
    [
        'temperature_2m_mean', 'temperature_2m_max', 'apparent_temperature_max', 'temperature_2m_min',
        'apparent_temperature_min', 'daily_wet_bulb_temperature_2m_mean', 'wind_speed_10m_max',
        'shortwave_radiation_sum', 'precipitation_sum', 'precipitation_hours', 'daily_dew_point_2m_mean',
        'daily_relative_humidity_2m_mean', 'daily_cloud_cover_mean'
    ]
).with_row_index('id_weather', offset=1)

# Prepare Fact Table

data = data.with_columns([
    pl.col('fecha_ingreso')
    .str.strptime(pl.Date, "%Y-%m-%d").dt.date().alias('fecha_ingreso'),
    pl.col('fecha_egreso')
    .str.strptime(pl.Date, "%Y-%m-%d").dt.date().alias('fecha_egreso')
])

data = data.with_columns(
    (
        pl.col('fecha_egreso') - pl.col('fecha_ingreso')
    ).dt.total_days().alias('dias_estancia')
)

# 1. Estancia Fact Table
fact_days = data.join(
    dim_time, left_on='fecha_ingreso',
    right_on='fecha', how='left').rename({'id_time': 'id_time_ingreso'})\
    .join(
        dim_time, left_on='fecha_egreso',
        right_on='fecha', how='left').rename({'id_time': 'id_time_egreso'})\
    .join(
        dim_patient_history, on=[
            'diagnostico_principal_cie10',
            'descripcion_diagnostico', 'servicio_troncal', 'sexo', 'edad'],
    how='left')\
    .join(
        dim_place,
    on=[
        'clave_entidad', 'nombre_entidad', 'clave_municipio', 'nombre_municipio',
        'clave_localidad', 'nombre_localidad', 'lat_decimal', 'lon_decimal', 'codigo_postal',
        'clues', 'nivel_atencion'
    ], how='left')\
    .join(dim_weather, on=[
        'temperature_2m_mean', 'temperature_2m_max', 'apparent_temperature_max',
        'temperature_2m_min', 'apparent_temperature_min', 'daily_wet_bulb_temperature_2m_mean',
        'wind_speed_10m_max', 'shortwave_radiation_sum', 'precipitation_sum', 'precipitation_hours',
        'daily_dew_point_2m_mean', 'daily_relative_humidity_2m_mean', 'daily_cloud_cover_mean'
    ], how='left')\
    .select([
        'id_time_ingreso', 'id_time_egreso', 'id_place', 'id_hist', 'id_weather',

        'personal_medico_general', 'personal_medico_esp',
        'ginecoobstetras', 'pediatras', 'cirujanos', 'internistas',
        'anestesiologos', 'odontologos', 'pasantes', 'personal_hospital',
        'enfermeras_general', 'enfermeras_esp', 'atencion_medica',
        'camas_hospitalizacion', 'camas_atencion_temporal', 'labs', 'dias_estancia'
    ])
fact_table_days = fact_days.group_by([
    'id_time_ingreso', 'id_time_egreso', 'id_place', 'id_hist', 'id_weather'
]).agg([
    pl.mean('personal_medico_general').alias('avg_personal_medico_general'),
    pl.mean('personal_medico_esp').alias('avg_personal_medico_esp'),
    pl.mean('ginecoobstetras').alias('avg_ginecoobstetras'),
    pl.mean('pediatras').alias('avg_pediatras'),
    pl.mean('cirujanos').alias('avg_cirujanos'),
    pl.mean('internistas').alias('avg_internistas'),
    pl.mean('anestesiologos').alias('avg_anestesiologos'),
    pl.mean('odontologos').alias('avg_odontologos'),
    pl.mean('pasantes').alias('avg_pasantes'),
    pl.mean('personal_hospital').alias('avg_personal_hospital'),
    pl.mean('enfermeras_general').alias('avg_enfermeras_general'),
    pl.mean('enfermeras_esp').alias('avg_enfermeras_esp'),
    pl.sum('atencion_medica').alias('total_atencion_medica'),
    pl.mean('camas_hospitalizacion').alias('avg_camas_hospitalizacion'),
    pl.mean('camas_atencion_temporal').alias('avg_camas_atencion_temporal'),
    pl.mean('labs').alias('avg_labs'),
    pl.mean('dias_estancia').alias('avg_dias_estancia')
])

# 2. Beds Fact Table
expanded_data = data.with_columns([
    pl.date_ranges(
        start=pl.col("fecha_ingreso"),
        end=pl.col("fecha_egreso"),
        interval="1d",
        closed="both"  # incluye ambas fechas
    ).alias("fecha_instancia")
]).explode("fecha_instancia")

fact_beds = expanded_data.join(
    dim_time, left_on='fecha_instancia',
    right_on='fecha', how='left')\
    .join(dim_place, on=[
        'clave_entidad', 'nombre_entidad', 'clave_municipio', 'nombre_municipio',
        'clave_localidad', 'nombre_localidad', 'lat_decimal', 'lon_decimal', 'codigo_postal',
        'clues', 'nivel_atencion'
    ], how='left')\
    .join(dim_weather, on=[
        'temperature_2m_mean', 'temperature_2m_max', 'apparent_temperature_max',
        'temperature_2m_min', 'apparent_temperature_min', 'daily_wet_bulb_temperature_2m_mean',
        'wind_speed_10m_max', 'shortwave_radiation_sum', 'precipitation_sum', 'precipitation_hours',
        'daily_dew_point_2m_mean', 'daily_relative_humidity_2m_mean', 'daily_cloud_cover_mean'
    ], how='left')\
    .select([
        'id_time', 'id_place', 'id_weather',

        'personal_medico_general', 'personal_medico_esp',
        'ginecoobstetras', 'pediatras', 'cirujanos', 'internistas',
        'anestesiologos', 'odontologos', 'pasantes', 'personal_hospital',
        'enfermeras_general', 'enfermeras_esp', 'atencion_medica',
        'camas_hospitalizacion', 'camas_atencion_temporal', 'labs', 'dias_estancia'
    ])

fact_table_beds = fact_beds.group_by([
    'id_time', 'id_place', 'id_weather'
]).agg([
    pl.mean('personal_medico_general').alias('avg_personal_medico_general'),
    pl.mean('personal_medico_esp').alias('avg_personal_medico_esp'),
    pl.mean('ginecoobstetras').alias('avg_ginecoobstetras'),
    pl.mean('pediatras').alias('avg_pediatras'),
    pl.mean('cirujanos').alias('avg_cirujanos'),
    pl.mean('internistas').alias('avg_internistas'),
    pl.mean('anestesiologos').alias('avg_anestesiologos'),
    pl.mean('odontologos').alias('avg_odontologos'),
    pl.mean('pasantes').alias('avg_pasantes'),
    pl.mean('personal_hospital').alias('avg_personal_hospital'),
    pl.mean('enfermeras_general').alias('avg_enfermeras_general'),
    pl.mean('enfermeras_esp').alias('avg_enfermeras_esp'),
    pl.sum('atencion_medica').alias('total_atencion_medica'),
    pl.mean('camas_hospitalizacion').alias('avg_camas_hospitalizacion'),
    pl.mean('camas_atencion_temporal').alias('avg_camas_atencion_temporal'),
    pl.mean('labs').alias('avg_labs'),
    pl.mean('dias_estancia').alias('avg_dias_estancia'),
    pl.len().alias('pacientes_hospital')
])

fact_table_beds = fact_table_beds.with_columns(
    (pl.when(
        (
            pl.col('avg_camas_hospitalizacion') +
            pl.col('avg_camas_atencion_temporal')) > 0
    ).then(
        pl.col('pacientes_hospital') / (pl.col('avg_camas_hospitalizacion') +
                                        pl.col('avg_camas_atencion_temporal'))
    ).otherwise(None)
        .alias('indicador_escasez_camas'))
)

fact_table_beds = fact_table_beds.with_columns(
    pl.when(pl.col('indicador_escasez_camas') > 1).then(pl.lit("Alta escasez"))
    .when(pl.col('indicador_escasez_camas') > 0.9).then(pl.lit("Moderada"))
    .when(pl.col('indicador_escasez_camas').is_null()).then(pl.lit("Sin datos"))
    .otherwise(pl.lit("Adecuada"))
    .alias("nivel_escasez")
)


# Export data

output_dir = '../data/gold/'
os.makedirs(output_dir, exist_ok=True)

outputs = [
    ('dim_time.csv', dim_time),
    ('dim_place.csv', dim_place),
    ('dim_patient_history.csv', dim_patient_history),
    ('dim_weather.csv', dim_weather),
    ('fact_table_days.csv', fact_table_days),
    ('fact_table_beds.csv', fact_table_beds)
]

for filename, df_lazy in outputs:
    full_path = os.path.join(output_dir, filename)

    if os.path.exists(full_path):
        respuesta = input(
            f'⚠️ El archivo "{filename}" ya existe. ¿Deseas sobrescribirlo? (s/n): ').strip().lower()
        if respuesta not in ['s', 'y']:
            print(f'⏩ Archivo "{filename}" no será sobrescrito.')
            continue

    print(f'💾 Guardando: {filename}...')
    df_lazy.collect().write_csv(full_path)

print("✅ Proceso finalizado.")
