import streamlit as st

st.set_page_config(page_title="P.I.C.O.S Chile Weather", page_icon="⚡", layout="wide")

from config import aplicar_estilos_base
from telemetry import obtener_datos_clima, generar_alertas_inteligentes
from components import (
    renderizar_banner_alerta,
    renderizar_grafico_google_style,
    renderizar_pronostico_7dias,
    renderizar_mapa_multicapa
)

aplicar_estilos_base()

# --- SIDEBAR ---
st.sidebar.title("⚡ P.I.C.O.S Weather")
st.sidebar.markdown("---")

ciudades = {
    "Quilpué / Marga Marga": (-33.0472, -71.4427),
    "Valparaíso / Viña del Mar": (-33.0472, -71.6127),
    "Santiago Central": (-33.4489, -70.6693),
    "Concepción": (-36.8201, -73.0444),
    "Antofagasta": (-23.6509, -70.3975),
    "La Serena": (-29.9027, -71.2519),
    "Temuco": (-38.7359, -72.5904),
    "Puerto Montt": (-41.4693, -72.9424),
    "Punta Arenas": (-53.1638, -70.9171)
}

ciudad_sel = st.sidebar.selectbox("📍 Comuna / Zona en Monitoreo", list(ciudades.keys()))
lat, lon = ciudades[ciudad_sel]

st.sidebar.markdown("---")
auto_refresh = st.sidebar.checkbox("🔄 Refresco Continuo (En Vivo)", value=True)
if auto_refresh:
    st.sidebar.caption("Monitoreando estación cada 60s")

capa_mapa = st.sidebar.selectbox("🗺️ Capa Geoespacial", ["Temperatura (°C)", "Velocidad del Viento (km/h)", "Radiación / Índice UV"])

# --- DATOS EN TIEMPO REAL ---
datos_clima = obtener_datos_clima(lat, lon)

if datos_clima and "current" in datos_clima:
    curr = datos_clima["current"]
    
    # 1. Banners de Alerta estilo Google Weather
    alertas = generar_alertas_inteligentes(datos_clima, ciudad_sel)
    renderizar_banner_alerta(alertas)

    # 2. Hero Card Principal
    st.markdown(f'''
        <div class="hero-card">
            <span class="live-badge"></span> <small>MONITOREO EN TIEMPO REAL — {ciudad_sel.upper()}</small>
            <div class="hero-city">{ciudad_sel}, Chile</div>
            <div class="hero-temp">{int(curr.get("temperature_2m", 0))}°C</div>
            <div style="opacity: 0.9; margin-top: 6px; font-size: 0.95rem;">
                Humedad: {curr.get("relative_humidity_2m")}% &nbsp;|&nbsp; Viento: {curr.get("wind_speed_10m")} km/h &nbsp;|&nbsp; Prec: {curr.get("precipitation", 0)} mm
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 3. Gráfico estilo Google por Horas (Temperatura / Precipitaciones / Viento)
    st.markdown("### 📈 Tendencia Continuada (Próximas 24 Horas)")
    pestana = st.radio("Ver variable:", ["Temperatura", "Precipitaciones", "Viento"], horizontal=True)
    
    if "hourly" in datos_clima:
        fig_google = renderizar_grafico_google_style(datos_clima["hourly"], pestana)
        st.plotly_chart(fig_google, width="stretch")

    st.markdown("---")

    # 4. Pronóstico Semanal (7 Días)
    if "daily" in datos_clima:
        renderizar_pronostico_7dias(datos_clima["daily"])

    st.markdown("---")

    # 5. Mapa Geoespacial Chileno
    st.markdown(f"### 🗺️ Monitoreo Geoespacial Nacional")
    datos_red_nacional = [
        {"nombre": "Quilpué", "lat": -33.0472, "lon": -71.4427, "temperatura": curr.get("temperature_2m", 12), "viento": curr.get("wind_speed_10m", 13), "uv": curr.get("uv_index", 3)},
        {"nombre": "Santiago", "lat": -33.4489, "lon": -70.6693, "temperatura": 14, "viento": 10, "uv": 4},
        {"nombre": "Concepción", "lat": -36.8201, "lon": -73.0444, "temperatura": 11, "viento": 22, "uv": 2},
        {"nombre": "Antofagasta", "lat": -23.6509, "lon": -70.3975, "temperatura": 18, "viento": 15, "uv": 7},
        {"nombre": "Puerto Montt", "lat": -41.4693, "lon": -72.9424, "temperatura": 9, "viento": 28, "uv": 1}
    ]
    fig_mapa = renderizar_mapa_multicapa(datos_red_nacional, capa_mapa)
    st.plotly_chart(fig_mapa, width="stretch")

else:
    st.error("No se pudo conectar a la red telemétrica.")