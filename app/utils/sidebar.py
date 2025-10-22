import streamlit as st


def show_sidebar():
    st.sidebar.header(":red[Health] Resources Prediction 🏥", divider="red")

    st.sidebar.page_link("0_🏠_home.py", label="🏠 Inicio")
    st.sidebar.page_link("pages/1_📶_analysis.py", label="📊 Análisis de datos")
    st.sidebar.page_link("pages/2_🔎_prediction.py",
                         label="🔍 Predicción de datos")
    st.sidebar.page_link("pages/3_📞_contact.py", label="📩 Contacto")

    st.sidebar.header("Equipo 🤝", divider="red")
    st.sidebar.subheader("Predictive :red[health] resources")

    st.sidebar.link_button(
        label="Proyecto en GitHub",
        url="https://github.com/JSEB99/predictive-health-resources",
        type="primary"
    )
