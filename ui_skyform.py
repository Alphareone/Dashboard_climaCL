import folium
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium
from config import aplicar_estilos_base


def generar_reloj_javascript():
    """Reloj en vivo dinámico cliente-servidor (avanza segundo a segundo)."""
    html_reloj = """
    <div id="live-clock-container" style="text-align: right; font-family: monospace;">
        <span id="live-clock" style="
            background: rgba(15, 23, 42, 0.85); 
            border: 1px solid rgba(56, 189, 248, 0.4); 
            color: #38bdf8; 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-size: 0.9rem; 
            font-weight: 700;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
        ">• --:--:--</span>
    </div>

    <script>
    function actualizarReloj() {
        const ahora = new Date();
        const horas = String(ahora.getHours()).padStart(2, '0');
        const minutos = String(ahora.getMinutes()).padStart(2, '0');
        const segundos = String(ahora.getSeconds()).padStart(2, '0');
        document.getElementById('live-clock').innerText = "• " + horas + ":" + minutos + ":" + segundos;
    }
    actualizarReloj();
    setInterval(actualizarReloj, 1000);
    </script>
    """
    components.html(html_reloj, height=40)


def generar_svg_icono(tipo, size=48):
    styles = """<style>
    @keyframes spin-slow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes float-cloud { 0%, 100% { transform: translateX(0px); } 50% { transform: translateX(4px); } }
    @keyframes drop-pulse { 0%, 100% { opacity: 0.3; transform: translateY(0); } 50% { opacity: 1; transform: translateY(3px); } }
    .svg-sun { transform-origin: center; animation: spin-slow 12s linear infinite; }
    .svg-cloud { animation: float-cloud 4s ease-in-out infinite; }
    .svg-drop { animation: drop-pulse 1.2s ease-in-out infinite; }
    </style>"""
    
    iconos = {
        "sun": f'{styles}<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><circle cx="32" cy="32" r="14" fill="#38BDF8"/><g class="svg-sun" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"><line x1="32" y1="6" x2="32" y2="12"/><line x1="32" y1="52" x2="32" y2="58"/><line x1="6" y1="32" x2="12" y2="32"/><line x1="52" y1="32" x2="58" y2="32"/></g></svg>',
        "sun_cloud": f'{styles}<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><circle cx="24" cy="24" r="10" fill="#38BDF8" class="svg-sun"/><path class="svg-cloud" d="M20 48h24a10 10 0 0 0 0-20 10.5 10.5 0 0 0-8-3.5 12 12 0 0 0-21 6.5A10 10 0 0 0 20 48z" fill="#94A3B8"/></svg>',
        "cloud": f'{styles}<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><path class="svg-cloud" d="M16 44h32a12 12 0 0 0 0-24 13 13 0 0 0-10-4.5 14 14 0 0 0-25 7.5A12 12 0 0 0 16 44z" fill="#E2E8F0"/></svg>',
        "rain": f'{styles}<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><path class="svg-cloud" d="M14 36h32a10 10 0 0 0 0-20 11 11 0 0 0-8-3.5 12 12 0 0 0-22 6.5A10 10 0 0 0 14 36z" fill="#38BDF8"/><line class="svg-drop" x1="22" y1="42" x2="18" y2="52" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/><line class="svg-drop" x1="32" y1="42" x2="28" y2="52" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/><line class="svg-drop" x1="42" y1="42" x2="38" y2="52" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/></svg>',
    }
    return iconos.get(tipo, iconos["cloud"])


def aplicar_estilos_skyform():
    st.markdown("""<style>
    .hero-card { background: linear-gradient(135deg, rgba(14, 116, 144, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 20px; padding: 22px; }
    .badge-ahora { background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; }
    .temp-main { font-size: 3.5rem; font-weight: 800; line-height: 1; color: #ffffff; }
    .metric-title { color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #f3f4f6; font-size: 1.25rem; font-weight: 700; }
    .progress-bar-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 6px; width: 100%; overflow: hidden; margin-top: 6px; }
    .progress-bar-fill { background: #38bdf8; height: 100%; border-radius: 10px; }
    </style>""", unsafe_allow_html=True)


def render_skyform(datos):
    st_autorefresh(interval=30 * 60 * 1000, limit=None, key="skyform_30min_refresh")

    if not datos:
        st.warning("No hay información meteorológica disponible.")
        return

    act = datos["actual"]
    dia = datos["diario"]
    aq = datos["calidad_aire"]
    df_h = datos["df_hourly"]
    df_d = datos["df_daily"]

    # 🌟 APLICAR FONDO DINÁMICO COMPLETO (SITUACIÓN Y CICLO SOLAR)
    aplicar_estilos_base(tipo_icono=act.get("tipo_icono", "sun"), es_dia=act.get("es_dia", 1))
    aplicar_estilos_skyform()

    # Header principal
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("### Plataforma Integrada de Control y Observación Sensorial")
        st.caption(f"{datos['timestamp']} • {datos['ciudad']}, {datos['region']}")
    with col_h2:
        generar_reloj_javascript()

    st.markdown("<br>", unsafe_allow_html=True)

    # Bento Box Grid
    col1, col2, col3 = st.columns([2.2, 2, 2])

    # COLUMNA 1: Tarjeta Principal
    with col1:
        svg_icon = generar_svg_icono(act["tipo_icono"], size=56)
        st.markdown(
            f'<div class="hero-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: center;"><span class="badge-ahora">AHORA</span><div>{svg_icon}</div></div>'
            f'<h2 style="margin-top: 10px; margin-bottom: 0px; font-weight: 700; color: white;">{datos["ciudad"]}</h2>'
            f'<div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 12px;">{act["condicion"]}</div>'
            f'<div style="display: flex; align-items: baseline; gap: 12px;"><span class="temp-main">{act["temperatura"]}°</span><span style="color: #94a3b8;">Máx: {dia["temp_max"]}° / Mín: {dia["temp_min"]}°</span></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if not df_h.empty:
            df_24h = df_h.head(24)
            fig_spark = go.Figure()
            fig_spark.add_trace(go.Scatter(
                x=df_24h["time"],
                y=df_24h["temperature_2m"],
                mode='lines',
                line=dict(color='#38bdf8', width=2),
                fill='tozeroy',
                fillcolor='rgba(56, 189, 248, 0.08)'
            ))
            fig_spark.update_layout(
                height=110,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, visible=True, tickformat="%H:%00", tickfont=dict(color="#64748b", size=9)),
                yaxis=dict(showgrid=False, visible=False)
            )
            st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

    # COLUMNA 2: Indicadores
    with col2:
        st.markdown(
            f'<div class="glass-card">'
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">'
            f'<div><div class="metric-title">HUMEDAD</div><div class="metric-value">{act["humedad"]}%</div></div>'
            f'<div><div class="metric-title">ÍNDICE UV</div><div class="metric-value">{dia["uv_max"]}</div></div>'
            f'<div><div class="metric-title">VIENTO</div><div class="metric-value">{act["viento_velocidad"]} km/h</div></div>'
            f'<div><div class="metric-title">VISIBILIDAD</div><div class="metric-value">{act["visibilidad_km"]} km</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        prob_lluvia = act['probabilidad_lluvia']
        st.markdown(
            f'<div class="glass-card">'
            f'<div class="metric-title" style="margin-bottom: 10px;">PRECIPITACIÓN & DINÁMICA DE VIENTO</div>'
            f'<div style="margin-bottom: 12px;">'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.8rem;"><span>Probabilidad Lluvia</span><span style="color: #38bdf8; font-weight: 600;">{prob_lluvia}%</span></div>'
            f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {prob_lluvia}%;"></div></div>'
            f'</div>'
            f'<div style="margin-bottom: 12px;">'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.8rem;"><span>Ráfagas de Viento</span><span style="color: #38bdf8; font-weight: 600;">{act["viento_rafagas"]} km/h</span></div>'
            f'</div>'
            f'<div>'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.8rem;"><span>Presión Barométrica</span><span style="color: #4ade80; font-weight: 600;">{act["presion"]} hPa</span></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # COLUMNA 3: Sol, Calidad del Aire y Mapa
    with col3:
        salida = dia['salida_sol'].split('T')[-1] if dia['salida_sol'] else '07:00'
        puesta = dia['puesta_sol'].split('T')[-1] if dia['puesta_sol'] else '18:00'

        st.markdown(
            f'<div class="glass-card">'
            f'<div class="metric-title" style="margin-bottom: 8px;">CICLO SOLAR Y CALIDAD DEL AIRE</div>'
            f'<svg width="100%" height="45" viewBox="0 0 200 50" style="overflow: visible;">'
            f'<path d="M 10 45 Q 100 0 190 45" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2" stroke-dasharray="4 4"/>'
            f'<circle cx="150" cy="18" r="5" fill="#f59e0b"/>'
            f'</svg>'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #9ca3af; margin-top: -6px;">'
            f'<span>Amanecer: <b>{salida}</b></span><span>Atardecer: <b>{puesta}</b></span>'
            f'</div>'
            f'<hr style="border-color: rgba(255,255,255,0.08); margin: 10px 0;">'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.8rem;">'
            f'<span>AQI: <b style="color: #4ade80;">{aq["aqi"]}</b></span><span>PM2.5: <b>{aq["pm2_5"]} µg/m³</b></span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="metric-title" style="margin-bottom: 6px;">UBICACIÓN ESTACIÓN SENSORIAL</div>', unsafe_allow_html=True)

        m = folium.Map(
            location=[datos['lat'], datos['lon']],
            zoom_start=12,
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="CartoDB",
            zoom_control=False
        )
        folium.CircleMarker(
            location=[datos['lat'], datos['lon']],
            radius=6,
            color="#38bdf8",
            fill=True,
            fill_color="#38bdf8",
            fill_opacity=0.9,
            popup=f"Estación Telemetría - {datos['ciudad']}"
        ).add_to(m)

        st_folium(m, height=125, use_container_width=True)

    # PRONÓSTICO 7 DÍAS
    if not df_d.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="metric-title" style="margin-bottom: 12px;">PRONÓSTICO 7 DÍAS</div>', unsafe_allow_html=True)

        cols_dias = st.columns(min(7, len(df_d)))
        dias_nombre = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        for idx, col in enumerate(cols_dias):
            if idx < len(df_d):
                row = df_d.iloc[idx]
                fecha_dt = pd.to_datetime(row['time'])
                nombre_dia = dias_nombre[fecha_dt.weekday()]
                max_t = round(row['temperature_2m_max'])
                min_t = round(row['temperature_2m_min'])

                with col:
                    st.markdown(
                        f'<div class="glass-card" style="text-align: center; padding: 12px 6px;">'
                        f'<div style="font-size: 0.8rem; font-weight: 600; color: #9ca3af;">{nombre_dia}</div>'
                        f'<div style="margin: 8px 0;">{generar_svg_icono("sun_cloud", size=28)}</div>'
                        f'<div style="font-weight: 700; font-size: 1rem; color: white;">{max_t}°</div>'
                        f'<div style="font-size: 0.75rem; color: #64748b;">{min_t}°</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )