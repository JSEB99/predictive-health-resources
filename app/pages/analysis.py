import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import utils.sidebar as sb
import utils.functions as uf

st.set_page_config(
    page_title="Análisis EDA",
    page_icon="📊",
    layout="wide"
)

sb.show_sidebar() 

st.markdown("""
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
            """, 
            unsafe_allow_html=True)

def kpi_card(icon: str, title: str, value: str, bg_color: str = "#F0F2F6"):
    """
    Muestra una tarjeta de KPI simple y personalizable.
    """
    st.markdown(f"""
    <div style="
        background-color: {bg_color}; 
        border-radius: 10px; 
        padding: 20px; 
        border: 1px solid #E0E0E0;
        height: 180px; /* <-- Mantenemos la altura fija */
        display: flex; 
        flex-direction: column; 
        justify-content: space-between;
    ">
        <div style="
            font-size: 22px; /* <-- REDUCIDO de 24px */
            font-weight: bold; 
            color: #31333F;
            line-height: 1.2; /* <-- Añadido por si el título necesita dos líneas */
        ">
            <span style="
                font-size: 26px; /* <-- REDUCIDO de 28px */
                color: #D33682; 
                vertical-align: text-bottom; 
                margin-right: 8px;
            ">
                {icon}
            </span>
            {title}
        </div>
        <div style="
            font-size: 32px; /* <-- REDUCIDO de 36px */
            font-weight: bold; 
            color: #D33682; 
            margin-top: 10px; 
            text-align: left;
            line-height: 1.1; /* <-- Línea más apretada para el valor */
        ">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Título Principal
st.title("📊 Análisis Exploratorio de Datos (EDA): Demanda Hospitalaria")
st.markdown("Visualización de los 7 análisis fundamentales sobre los recursos hospitalarios (camas, personal, servicios).")


# SECCIÓN DE KPIs EN TARJETAS
st.header("KPIs Principales (Resumen del EDA)", divider='red')
st.markdown("Los hallazgos cuantitativos clave de nuestro análisis exploratorio.")

# Datos de KPI
kpis = uf.load_all_kpis()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card('<i class="bi bi-house"></i>', "Pico Ocupación Camas", kpis["pico_ocupacion"])

with col2:
    kpi_card('<i class="bi bi-graph-up"></i>', "Rango Operativo (Ingreso/Día)", kpis["rango_ingresos"])
    
with col3:
    kpi_card('<i class="bi bi-hourglass-split"></i>', "Mediana Estancia (Med. Int.)", kpis["mediana_estancia"])

with col4:
    kpi_card('<i class="bi bi-hospital"></i>', "Carga (Tercer Nivel)", kpis["carga_tercer_nivel"])

# SECCIÓN 1: KPIs PRINCIPALES: LA DEMANDA EN EL TIEMPO
st.header("Análisis de la Demanda en el Tiempo", divider='red')
st.markdown("Visión macro de las dos métricas fundamentales: Ocupación (stock de camas) e Ingresos (flujo de pacientes).")

st.subheader("Análisis #1: Ocupación Real de Camas")
fig1 = uf.plot_analisis_1()
st.pyplot(fig1)
st.info("""
**Interpretación:** La ocupación total de camas (stock) exhibe un claro **patrón estacional** predecible.
* Los picos ocurren consistentemente en invierno, acercándose a las **~3,800 camas** ocupadas.
* Los valles se presentan en verano, con una demanda base en torno a las 3,100 camas.
""")

st.subheader("Análisis #2: Flujo de Demanda Diaria")
fig2 = uf.plot_analisis_2()
st.pyplot(fig2)
st.info("""
**Interpretación:** El flujo de *nuevos ingresos* diarios es extremadamente volátil.
* El **rango operativo normal** (excluyendo valores atípicos iniciales) oscila entre **351 y 835 admisiones diarias**.
""")

# SECCIÓN 2: IMPULSORES DE LA DEMANDA: ¿CUÁNDO Y POR QUÉ?
st.header("Impulsores de la Demanda: ¿Cuándo y Por Qué?", divider='red')
st.markdown("Identificación de los patrones temporales y los servicios que componen la demanda.")

st.subheader("Análisis #5: Patrones Temporales de Demanda")
fig5 = uf.plot_analisis_5()
st.pyplot(fig5)
st.info("""
**Interpretación:** La demanda muestra fuertes ciclos temporales, evidentes en la **mediana** de ingresos diarios:
* **Ciclo Semanal:** La mediana de ingresos se mantiene alta y estable de **Lunes a Jueves**. Luego, **desciende notablemente el Viernes** y alcanza sus **puntos más bajos durante el Sábado y Domingo**.
* **Ciclo Mensual:** La mediana de ingresos es significativamente **más alta en los meses de invierno** (Enero, Febrero, Diciembre) y tiende a ser **más baja durante los meses de verano y otoño (junio - diciembre)**.
""")

st.subheader("Análisis #4: Composición de la Demanda por Servicio")
fig4 = uf.plot_analisis_4()
st.pyplot(fig4)
st.info("""
**Interpretación:** La demanda hospitalaria se compone de servicios con perfiles de volatilidad muy diferentes.
* **Gineco-Obtetricia** muestra la volatilidad más extrema, con picos que se acercan a los 5,000 ingresos semanales.
* **Cirugía General** presenta una base de demanda más estable, aunque también con fluctuaciones.
""")

# SECCIÓN 3: IMPACTO EN RECURSOS: ¿QUIÉN Y POR CUÁNTO TIEMPO?
st.header("Impacto en Recursos: ¿Quién y Por Cuánto Tiempo?", divider='red')
st.markdown("Análisis del consumo de camas y la carga de trabajo por tipo de hospital.")

st.subheader("Análisis #6: Duración de Estancia y Diagnósticos")
st.markdown("El consumo de camas depende críticamente del servicio al que ingresa el paciente.")
fig6_contexto = uf.plot_analisis_6_contexto()
st.pyplot(fig6_contexto)

st.info("""
**Interpretación:** El consumo de camas (recursos) depende críticamente de la duración de la estancia, la cual varía significativamente por servicio.
* La estancia mediana en **Medicina Interna (5 días)** es considerablemente mayor que en **Gineco-Obstetricia, Cirugía General y Pediatría (2 días)**.
""")

st.subheader("Sub-Análisis 6: Causa de las Estancias Atípicas")
st.markdown("Diagnósticos específicos que causan las estancias más largas en cada servicio.")
fig6_outliers = uf.plot_analisis_6_outliers()
st.pyplot(fig6_outliers)

st.info("""
**Interpretación:** Las estancias atípicamente largas (outliers) no son aleatorias, sino que son impulsadas por **diagnósticos específicos** para cada servicio.
* Identificar estas causas raíz (ej. "Neumonía" en Medicina Interna) permite enfocar estrategias de gestión y eficiencia.
""")

st.subheader("Análisis #3: Carga de Pacientes por Nivel de Atención")
fig3 = uf.plot_analisis_3()
st.pyplot(fig3)
st.info("""
**Interpretación:** La carga de trabajo está fuertemente concentrada por nivel.
* Los hospitales de **Tercer Nivel** manejan la gran mayoría de la demanda, promediando **~23 ingresos diarios** por hospital.
* La carga disminuye drásticamente en el **Segundo Nivel** (~6 ingresos/día).
* La carga es mínima en el **Primer Nivel** (~2 ingresos/día).
""")

# SECCIÓN 4: ANÁLISIS GEOESPACIAL: ¿DÓNDE OCURRE?
st.header("Análisis Geoespacial: ¿Dónde Ocurre?", divider='red')
st.markdown("Identificación de las regiones geográficas que concentran la mayor carga de trabajo.")

st.subheader("Análisis #7: Puntos Calientes Geográficos")
fig7 = uf.plot_analisis_7()
st.pyplot(fig7)
st.info("""
**Interpretación:** La demanda hospitalaria presenta una alta **concentración geográfica**.
* Entidades como **Ciudad de México, Michoacán De Ocampo y Veracruz** concentran una parte significativa de la carga de trabajo.
""")
