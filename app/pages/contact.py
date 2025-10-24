import streamlit as st
import utils.sidebar as sb

st.set_page_config(page_title="Contact", page_icon="📞")

sb.show_sidebar()

st.markdown("<h1 style='text-align: center; color: rgb(189, 64, 67);'>Contacto</h1>",
            unsafe_allow_html=True)
st.divider()
st.subheader(":red[Integrantes:]")
name, github = st.columns(2)

name.write("Sebastian Mora")
github.markdown('[GitHub](https://github.com/JSEB99)')
name.write("Luis Flores")
github.markdown('[GitHub](https://github.com/https://github.com/LuisF1412)')

st.subheader(":red[No Country]")
st.markdown(
    "Proyecto de [simulación laboral](https://www.nocountry.tech/)")
