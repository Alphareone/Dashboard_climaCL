import streamlit as st
import plotly.express as px
import pandas as pd

# DICCIONARIO DE ÍCONOS SVG ESTILIZADOS
ICONS = {
    "temp": '<svg class="icon-svg icon-pulse" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
    "uv": '<svg class="icon-svg icon-float" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FACC15" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    "wind": '<svg class="icon-svg icon-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
    "humidity": '<svg class="icon-svg icon-float" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    "rain": '<svg class="icon-svg icon-pulse" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M16 13v8M8 13v8M12 15v8M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/></svg>',
    "bot": '<svg class="icon-svg icon-pulse" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4M8 16h.01M16 16h.01"/></svg>'
}

def renderizar_alertas(alertas):
    """Muestra alertas inteligentes con ícono animado"""
    st.markdown(f"### {ICONS['bot']} Detección de Anomalías e IA Predictiva", unsafe_allow_html=True)
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
    """Tarjetas con SVG vectoriales estilizados"""
    col1, col2, col3, col4 = st.columns(4)

    if modo == "🏃 Ciudadano / Deporte":
        with col1:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["temp"]} Temperatura</div>
                <div class="metric-num">{curr_data.get("temperature_2m", "N/A")}°C</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["uv"]} Índice UV</div>
                <div class="metric-num">{curr_data.get("uv_index", "N/A")}</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["humidity"]} Humedad</div>
                <div class="metric-num">{curr_data.get("relative_humidity_2m", "N/A")}%</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["temp"]} Sensación Térmica</div>
                <div class="metric-num">{curr_data.get("apparent_temperature", "N/A")}°C</div>
            </div>''', unsafe_allow_html=True)

    elif modo == "🌾 Agrícola / Industria":
        with col1:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["rain"]} Evapotranspiración</div>
                <div class="metric-num">{curr_data.get("et0_fao_evapotranspiration", "N/A")} mm</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["temp"]} Temp. Aire</div>
                <div class="metric-num">{curr_data.get("temperature_2m", "N/A")}°C</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["rain"]} Precipitación</div>
                <div class="metric-num">{curr_data.get("precipitation", 0)} mm</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["wind"]} Vel. Viento</div>
                <div class="metric-num">{curr_data.get("wind_speed_10m", "N/A")} km/h</div>
            </div>''', unsafe_allow_html=True)

    else: # Modo Prevención
        with col1:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["wind"]} Rachas Viento</div>
                <div class="metric-num">{curr_data.get("wind_speed_10m", "N/A")} km/h</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["wind"]} Dirección Viento</div>
                <div class="metric-num">{curr_data.get("wind_direction_10m", "N/A")}°</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["rain"]} Precipitación</div>
                <div class="metric-num">{curr_data.get("precipitation", 0)} mm</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="glass-card">
                <div class="metric-title">{ICONS["uv"]} Índice Máx UV</div>
                <div class="metric-num">{curr_data.get("uv_index", "N/A")}</div>
            </div>''', unsafe_allow_html=True)

def renderizar_mapa_multicapa(ciudades_data, capa_seleccionada):
    """Renderiza el mapa con zoom acotado a Chile"""
    df = pd.DataFrame(ciudades_data)
    
    mapa_cols = {
        "Temperatura (°C)": "temperatura",
        "Velocidad del Viento (km/h)": "viento",
        "Radiación / Índice UV": "uv"
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
        zoom=4.3,
        center={"lat": -36.5, "lon": -71.5}
    )

    # RESTRICCIÓN DE NAVEGACIÓN Y ZOOM (Límites de Chile)
    fig.update_layout(
        map_style="carto-darkmatter",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        map=dict(
            bounds=dict(
                west=-78.0,  # Océano Pacífico
                east=-65.0,  # Línea Andina
                south=-56.0, # Cabo de Hornos
                north=-17.0  # Arica
            )
        )
    )
    return fig