import streamlit as st
from telemetry import TERRITORIO_CHILE, obtener_telemetria_completa
from ui_skyform import render_skyform

# Configuración inicial de la aplicación
st.set_page_config(
    page_title="Plataforma de Control y Observación Sensorial",
    page_icon="https://i.pinimg.com/1200x/24/dc/75/24dc75cd0617592b6d65c0a4a8af50d6.jpg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONTENEDOR SUPERIOR DE SELECCIÓN TERRITORIAL ---
st.markdown("##### Territorio Chileno ")

# Columnas adaptables para mantener responsividad en móviles y pantallas pequeñas
col_reg, col_ciu = st.columns([1, 1])

with col_reg:
    region_sel = st.selectbox(
        "Región",
        list(TERRITORIO_CHILE.keys()),
        index=5,
        key="selector_region_main"
    )

# Obtención del diccionario de ciudades según la región seleccionada
ciudades_dict = TERRITORIO_CHILE[region_sel]

with col_ciu:
    ciudad_sel = st.selectbox(
        "Comuna / Ciudad",
        list(ciudades_dict.keys()),
        index=2 if "Quilpué" in ciudades_dict else 0,
        key="selector_ciudad_main"
    )

# Coordenadas geográficas asociadas
lat, lon = ciudades_dict[ciudad_sel]

# Separador estético
st.markdown("<hr style='margin: 10px 0 20px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# --- OBTENCIÓN DE DATOS Y RENDERIZADO ---
datos = obtener_telemetria_completa(lat, lon, ciudad_sel, region_sel)
render_skyform(datos)
