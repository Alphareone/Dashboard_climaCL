import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# Importaciones correctas de tus módulos locales
from config import load_css
from telemetry import NODOS_CHILE, cargar_telemetria_real, calcular_indices_operativos
from components import (
    render_header, 
    render_chart_historico,
    render_mapa_3d_chile,
    generar_html_reporte_pdf,
    SVG_ICONS
)

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="F.U.I.S.T.E. B.U.E.N.O. - Telemetría Climática", 
    page_icon="⚡", 
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. AUTO-REFRESCO CADA 500 MS (Reloj continuo en vivo sin saltos)
# -----------------------------------------------------------------------------
st_autorefresh(interval=500, limit=None, key="fuiste_clock_refresh")

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL TÁCTICA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:8px; font-family:Orbitron; font-size: 0.85rem; font-weight:800; letter-spacing:1px; color:#00F0FF; margin-bottom:12px;'>
            {SVG_ICONS['grid']} <span>CONSOLA F.U.I.S.T.E. v2.0</span>
        </div>
    """, unsafe_allow_html=True)
    
    modulo_seleccionado = st.radio(
        "SELECCIONAR MÓDULO:",
        options=[
            "[LIVE] Telemetría en Vivo",
            "[EVAL] Análisis de Riesgos Estacionales",
            "[STREAM] Consola de Datos JSON",
            "[REPORT] Exportar Informe Técnico"
        ],
        index=0
    )

    st.markdown("---")
    
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:8px; font-family:Orbitron; font-size: 0.85rem; font-weight:800; letter-spacing:1px; color:#00FF66; margin-bottom:12px;'>
            {SVG_ICONS['map']} <span>RED DE NODOS CHILE</span>
        </div>
    """, unsafe_allow_html=True)
    
    zona_seleccionada = st.selectbox(
        "SELECCIONAR NODO:",
        options=list(NODOS_CHILE.keys()),
        index=5 # Valparaíso / Viña por defecto
    )

    info_nodo = NODOS_CHILE[zona_seleccionada]

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.78rem;">
        <div><strong>REGIÓN:</strong> {info_nodo['region']}</div>
        <div><strong>LAT:</strong> {info_nodo['lat']} | <strong>LON:</strong> {info_nodo['lon']}</div>
        <div style="margin-top:6px; display:flex; align-items:center; gap:6px;">
            <span class="live-dot" style="width:6px; height:6px;"></span>
            <strong style="color:#00FF66;">STREAMING SATELITAL OK</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    theme_mode = st.radio(
        "APARIENCIA UI:",
        options=["Oscuro Cyberpunk", "Claro Futurista"],
        index=0
    )

# -----------------------------------------------------------------------------
# 4. CARGA DE ESTILOS Y DATOS EN REAL-TIME
# -----------------------------------------------------------------------------
load_css(theme_mode)

# Llamada a las funciones REALES de telemetry.py
data, df_hourly = cargar_telemetria_real(info_nodo["lat"], info_nodo["lon"])
indices = calcular_indices_operativos(data['Temp'], data['Humedad'], data['Viento'], data['UV'])

# Encabezado con hora en vivo
render_header("America/Santiago", zona_seleccionada, theme_mode)

# -----------------------------------------------------------------------------
# 5. RENDERIZADO DE MÓDULOS
# -----------------------------------------------------------------------------

if "[LIVE]" in modulo_seleccionado:
    col_left, col_right = st.columns([5.5, 4.5])

    with col_left:
        m1, m2, m3 = st.columns(3)
        
        with m1:
            st.markdown(f"""
                <div class="cyber-panel">
                    <div class="panel-tag">
                        <span>F.U.I.S.T.E. TEMP</span>
                        <span style="color:#00F0FF;">REAL API</span>
                    </div>
                    <div class="metric-big" style="color: #00F0FF;">
                        {data['Temp']}<span class="unit-label">°C</span>
                    </div>
                    <div class="sub-status" style="color:#00FF66;">
                        <span>ST: {data['Sensacion']}°C</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
                <div class="cyber-panel-green">
                    <div class="panel-tag panel-tag-green">
                        <span>HUMEDAD</span>
                        <span style="color:#00FF66;">ACTIVA</span>
                    </div>
                    <div class="metric-big" style="color: #00FF66;">
                        {data['Humedad']}<span class="unit-label">%</span>
                    </div>
                    <div class="sub-status" style="color:#00F0FF;">
                        <span>ROCÍO: {indices['PuntoRocio']}°C</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
                <div class="cyber-panel">
                    <div class="panel-tag">
                        <span>VIENTO & BARO</span>
                        <span style="color:#FF0055;">VECTOR</span>
                    </div>
                    <div class="metric-big" style="color: #FF0055;">
                        {data['Viento']}<span class="unit-label">km/h</span>
                    </div>
                    <div class="sub-status" style="color:#E2E8F0;">
                        <span>PRES: {data['Presion']} hPa</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="cyber-panel" style="margin-top: 4px;">
                <div class="panel-tag">
                    <span style="display:flex; align-items:center; gap:6px;">
                        {SVG_ICONS['activity']} [ PRONÓSTICO Y CURVA REAL DE 24 HORAS ]
                    </span>
                    <span style="opacity: 0.6;">OPEN-METEO FEED</span>
                </div>
        """, unsafe_allow_html=True)
        render_chart_historico(df_hourly, theme_mode)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
            <div class="cyber-panel">
                <div class="panel-tag">
                    <span style="display:flex; align-items:center; gap:6px;">
                        {SVG_ICONS['radar']} [ UBICACIÓN DEL NODO // CHILE ]
                    </span>
                    <span style="color:#FF0055;">● RASTER LOCKED</span>
                </div>
        """, unsafe_allow_html=True)
        render_mapa_3d_chile(NODOS_CHILE, zona_seleccionada, theme_mode)
        st.markdown('</div>', unsafe_allow_html=True)

elif "[EVAL]" in modulo_seleccionado:
    st.markdown(f"""
        <div class="cyber-panel">
            <div class="panel-tag">
                <span style="display:flex; align-items:center; gap:6px;">
                    {SVG_ICONS['shield']} MÓDULO F.U.I.S.T.E. DE EVALUACIÓN DE RIESGOS
                </span>
                <span style="color:{indices['ColorIncendio']}">{indices['RiesgoIncendio']}</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1);">
                    <h4 style="color:#FF0055; margin-top:0;">🔥 ALERTA DE INCENDIOS FORESTALES</h4>
                    <p style="font-size: 0.9rem;">Índice Operativo: <strong>{indices['RiesgoIncendio']}</strong></p>
                    <p style="font-size: 0.8rem; opacity:0.8;">Calculado por brecha de rocío ({indices['PuntoRocio']}°C) y viento ({data['Viento']} km/h).</p>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1);">
                    <h4 style="color:#00F0FF; margin-top:0;">❄️ ANÁLISIS AGROCLIMÁTICO</h4>
                    <p style="font-size: 0.9rem;">Riesgo Helada: <strong style="color:{indices['ColorHelada']};">{indices['RiesgoHelada']}</strong></p>
                    <p style="font-size: 0.8rem; opacity:0.8;">Radiación UV: <strong>{data['UV']}</strong> | Precipitación: <strong>{data['Precip']} mm</strong></p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif "[STREAM]" in modulo_seleccionado:
    st.markdown(f"""
        <div class="cyber-panel">
            <div class="panel-tag">
                <span>[ CONSOLA DE STREAMING RAW DATA // JSON FEED ]</span>
                <span style="color:#00FF66;">● ENGINE F.U.I.S.T.E. OK</span>
            </div>
    """, unsafe_allow_html=True)
    st.json({
        "sistema": "F.U.I.S.T.E. B.U.E.N.O. Engine",
        "nodo_activo": zona_seleccionada,
        "coordenadas": {"lat": info_nodo["lat"], "lon": info_nodo["lon"]},
        "timestamp_utc": pd.Timestamp.now().isoformat(),
        "telemetria_raw": data,
        "indices_calculados": indices
    })
    st.markdown('</div>', unsafe_allow_html=True)

elif "[REPORT]" in modulo_seleccionado:
    st.markdown(f"""
        <div class="cyber-panel" style="text-align: center; padding: 30px;">
            <h3 style="color:#00F0FF; font-family:'Orbitron';">INFORME TÉCNICO F.U.I.S.T.E. B.U.E.N.O.</h3>
            <p style="font-size: 0.9rem; opacity:0.8;">Descarga la ficha oficial de monitoreo de {zona_seleccionada}.</p>
    """, unsafe_allow_html=True)
    
    html_reporte = generar_html_reporte_pdf(zona_seleccionada, data, indices)
    
    st.download_button(
        label="📄 DESCARGAR INFORME OFICIAL (HTML/PDF)",
        data=html_reporte,
        file_name=f"Reporte_FUISTE_BUENO_{zona_seleccionada.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)