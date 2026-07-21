import streamlit as st

st.set_page_config(page_title="P.I.C.O.S Chile Weather", page_icon="⚡", layout="wide")

from config import aplicar_estilos_base
from telemetry import obtener_datos_clima, generar_alertas_inteligentes
from components import (
    renderizar_alertas, 
    renderizar_tarjetas_adaptativas, 
    renderizar_mapa_multicapa
)

# Estilos CSS
aplicar_estilos_base()

# --- SIDEBAR ---
st.sidebar.title("⚡ P.I.C.O.S Weather")
st.sidebar.markdown("---")

# Selector de Perfil
modo_perfil = st.sidebar.radio(
    "Modo de Uso / Perfil",
    ["🏃 Ciudadano / Deporte", "🌾 Agrícola / Industria", "⚠️ Prevención de Riesgo"]
)

st.sidebar.markdown("---")

ciudades = {
    "Santiago": (-33.4489, -70.6693),
    "Valparaíso / Quilpué": (-33.0472, -71.6127),
    "Concepción": (-36.8201, -73.0444),
    "Antofagasta": (-23.6509, -70.3975),
    "Puerto Montt": (-41.4693, -72.9424)
}

ciudad_sel = st.sidebar.selectbox("Selección de Zona", list(ciudades.keys()))
lat, lon = ciudades[ciudad_sel]

st.sidebar.markdown("---")

# Selector de Capas para el Mapa
capa_mapa = st.sidebar.selectbox(
    "Capa Geoespacial",
    ["Temperatura (°C)", "Velocidad del Viento (km/h)", "Radiación / Índice UV"]
)

# --- CARGA DE DATOS ---
datos_clima = obtener_datos_clima(lat, lon)

if datos_clima and "current" in datos_clima:
    curr = datos_clima["current"]
    
    # Hero Card
    st.markdown(f'''
        <div class="hero-card">
            <span class="live-badge"></span> <small>TELEMÉTRICA EN VIVO - MODO: {modo_perfil.upper()}</small>
            <div class="hero-city">{ciudad_sel}, Chile</div>
            <div class="hero-temp">{curr.get("temperature_2m", "--")}°C</div>
        </div>
    ''', unsafe_allow_html=True)

    # 1. Alertas de IA
    alertas = generar_alertas_inteligentes(datos_clima)
    renderizar_alertas(alertas)
    st.markdown("---")

    # 2. Tarjetas con íconos vectoriales animados
    st.markdown(f"### Métricas Clave ({modo_perfil})")
    renderizar_tarjetas_adaptativas(curr, modo_perfil)
    st.markdown("---")

    # 3. Mapa con Zoom delimitado a Chile
    st.markdown(f"### Análisis Geoespacial - {capa_mapa}")
    
    datos_red_nacional = [
        {"nombre": "Santiago", "lat": -33.4489, "lon": -70.6693, "temperatura": curr.get("temperature_2m", 20), "viento": curr.get("wind_speed_10m", 12), "uv": curr.get("uv_index", 5)},
        {"nombre": "Valparaíso", "lat": -33.0472, "lon": -71.6127, "temperatura": curr.get("temperature_2m", 18) - 2, "viento": curr.get("wind_speed_10m", 12) + 10, "uv": curr.get("uv_index", 5)},
        {"nombre": "Concepción", "lat": -36.8201, "lon": -73.0444, "temperatura": 15, "viento": 25, "uv": 4},
        {"nombre": "Antofagasta", "lat": -23.6509, "lon": -70.3975, "temperatura": 22, "viento": 18, "uv": 9},
        {"nombre": "Puerto Montt", "lat": -41.4693, "lon": -72.9424, "temperatura": 11, "viento": 30, "uv": 2}
    ]
    
    fig_mapa = renderizar_mapa_multicapa(datos_red_nacional, capa_mapa)
    st.plotly_chart(fig_mapa, width="stretch")

else:
    st.error("No se pudo conectar con la red de telemetría.")