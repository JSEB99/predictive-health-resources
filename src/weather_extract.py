# Libraries
import polars as pl
import openmeteo_requests
import requests_cache
from retry_requests import retry
import time
import datetime as dt
import os

# 0. Check file
rewrite = False
filepath = '../data/weather_api.csv'

if os.path.exists(filepath):
    try:
        user = input(
            "El archivo ya existe. ¿Quieres sobreescribirlo? (Y/N): ").strip().upper()
        if user == 'Y':
            os.remove(filepath)
            rewrite = True
        else:
            print("No se sobreescribirá el archivo.")
    except Exception as e:
        print(f'Error al manejar el archivo: {e}')
else:
    rewrite = True


if rewrite:
    # Values for the API
    # 1. Read data
    df = pl.scan_csv('../data/egresos_resources_final.csv')

    # 2. Min & Max dates
    min_date = df.select(pl.col('fecha_ingreso'))\
        .min().collect()[0, 0]
    max_date = df.select(pl.col('fecha_egreso'))\
        .max().collect()[0, 0]

    # 3. Unique latitudes-longitures pairs
    unique_coords = df.select(pl.col('lat_decimal', 'lon_decimal')).unique()
    api_data = unique_coords.with_columns([
        pl.lit(min_date).alias('start_date'),
        pl.lit(max_date).alias('end_date')
    ]
    )

    # 4. SetUp the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    URL = "https://archive-api.open-meteo.com/v1/archive"

    dfs = []
    # 5. Extract data per row
    for row in api_data.collect().iter_rows(named=True):
        lat = row['lat_decimal']
        lon = row['lon_decimal']
        start = row['start_date']
        end = row['end_date']
        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': start,
            'end_date': end,
            'daily': [
                "temperature_2m_mean", "temperature_2m_max", "apparent_temperature_max",
                "temperature_2m_min", "apparent_temperature_min", "wet_bulb_temperature_2m_mean",
                "wind_speed_10m_max", "shortwave_radiation_sum", "precipitation_sum", "precipitation_hours",
                "dew_point_2m_mean", "relative_humidity_2m_mean", "cloud_cover_mean"],
            'timezone': 'America/Mexico_City'
        }

        try:
            responses = openmeteo.weather_api(URL, params=params)
            response = responses[0]

            daily = response.Daily()
            start_ts = dt.datetime.fromtimestamp(daily.Time())
            interval = dt.timedelta(seconds=daily.Interval())
            n = len(daily.Variables(0).ValuesAsNumpy())
            dates = [(start_ts + i * interval).date() for i in range(n)]

            df_weather = pl.DataFrame({
                "date": dates,
                "temperature_2m_mean": daily.Variables(0).ValuesAsNumpy(),
                "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
                "apparent_temperature_max": daily.Variables(2).ValuesAsNumpy(),
                "temperature_2m_min": daily.Variables(3).ValuesAsNumpy(),
                "apparent_temperature_min": daily.Variables(4).ValuesAsNumpy(),
                "daily_wet_bulb_temperature_2m_mean": daily.Variables(5).ValuesAsNumpy(),
                "wind_speed_10m_max": daily.Variables(6).ValuesAsNumpy(),
                "shortwave_radiation_sum": daily.Variables(7).ValuesAsNumpy(),
                "precipitation_sum": daily.Variables(8).ValuesAsNumpy(),
                "precipitation_hours": daily.Variables(9).ValuesAsNumpy(),
                "daily_dew_point_2m_mean": daily.Variables(10).ValuesAsNumpy(),
                "daily_relative_humidity_2m_mean": daily.Variables(11).ValuesAsNumpy(),
                "daily_cloud_cover_mean": daily.Variables(12).ValuesAsNumpy(),
                "lat": [lat] * n,
                "lon": [lon] * n
            })

            print(
                f"Procesando coordenadas ({lat}, {lon}) con {n} registros...")
            dfs.append(df_weather)
            time.sleep(6)

        except Exception as e:
            print(f'Error an coordenadas ({lat}, {lon}): {e}')
    # 6. Export data
    if dfs:
        final_df = pl.concat(dfs, how='vertical')
        final_df.write_csv(filepath)
        print("Archivo exportado correctamente.")
    else:
        print("No se generaron datos para exportar.")
