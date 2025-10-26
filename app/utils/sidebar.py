import streamlit as st
from functools import lru_cache


@lru_cache(maxsize=1)
def load_sidebar_html():
    with open("./app/utils/sidebar.html", "r", encoding="utf-8") as file:
        return file.read()


def show_sidebar():
    sidebar_html = load_sidebar_html()
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
