import streamlit as st
from telemetry import TERRITORIO_CHILE, obtener_telemetria_completa
from components import (
    aplicar_estilos_skyform_dinamico,
    renderizer_reloj_tiempo_real,
    renderizar_hero_card,
    renderizar_grafico_tendencia,
    renderizar_condiciones_grid,
    renderizar_mapa_integradom,
    renderizar_pronostico_7dias
)

st.set_page_config(
    page_title="Plataforma Integrada de Control y Observación Sensorial",
    page_icon="https://www.rubendario.cl/sitio/wp-content/uploads/2023/03/clima.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR: SELECCIÓN TERRITORIAL ---
st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
            <circle cx="12" cy="10" r="3"/>
        </svg>
        <h3 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 700;">Territorio Chile</h3>
    </div>
    <p style="font-size: 0.72rem; color: #94a3b8; margin-top: 0; margin-bottom: 12px;">Plataforma Integrada de Control y Observación Sensorial</p>
""", unsafe_allow_html=True)

region_sel = st.sidebar.selectbox("Región", list(TERRITORIO_CHILE.keys()), index=5)
comunas_region = TERRITORIO_CHILE[region_sel]
comuna_sel = st.sidebar.selectbox("Comuna / Ciudad", list(comunas_region.keys()), index=0)

coords = comunas_region[comuna_sel]
clima = obtener_telemetria_completa(coords["lat"], coords["lon"], comuna_sel, region_sel)

if clima:
    aplicar_estilos_skyform_dinamico(clima)

    # --- HEADER CON TITULO COMPLETO Y RELOJ ---
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f"""
            <div style="padding-top: 2px;">
                <h3 style="margin:0; font-size: 1.15rem; color: white;">Plataforma Integrada de Control y Observación Sensorial</h3>
                <span style="font-size: 0.75rem; color: #94a3b8;">{clima.get('dia_nombre')} • {clima.get('fecha_actual')} • {comuna_sel}, {region_sel}</span>
            </div>
        """, unsafe_allow_html=True)
    with col_h2:
        renderizer_reloj_tiempo_real()

    st.markdown("<div style='margin-bottom: 0.4rem;'></div>", unsafe_allow_html=True)

    # --- GRILLA BENTO ---
    col_left, col_mid, col_right = st.columns([1.1, 1, 1.2])

    with col_left:
        renderizar_hero_card(clima)
        renderizar_grafico_tendencia(clima)

    with col_mid:
        renderizar_condiciones_grid(clima)
        st.markdown(f"""
            <div class="bento-card">
                <div class="metric-title" style="margin-bottom: 6px;">CICLO SOLAR & AMBIENTAL</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h20"/><path d="M20 18a8 8 0 0 0-16 0"/><path d="m19.07 10.93-1.41 1.41"/></svg>
                        <span>Amanecer: <b>{clima.get('amanecer')}</b></span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 10V2"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h20"/><path d="M20 18a8 8 0 0 0-16 0"/><path d="m19.07 10.93-1.41 1.41"/></svg>
                        <span>Atardecer: <b>{clima.get('atardecer')}</b></span>
                    </div>
                </div>
                <div style="margin-top: 6px; display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 4px;">
                    <span>AQI: <b style="color:#00ff88;">{clima.get('aqi')}</b></span>
                    <span>PM2.5: <b>{clima.get('pm2_5')} µg/m³</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="metric-title" style="margin-bottom: 4px;">UBICACIÓN ESTACIÓN SENSORIAL</div>', unsafe_allow_html=True)
        renderizar_mapa_integradom(coords["lat"], coords["lon"])

    # --- PRONÓSTICO 7 DÍAS ---
    renderizar_pronostico_7dias(clima)

else:
    st.error("Error al obtener la telemetría del territorio seleccionado.")