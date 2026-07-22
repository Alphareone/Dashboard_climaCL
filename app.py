import streamlit as st
from telemetry import TERRITORIO_CHILE, obtener_telemetria_completa
from ui_skyform import render_skyform

st.set_page_config(
    page_title="Plataforma de Control y Observación Sensorial",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar de Selección
st.sidebar.title("Territorio Chile")
st.sidebar.caption("Plataforma Integrada de Control y Observación Sensorial")

region_sel = st.sidebar.selectbox("Región", list(TERRITORIO_CHILE.keys()), index=5)
ciudades_dict = TERRITORIO_CHILE[region_sel]
ciudad_sel = st.sidebar.selectbox("Comuna / Ciudad", list(ciudades_dict.keys()), index=2 if "Quilpué" in ciudades_dict else 0)

lat, lon = ciudades_dict[ciudad_sel]

# Obtención de Datos de Telemetría
datos = obtener_telemetria_completa(lat, lon, ciudad_sel, region_sel)

# Render de la vista principal Skyform
render_skyform(datos)