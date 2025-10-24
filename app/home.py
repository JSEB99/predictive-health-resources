import streamlit as st
import utils.sidebar as sb

st.set_page_config(
    page_title="Análisis y Predicción de los recursos de salud en México",
    layout="wide",
    page_icon="🏥"
)

sb.show_sidebar()

st.markdown("<h1 style='text-align: center; color: rgb(189, 64, 67);'>Predictive Health Resources</h1>",
            unsafe_allow_html=True)
st.divider()
st.subheader(":red[Descripción]")
st.markdown("Este proyecto realiza un **análisis y predicción** de los recursos en **instituciones de salud** en **México**, utilizando información a nivel de **CLUES (Catálogo Único de Establecimientos de Salud)**. Se integraron múltiples fuentes de datos, incluyendo registros de ingresos y egresos hospitalarios, variables climáticas, ubicación geográfica y datos temporales. A través de técnicas de análisis de datos y modelos predictivos, se identifican patrones que permiten comprender el comportamiento de la demanda en los centros de salud.")
st.subheader(":red[Objetivo]")
st.markdown("El objetivo principal es predecir la **cantidad de pacientes** que recibirá un centro de salud en un día específico. Esta predicción permite optimizar la planificación y asignación de recursos médicos, mejorando la capacidad de respuesta del sistema de salud ante diferentes condiciones temporales y geográficas.")
