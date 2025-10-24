import streamlit as st
import pandas as pd
import requests
import utils.sidebar as sb

place = pd.read_csv('../data/gold/dim_place.csv')
place['opc'] = place['nombre_entidad'] + ' | ' + place['nombre_municipio'] + \
    ' | ' + place['nombre_localidad'] + ' | ' + \
    place['codigo_postal'].astype(str)

st.set_page_config(page_title="Prediction", page_icon="🔎", layout='wide')

sb.show_sidebar()

st.markdown("<h1 style='text-align: center;'>Predictor de cantidad de pacientes</h1>",
            unsafe_allow_html=True)
st.markdown("""
Modelo de regresion para predecir la cantidad de pacientes por Catálogo de Clave Única de Establecimientos de Salud *(CLUES)* y Fecha, según unas cuantas caracteristicas propias de la institución. Este modelo busca prevenir a las instituciones en el uso de los recursos como camas, personal médico, equipo médico, entre otros para asi estar mejor preparados y ayudar a tener un mejor planteamiento de la ejecución de servicios gracias a la predicción de pacientes probables durante determinadas fechas
""")

with st.form("prediction", border=False):
    st.subheader(":red[Datos requeridos:]")
    fecha = st.date_input('Fecha', format='YYYY-MM-DD', min_value='2023-12-31')
    lugar = st.selectbox('Lugar', place['opc'].unique())

    st.subheader(":red[Datos del establecimiento]")

    # --- Fila 1
    c1, c2, c3 = st.columns(3)
    avg_personal_medico_general = c1.number_input(
        "Médico general (avg)", value=3000)
    avg_personal_medico_esp = c2.number_input(
        "Médico especializado (avg)", value=1500)
    avg_ginecoobstetras = c3.number_input("Gineco-obstetras (avg)", value=120)

    # --- Fila 2
    c1, c2, c3 = st.columns(3)
    avg_pediatras = c1.number_input("Pediatras (avg)", value=100)
    avg_cirujanos = c2.number_input("Cirujanos (avg)", value=110)
    avg_internistas = c3.number_input("Internistas (avg)", value=60)

    # --- Fila 3
    c1, c2, c3 = st.columns(3)
    avg_anestesiologos = c1.number_input("Anestesiólogos (avg)", value=130)
    avg_odontologos = c2.number_input("Odontólogos (avg)", value=10)
    avg_pasantes = c3.number_input("Pasantes (avg)", value=20)

    # --- Fila 4
    c1, c2, c3 = st.columns(3)
    avg_personal_hospital = c1.number_input(
        "Personal hospital (avg)", value=3500)
    avg_enfermeras_general = c2.number_input(
        "Enfermeras generales (avg)", value=600)
    avg_enfermeras_esp = c3.number_input("Enfermeras esp. (avg)", value=130)

    # --- Fila 5
    c1, c2, c3 = st.columns(3)
    avg_camas_hospitalizacion = c1.number_input(
        "Camas hospitalización (avg)", value=700)
    avg_camas_atencion_temporal = c2.number_input(
        "Camas atención temporal (avg)", value=250)
    avg_labs = c3.number_input("Laboratorios (avg)", value=10)

    # --- Fila 6
    c1, c2, c3 = st.columns(3)
    avg_dias_estancia = c1.number_input("Días estancia (avg)", value=40)
    total_atencion_medica = c2.number_input(
        "Total atención médica", value=9000)
    lag_1 = c3.number_input("Lag 1", value=80)

    # --- Fila 7
    c1, c2, c3 = st.columns(3)
    delta_1 = c1.number_input("Delta 1", value=5)
    rolling_mean_3 = c2.number_input("Media móvil 3", value=85)

    submitted = st.form_submit_button('Predecir', width="stretch")

    place_parts = lugar.split(' | ')

    if submitted:
        user = {
            "avg_personal_medico_general": avg_personal_medico_general,
            "avg_personal_medico_esp": avg_personal_medico_esp,
            "avg_ginecoobstetras": avg_ginecoobstetras,
            "avg_pediatras": avg_pediatras,
            "avg_cirujanos": avg_cirujanos,
            "avg_internistas": avg_internistas,
            "avg_anestesiologos": avg_anestesiologos,
            "avg_odontologos": avg_odontologos,
            "avg_pasantes": avg_pasantes,
            "avg_personal_hospital": avg_personal_hospital,
            "avg_enfermeras_general": avg_enfermeras_general,
            "avg_enfermeras_esp": avg_enfermeras_esp,
            "avg_camas_hospitalizacion": avg_camas_hospitalizacion,
            "avg_camas_atencion_temporal": avg_camas_atencion_temporal,
            "avg_labs": avg_labs,
            "avg_dias_estancia": avg_dias_estancia,
            "total_atencion_medica": total_atencion_medica,
            "lag_1": lag_1,
            "delta_1": delta_1,
            "rolling_mean_3": rolling_mean_3,
            "year": fecha.year,
            "quarter": (fecha.month - 1)//3 + 1,
            "month": fecha.month,
            "day": fecha.day,
            "weekday": fecha.weekday(),
            "nombre_entidad": place_parts[0],
            "nombre_municipio": place_parts[1],
            "nombre_localidad": place_parts[2],
            "codigo_postal": place_parts[3]
        }
        api_url = st.secrets["api"]["model"]

        response = requests.get(f'{api_url}/v1/predict/', json=user)
        api_response = response.json()
        st.write(api_response['No. of Patients'])
