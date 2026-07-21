import streamlit as st
from datetime import datetime
import pytz
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

from telemetry import NODOS_CHILE, obtener_clima_en_vivo, obtener_resumen_red_nodos
from config import aplicar_estilos_base

# Configuración de página ancha para aprovechar toda la pantalla
st.set_page_config(
    page_title="P.I.C.O.S Chile Weather",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Aplicar estilos CSS Glassmorphism
aplicar_estilos_base()

# Refresco dinámico automático cada 30 segundos
st_autorefresh(interval=30000, limit=None, key="clima_refresh")

# --- HEADER SUPERIOR COMPACTO ---
col_head_title, col_head_select = st.columns([2.5, 1])

with col_head_title:
    st.markdown(
        "## ⚡ **P.I.C.O.S** `Chile Weather` &nbsp;<span class='live-badge'></span>"
        "<small style='font-size:0.85rem; color:#38BDF8;'>EN VIVO</small>", 
        unsafe_allow_html=True
    )

with col_head_select:
    ciudad_seleccionada = st.selectbox(
        "📍 Seleccionar Estación:",
        options=list(NODOS_CHILE.keys()),
        index=6,
        label_visibility="collapsed"
    )

nodo_info = NODOS_CHILE[ciudad_seleccionada]

# Consulta de datos en vivo
clima, df_hourly, df_daily = obtener_clima_en_vivo(nodo_info['lat'], nodo_info['lon'])

if clima:
    # Banner de Alerta Dinámica (si aplica)
    if clima['temp'] >= 30:
        st.error(f"🔥 **Alerta Térmica:** {clima['temp']}°C registrados en {ciudad_seleccionada}.")
    elif clima['viento'] >= 30:
        st.warning(f"💨 **Aviso Metereológico:** Viento fuerte de {clima['viento']} km/h.")

    # =========================================================================
    # ESTRUCTURA DE VISTA ÚNICA EN 3 COLUMNAS (TODO VISIBLE A LA VEZ)
    # =========================================================================
    col_izq, col_centro, col_der = st.columns([1.1, 1.4, 1.5])

    # -------------------------------------------------------------------------
    # COLUMNA IZQUIERDA: Hero principal + Tacómetro UV
    # -------------------------------------------------------------------------
    with col_izq:
        # 1. Hero Card Ciudad
        st.markdown(f"""
            <div class="hero-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="hero-city">{ciudad_seleccionada}</div>
                        <small>{nodo_info['region']} • {clima['condicion']}</small>
                        <div class="hero-temp" style="margin-top: 10px;">{clima['temp']}°</div>
                        <small>Sensación: {clima['sensacion']}°C</small>
                    </div>
                    <div style="font-size: 4rem; line-height: 1;">
                        {clima['icono']}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 2. Tacómetro UV
        fig_uv = go.Figure(go.Indicator(
            mode="gauge+number",
            value=clima['uv'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ÍNDICE UV", 'font': {'size': 12, 'color': '#94A3B8'}},
            gauge={
                'axis': {'range': [None, 12], 'tickwidth': 1, 'tickcolor': "#38BDF8"},
                'bar': {'color': "#00F0FF"},
                'bgcolor': "rgba(15, 23, 42, 0.6)",
                'borderwidth': 1,
                'bordercolor': "#1E293B",
                'steps': [
                    {'range': [0, 3], 'color': 'rgba(16, 185, 129, 0.2)'},
                    {'range': [3, 6], 'color': 'rgba(245, 158, 11, 0.2)'},
                    {'range': [6, 12], 'color': 'rgba(239, 68, 68, 0.2)'}
                ],
            }
        ))
        fig_uv.update_layout(
            height=170, 
            margin=dict(l=10, r=10, t=25, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#F8FAFC")
        )
        st.plotly_chart(fig_uv, use_container_width="stretch")

    # -------------------------------------------------------------------------
    # COLUMNA CENTRO: Grid de Métricas + Tendencia 24 Horas
    # -------------------------------------------------------------------------
    with col_centro:
        # 1. Grid 2x2 de métricas rápidas
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-title">💧 Humedad</div>
                    <div class="metric-num">{clima['humedad']}%</div>
                </div>
                <div class="glass-card">
                    <div class="metric-title">💨 Viento</div>
                    <div class="metric-num">{clima['viento']} <small style="font-size:0.8rem;">km/h</small></div>
                </div>
            """, unsafe_allow_html=True)
        with c_m2:
            st.markdown(f"""
                <div class="glass-card">
                    <div class="metric-title">👁️ Visibilidad</div>
                    <div class="metric-num">{clima['visibilidad']} <small style="font-size:0.8rem;">km</small></div>
                </div>
                <div class="glass-card">
                    <div class="metric-title">⏲️ Presión</div>
                    <div class="metric-num">{int(clima['presion'])} <small style="font-size:0.8rem;">hPa</small></div>
                </div>
            """, unsafe_allow_html=True)

        # 2. Gráfico de Tendencia 24H
        if df_hourly is not None:
            fig_quick = go.Figure()
            fig_quick.add_trace(go.Scatter(
                x=df_hourly["Hora"], y=df_hourly["Temperatura (°C)"],
                mode='lines', line=dict(shape='spline', color='#00F0FF', width=3),
                fill='tozeroy', fillcolor='rgba(0, 240, 255, 0.08)',
                name="Temp (°C)"
            ))
            fig_quick.update_layout(
                title=dict(text="Tendencia 24H", font=dict(size=13, color="#94A3B8")),
                template="plotly_dark", height=200,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified"
            )
            st.plotly_chart(fig_quick, use_container_width="stretch")

    # -------------------------------------------------------------------------
    # COLUMNA DERECHA: Mapa Zonal en Vivo + Pronóstico 7 Días
    # -------------------------------------------------------------------------
    with col_der:
        # 1. Mapa de Red Territorial
        df_mapa = obtener_resumen_red_nodos()
        if df_mapa is not None and not df_mapa.empty:
            df_mapa["Tamaño_Nodo"] = df_mapa["Temp"].apply(lambda t: float(max(t + 20.0, 5.0)))
            
            fig_map = px.scatter_map(
                df_mapa, lat="lat", lon="lon", text="Etiqueta",
                color="Temp", size="Tamaño_Nodo", size_max=14,
                color_continuous_scale="Plasma", zoom=3.8,
                center={"lat": -35.0, "lon": -71.5},
                hover_name="Ciudad",
                hover_data={"Región": True, "Temp": ":.1f °C", "Humedad": ":.0f %", "Condicion": True, "Tamaño_Nodo": False, "lat": False, "lon": False},
                map_style="carto-darkmatter"
            )
            fig_map.update_layout(
                height=260, margin={"r":0, "t":0, "l":0, "b":0},
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_map, use_container_width="stretch")

        # 2. Pronóstico semanal horizontal
        if df_daily is not None:
            st.markdown("<small style='color:#94A3B8; font-weight:600;'>PRONÓSTICO 7 DÍAS</small>", unsafe_allow_html=True)
            cols_d = st.columns(min(len(df_daily), 7))
            for i, row in df_daily.head(7).iterrows():
                with cols_d[i]:
                    st.markdown(f"""
                        <div class="glass-card" style="text-align: center; padding: 8px 4px; margin-bottom: 0;">
                            <small style="font-size: 0.7rem;">{row['Fecha'].strftime('%a')}</small>
                            <div style="font-size:1rem; font-weight:bold; color:#38BDF8; margin: 2px 0;">{int(row['Max'])}°</div>
                            <small style="color:#94A3B8; font-size: 0.7rem;">{int(row['Min'])}°</small>
                        </div>
                    """, unsafe_allow_html=True)

else:
    st.info("Sincronizando con la red de sensores...")