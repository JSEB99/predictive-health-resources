import streamlit as st
import utils.sidebar as sb

sb.show_sidebar()

st.header("📞 Contacto", divider="red")

st.subheader("Integrantes:")
name, github = st.columns(2)

name.write("Sebastian Mora")
github.markdown('[GitHub](https://github.com/JSEB99)')
name.write("Luis Flores")
github.markdown('[GitHub](https://github.com/https://github.com/LuisF1412)')

st.subheader(":red[No Country]")
st.markdown(
    "Proyecto de [simulación laboral](https://www.nocountry.tech/)")
