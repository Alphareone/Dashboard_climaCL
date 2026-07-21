import streamlit as st
import plotly.express as px
import pandas as pd

def renderizar_alertas(alertas):
    """Muestra la sección de IA & Detección de Anomalías"""
    st.markdown("### 🤖 Detección de Anomalías e IA Predictiva")
    for al in alertas:
        if al["nivel"] == "error":
            st.error(al["msg"])
        elif al["nivel"] == "warning":
            st.warning(al["msg"])
        elif al["nivel"] == "info":
            st.info(al["msg"])
        else:
            st.success(al["msg"])

def renderizar_tarjetas_adaptativas(curr_data, modo):
    """Renderiza métricas según el perfil seleccionado (Ciudadano vs Agro vs Riesgo)"""
    col1, col2, col3, col4 = st.columns(4)

    if modo == "🏃 Ciudadano / Deporte":
        with col1:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Temperatura</div>
                <div class="metric-num">{curr_data.get("temperature_2m", "N/A")}°C</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Índice UV</div>
                <div class="metric-num">{curr_data.get("uv_index", "N/A")}</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Humedad</div>
                <div class="metric-num">{curr_data.get("relative_humidity_2m", "N/A")}%</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Sensación Térmica</div>
                <div class="metric-num">{curr_data.get("apparent_temperature", "N/A")}°C</div>
            </div>''', unsafe_allow_html=True)

    elif modo == "🌾 Agrícola / Industria":
        with col1:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Evapotranspiración</div>
                <div class="metric-num">{curr_data.get("et0_fao_evapotranspiration", "N/A")} mm</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Temp. Aire</div>
                <div class="metric-num">{curr_data.get("temperature_2m", "N/A")}°C</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Precipitación</div>
                <div class="metric-num">{curr_data.get("precipitation", 0)} mm</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Velocidad Viento</div>
                <div class="metric-num">{curr_data.get("wind_speed_10m", "N/A")} km/h</div>
            </div>''', unsafe_allow_html=True)

    else: # Modo Prevención / Riesgo
        with col1:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Rachas Viento</div>
                <div class="metric-num">{curr_data.get("wind_speed_10m", "N/A")} km/h</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Dirección Viento</div>
                <div class="metric-num">{curr_data.get("wind_direction_10m", "N/A")}°</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Precipitación Activa</div>
                <div class="metric-num">{curr_data.get("precipitation", 0)} mm</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">Índice Máx UV</div>
                <div class="metric-num">{curr_data.get("uv_index", "N/A")}</div>
            </div>''', unsafe_allow_html=True)

def renderizar_mapa_multicapa(ciudades_data, capa_seleccionada):
    """Renderiza mapa interactivo cambiando la variable analizada"""
    df = pd.DataFrame(ciudades_data)
    
    # Mapeo de capa a columna
    mapa_cols = {
        "🌡️ Temperatura (°C)": "temperatura",
        "💨 Velocidad del Viento (km/h)": "viento",
        "☀️ Radiación / Índice UV": "uv"
    }
    col_activa = mapa_cols.get(capa_seleccionada, "temperatura")
    
    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        size=col_activa,
        color=col_activa,
        hover_name="nombre",
        color_continuous_scale="Plasma" if col_activa == "uv" else "Viridis",
        zoom=4.2,
        center={"lat": -35.6751, "lon": -71.5430}
    )
    fig.update_layout(
        map_style="carto-darkmatter",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig