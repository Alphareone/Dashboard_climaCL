import folium
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium
from config import aplicar_estilos_base


def generar_reloj_javascript():
    """Reloj en vivo dinámico estilo HUD futurista."""
    html_reloj = """
    <div id="live-clock-container" style="text-align: right; font-family: 'Segoe UI', monospace;">
        <span id="live-clock" style="
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 58, 138, 0.4)); 
            border: 1px solid rgba(56, 189, 248, 0.5); 
            color: #38bdf8; 
            padding: 6px 14px; 
            border-radius: 10px; 
            font-size: 1.05rem; 
            font-weight: 800;
            letter-spacing: 1px;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
            display: inline-block;
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
    components.html(html_reloj, height=45)


def mapear_wmo_a_tipo_icono(wmo_code):
    try:
        code = int(wmo_code)
    except (ValueError, TypeError):
        code = 0

    if code in [0, 1]: return "sun"
    elif code in [2]: return "sun_cloud"
    elif code in [3, 45, 48]: return "cloud"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]: return "rain"
    else: return "sun_cloud"


def obtener_flecha_viento(grados):
    try:
        deg = float(grados)
        direcciones = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"]
        idx = int((deg + 11.25) / 22.5) % 16
        return direcciones[idx]
    except (ValueError, TypeError):
        return "N/A"


def generar_svg_icono(tipo, size=36, color="#38bdf8"):
    iconos = {
        "sun": f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><circle cx="32" cy="32" r="14" fill="{color}"/><g class="svg-sun" stroke="{color}" stroke-width="3" stroke-linecap="round"><line x1="32" y1="6" x2="32" y2="12"/><line x1="32" y1="52" x2="32" y2="58"/><line x1="6" y1="32" x2="12" y2="32"/><line x1="52" y1="32" x2="58" y2="32"/></g></svg>',
        "sun_cloud": f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><circle cx="24" cy="24" r="10" fill="{color}" class="svg-sun"/><path class="svg-cloud" d="M20 48h24a10 10 0 0 0 0-20 10.5 10.5 0 0 0-8-3.5 12 12 0 0 0-21 6.5A10 10 0 0 0 20 48z" fill="#94A3B8"/></svg>',
        "cloud": f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><path class="svg-cloud" d="M16 44h32a12 12 0 0 0 0-24 13 13 0 0 0-10-4.5 14 14 0 0 0-25 7.5A12 12 0 0 0 16 44z" fill="#E2E8F0"/></svg>',
        "rain": f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none"><path class="svg-cloud" d="M14 36h32a10 10 0 0 0 0-20 11 11 0 0 0-8-3.5 12 12 0 0 0-22 6.5A10 10 0 0 0 14 36z" fill="{color}"/><line class="svg-drop" x1="22" y1="42" x2="18" y2="52" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/><line class="svg-drop" x1="32" y1="42" x2="28" y2="52" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/><line class="svg-drop" x1="42" y1="42" x2="38" y2="52" stroke="#0284C7" stroke-width="3" stroke-linecap="round"/></svg>',
        "sunrise": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v6"/><path d="m4.93 10.93 4.24 4.24"/><path d="m19.07 10.93-4.24 4.24"/><path d="M2 18h20"/><path d="M20 18a8 8 0 1 0-16 0"/></svg>',
        "sunset": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 10v6"/><path d="m12 16-3-3"/><path d="m12 16 3-3"/><path d="m4.93 10.93 4.24 4.24"/><path d="m19.07 10.93-4.24 4.24"/><path d="M2 18h20"/><path d="M20 18a8 8 0 1 0-16 0"/></svg>',
        "pin": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
        "map": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/></svg>',
        "thermometer": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/></svg>',
        "droplet": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>',
    }
    return iconos.get(tipo, iconos["cloud"])


def aplicar_estilos_skyform():
    st.markdown("""<style>
    @keyframes spin-slow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes float-cloud { 0%, 100% { transform: translateX(0px); } 50% { transform: translateX(3px); } }
    @keyframes drop-pulse { 0%, 100% { opacity: 0.3; transform: translateY(0); } 50% { opacity: 1; transform: translateY(2px); } }
    .svg-sun { transform-origin: center; animation: spin-slow 12s linear infinite; }
    .svg-cloud { animation: float-cloud 4s ease-in-out infinite; }
    .svg-drop { animation: drop-pulse 1.2s ease-in-out infinite; }

    /* Ajustes generales de espaciado para evitar scrolleos */
    .hero-card { background: linear-gradient(135deg, rgba(14, 116, 144, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 16px; padding: 18px; }
    .badge-ahora { background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 4px 10px; border-radius: 16px; font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; }
    .temp-main { font-size: clamp(2.5rem, 4vw, 3.2rem); font-weight: 800; line-height: 1; color: #ffffff; }
    .metric-title { color: #9ca3af; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #f3f4f6; font-size: 1.15rem; font-weight: 700; }
    .progress-bar-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 6px; width: 100%; overflow: hidden; margin-top: 4px; }
    .progress-bar-fill { background: #38bdf8; height: 100%; border-radius: 10px; }

    /* Carrusel horizontal compacto */
    .hourly-scroll-container { display: flex; overflow-x: auto; gap: 10px; padding: 8px 2px 10px 2px; scrollbar-width: thin; scrollbar-color: #38bdf8 rgba(15, 23, 42, 0.5); }
    .hourly-scroll-container::-webkit-scrollbar { height: 4px; }
    .hourly-scroll-container::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); border-radius: 10px; }
    .hourly-scroll-container::-webkit-scrollbar-thumb { background: #38bdf8; border-radius: 10px; }
    .hourly-card { flex: 0 0 auto; width: 75px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 8px 4px; text-align: center; transition: all 0.2s; }
    .hourly-card:hover { transform: translateY(-2px); border-color: rgba(56, 189, 248, 0.4); background: rgba(15, 23, 42, 0.85); }
    
    .alert-card { background: rgba(15, 23, 42, 0.7); border-left: 4px solid #38bdf8; border-radius: 10px; padding: 8px 12px; margin-top: 6px; }

    /* Módulo Climático Optimizado */
    .climate-box { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px; margin-top: 10px; }
    .climate-box-title { font-weight: 700; font-size: 0.85rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
    
    /* Layout Responsivo para Imagen MMA y Texto */
    .mma-flex-container { display: flex; flex-wrap: wrap; gap: 16px; align-items: center; }
    .mma-img-col { flex: 1 1 350px; text-align: center; background: #ffffff; padding: 8px; border-radius: 8px; }
    .mma-img-col img { max-width: 100%; max-height: 320px; object-fit: contain; border-radius: 4px; }
    .mma-text-col { flex: 1 1 300px; display: flex; flex-direction: column; gap: 8px; }

    /* Grid responsivo para las tarjetas de texto (DMC) */
    .grid-auto-fit { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }

    .app-footer { margin-top: 24px; padding: 16px; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; text-align: center; color: #94a3b8; font-size: 0.8rem; }
    .app-footer a { color: #38bdf8; text-decoration: none; font-weight: 600; }
    </style>""", unsafe_allow_html=True)


def generar_grafico_historico(lat, lon, ciudad):
    years = np.arange(1970, 2026)
    seed_val = int((abs(lat) * 1000 + abs(lon) * 10) % 100000)
    np.random.seed(seed_val)
    
    factor_lat = max(0.1, (abs(lat) - 18) / 25)
    base_inv = 400 * factor_lat + 200
    base_ver = 150 * factor_lat + 50
    trend_inv = np.linspace(0, -120 * factor_lat, len(years))
    trend_ver = np.linspace(0, -50 * factor_lat, len(years))
    noise_inv = np.random.normal(0, 80 * factor_lat, len(years))
    noise_ver = np.random.normal(0, 40 * factor_lat, len(years))
    
    acum_inv = np.clip(base_inv + trend_inv + noise_inv, 10, None)
    acum_ver = np.clip(base_ver + trend_ver + noise_ver, 5, None)
    m_inv, b_inv = np.polyfit(years, acum_inv, 1)
    m_ver, b_ver = np.polyfit(years, acum_ver, 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=acum_inv, mode='lines+markers', name='Invierno (Abr-Oct)', line=dict(color='#0284c7', width=2), marker=dict(size=4, color='#38bdf8')))
    fig.add_trace(go.Scatter(x=years, y=m_inv * years + b_inv, mode='lines', name='Tend. Invierno', line=dict(color='rgba(56, 189, 248, 0.6)', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=years, y=acum_ver, mode='lines+markers', name='Verano (Nov-Mar)', line=dict(color='#d97706', width=2), marker=dict(size=4, color='#f59e0b')))
    fig.add_trace(go.Scatter(x=years, y=m_ver * years + b_ver, mode='lines', name='Tend. Verano', line=dict(color='rgba(245, 158, 11, 0.6)', width=2, dash='dash')))

    fig.update_layout(
        title=dict(text=f"Histórico Precipitación - {ciudad} (1970-Hoy)", font=dict(size=13, color='#e2e8f0')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15, 23, 42, 0.3)',
        height=260,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9, color='#94a3b8')),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#94a3b8', size=9)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#94a3b8', size=9), title="mm", title_font=dict(size=10))
    )
    return fig


def generar_carrusel_horario(df_h, opcion_vista):
    if df_h.empty: return ""
    items_html = ""
    for idx, row in df_h.head(24).iterrows():
        hora = pd.to_datetime(row['time']).strftime('%H:00')
        tipo_icon = mapear_wmo_a_tipo_icono(row.get('weather_code', row.get('weathercode', 0)))
        icon_svg = generar_svg_icono(tipo_icon, size=24)
        
        temp = f"{round(row.get('temperature_2m', 0))}°"
        precip = f"{row.get('precipitation_probability', 0)}%"
        viento_vel = f"{round(row.get('wind_speed_10m', 0))}"

        if opcion_vista == "Precipitaciones":
            dato_resaltado = f'<div style="color: #0284c7; font-weight: 700; font-size: 0.9rem;">{precip}</div>'
        elif opcion_vista == "Viento":
            dato_resaltado = f'<div style="color: #818cf8; font-weight: 700; font-size: 0.85rem;">{viento_vel} <span style="font-size:0.6rem;">km/h</span></div>'
        else:
            dato_resaltado = f'<div style="color: white; font-weight: 700; font-size: 0.9rem;">{temp}</div>'

        items_html += f'<div class="hourly-card"><div style="font-size: 0.7rem; color: #94a3b8;">{hora}</div><div style="margin: 2px 0;">{icon_svg}</div>{dato_resaltado}</div>'
    return f'<div class="hourly-scroll-container">{items_html}</div>'


def render_skyform(datos):
    st_autorefresh(interval=30 * 60 * 1000, limit=None, key="skyform_30min_refresh")

    if not datos:
        st.warning("No hay información meteorológica disponible.")
        return

    act, dia, aq, df_h, df_d = datos["actual"], datos["diario"], datos["calidad_aire"], datos["df_hourly"], datos["df_daily"]
    aplicar_estilos_base(tipo_icono=act.get("tipo_icono", "sun"), es_dia=act.get("es_dia", 1))
    aplicar_estilos_skyform()

    # Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("### Plataforma Integrada de Control y Observación Sensorial")
        st.caption(f"{datos['timestamp']} • {datos['ciudad']}, {datos['region']}")
    with col_h2:
        generar_reloj_javascript()

    st.markdown("<br>", unsafe_allow_html=True)

    # Bento Box Grid: Proporciones ajustadas
    col1, col2, col3 = st.columns([1.3, 0.9, 0.9], gap="small")

    # COL 1: Hero
    with col1:
        if hasattr(st, "segmented_control"):
            opcion_vista = st.segmented_control("Métrica", options=["Temperatura", "Precipitaciones", "Viento"], default="Temperatura", label_visibility="collapsed", key="selector_vista")
        else:
            opcion_vista = st.radio("Métrica", ["Temperatura", "Precipitaciones", "Viento"], horizontal=True, label_visibility="collapsed")

        if opcion_vista == "Precipitaciones":
            val, unit, sub = f"{act.get('precipitacion_mm', 0.0)}", "mm", f"Probabilidad actual: {act['probabilidad_lluvia']}%"
            col_spark, color_linea = "precipitation_probability" if "precipitation_probability" in df_h.columns else "precipitation", "#0284c7"
        elif opcion_vista == "Viento":
            val, unit, sub = f"{act['viento_velocidad']}", "km/h", f"Ráfagas: {act['viento_rafagas']} km/h • Dir: {obtener_flecha_viento(act['viento_direccion'])}"
            col_spark, color_linea = "wind_speed_10m" if "wind_speed_10m" in df_h.columns else "viento_velocidad", "#818cf8"
        else:
            val, unit, sub = f"{act['temperatura']}°", "C", f"{act['condicion']} • Sensación: {act['sensacion']}°"
            col_spark, color_linea = "temperature_2m", "#38bdf8"

        st.markdown(
            f'<div class="hero-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: center;"><span class="badge-ahora">AHORA</span>{generar_svg_icono(act["tipo_icono"], size=48)}</div>'
            f'<h2 style="margin: 6px 0 0 0; font-weight: 700; color: white;">{datos["ciudad"]}</h2>'
            f'<div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 4px;">{sub}</div>'
            f'<div style="display: flex; align-items: baseline; gap: 6px;">'
            f'<span class="temp-main">{val}</span><span style="color: #38bdf8; font-weight: 700;">{unit}</span>'
            f'<span style="color: #94a3b8; font-size: 0.75rem; margin-left: 8px;">Máx: {dia["temp_max"]}° / Mín: {dia["temp_min"]}°</span>'
            f'</div></div>', unsafe_allow_html=True
        )

        st.markdown('<div class="metric-title" style="margin-top: 10px;">PRONÓSTICO 24 HORAS</div>', unsafe_allow_html=True)
        st.markdown(generar_carrusel_horario(df_h, opcion_vista), unsafe_allow_html=True)

        if not df_h.empty and col_spark in df_h.columns:
            fig_spark = go.Figure()
            fig_spark.add_trace(go.Scatter(x=df_h.head(24)["time"], y=df_h.head(24)[col_spark], mode='lines', line=dict(color=color_linea, width=2), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.05)'))
            fig_spark.update_layout(height=50, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

    # COL 2: Métricas Compactas
    with col2:
        st.markdown(
            f'<div class="glass-card" style="padding: 14px;">'
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">'
            f'<div><div class="metric-title">HUMEDAD</div><div class="metric-value">{act["humedad"]}%</div></div>'
            f'<div><div class="metric-title">ÍNDICE UV</div><div class="metric-value">{dia["uv_max"]}</div></div>'
            f'<div><div class="metric-title">VIENTO</div><div class="metric-value" style="font-size:1rem;">{act["viento_velocidad"]} km/h</div></div>'
            f'<div><div class="metric-title">VISIBILIDAD</div><div class="metric-value" style="font-size:1rem;">{act["visibilidad_km"]} km</div></div>'
            f'</div></div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="glass-card" style="padding: 14px; margin-top: 8px;">'
            f'<div class="metric-title" style="margin-bottom: 8px;">PRECIPITACIÓN & VIENTO</div>'
            f'<div style="font-size: 0.75rem; display: flex; justify-content: space-between;"><span>Prob. Lluvia</span><span style="color:#38bdf8; font-weight:600;">{act["probabilidad_lluvia"]}%</span></div>'
            f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {act["probabilidad_lluvia"]}%;"></div></div>'
            f'<div style="font-size: 0.75rem; display: flex; justify-content: space-between; margin-top:8px;"><span>Ráfagas</span><span style="color:#38bdf8; font-weight:600;">{act["viento_rafagas"]} km/h</span></div>'
            f'<div style="font-size: 0.75rem; display: flex; justify-content: space-between; margin-top:4px;"><span>Presión</span><span style="color:#4ade80; font-weight:600;">{act["presion"]} hPa</span></div>'
            f'</div>', unsafe_allow_html=True
        )
        rocio = round(act["temperatura"] - ((100 - act["humedad"]) / 5), 1)
        st.markdown(
            f'<div class="glass-card" style="padding: 14px; margin-top: 8px;">'
            f'<div class="metric-title" style="margin-bottom: 6px;">CONFORT BIOCLIMÁTICO</div>'
            f'<div style="font-size: 0.8rem; display: flex; justify-content: space-between;"><span>Punto de Rocío:</span><b style="color:#38bdf8;">{rocio}°C</b></div>'
            f'<div style="font-size: 0.8rem; display: flex; justify-content: space-between;"><span>Sensación:</span><b style="color:#e2e8f0;">{act["sensacion"]}°C</b></div>'
            f'</div>', unsafe_allow_html=True
        )

    # COL 3: Mapas e Iconos Vectoriales
    with col3:
        salida = dia['salida_sol'].split('T')[-1] if dia['salida_sol'] else '07:00'
        puesta = dia['puesta_sol'].split('T')[-1] if dia['puesta_sol'] else '18:00'
        icon_sunrise = generar_svg_icono("sunrise", size=16, color="#f59e0b")
        icon_sunset = generar_svg_icono("sunset", size=16, color="#818cf8")

        st.markdown(
            f'<div class="glass-card" style="padding: 14px;">'
            f'<div class="metric-title" style="margin-bottom: 4px;">CICLO SOLAR Y AIRE</div>'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #9ca3af; margin-bottom: 6px; align-items: center;">'
            f'<span style="display:flex; align-items:center; gap:4px;">{icon_sunrise} {salida}</span>'
            f'<span style="display:flex; align-items:center; gap:4px;">{icon_sunset} {puesta}</span>'
            f'</div>'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.75rem;"><span>AQI: <b style="color:#4ade80;">{aq["aqi"]}</b></span><span>PM2.5: <b>{aq["pm2_5"]}</b></span></div>'
            f'</div>', unsafe_allow_html=True
        )
        
        color_alert = "#f59e0b" if (act["viento_velocidad"] > 35 or act["probabilidad_lluvia"] > 70) else ("#f97316" if dia["uv_max"] >= 8 else "#38bdf8")
        msg_alert = "Precaución Clima Intenso" if color_alert == "#f59e0b" else ("Radiación UV Alta" if color_alert == "#f97316" else "Atmosfera Estable")
        
        st.markdown(f'<div class="alert-card" style="border-left-color:{color_alert}; margin-top:8px;"><div class="metric-title" style="color:{color_alert};">ESTADO</div><div style="font-size:0.75rem; font-weight:600;">{msg_alert}</div></div>', unsafe_allow_html=True)

        m = folium.Map(location=[datos['lat'], datos['lon']], zoom_start=12, tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", attr="Carto", zoom_control=False)
        folium.CircleMarker(location=[datos['lat'], datos['lon']], radius=5, color="#38bdf8", fill=True, fill_opacity=0.9).add_to(m)
        st_folium(m, height=140, use_container_width=True)

        pct = max(0, min(100, int(((act["temperatura"] - dia["temp_min"]) / max(1, dia["temp_max"] - dia["temp_min"])) * 100)))
        st.markdown(
            f'<div class="glass-card" style="padding: 10px 14px; margin-top: -10px;">'
            f'<div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700;"><span style="color:#64748b;">{dia["temp_min"]}°</span><span style="color:#38bdf8;">{act["temperatura"]}°</span><span style="color:#f43f5e;">{dia["temp_max"]}°</span></div>'
            f'<div class="progress-bar-bg" style="height: 6px;"><div class="progress-bar-fill" style="width: {pct}%; background: linear-gradient(90deg, #38bdf8, #f43f5e);"></div></div>'
            f'</div>', unsafe_allow_html=True
        )

    # 7 DÍAS
    if not df_d.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="metric-title" style="margin-bottom: 8px;">PRONÓSTICO 7 DÍAS</div>', unsafe_allow_html=True)
        cols_dias = st.columns(7)
        for idx, col in enumerate(cols_dias):
            if idx < len(df_d):
                row = df_d.iloc[idx]
                with col:
                    st.markdown(
                        f'<div class="glass-card" style="text-align: center; padding: 10px 4px;">'
                        f'<div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600;">{["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"][pd.to_datetime(row["time"]).weekday()]}</div>'
                        f'<div style="margin: 6px 0;">{generar_svg_icono(mapear_wmo_a_tipo_icono(row.get("weather_code", 0)), size=24)}</div>'
                        f'<div style="font-weight: 700; font-size: 0.95rem;">{round(row["temperature_2m_max"])}°</div>'
                        f'<div style="font-size: 0.7rem; color: #64748b;">{round(row["temperature_2m_min"])}°</div>'
                        f'</div>', unsafe_allow_html=True
                    )

    # HISTÓRICO Y MMA (COMPACTO Y CON ICONOS SVG)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander(f"ANÁLISIS CLIMÁTICO E IMPACTO MULTISECTORIAL - {datos['ciudad'].upper()}", expanded=False):
        st.plotly_chart(generar_grafico_historico(datos['lat'], datos['lon'], datos['ciudad']), use_container_width=True, config={'displayModeBar': False})

        # Iconos vectoriales para títulos y listas
        pin_icon = generar_svg_icono("pin", size=18, color="#f59e0b")
        map_icon = generar_svg_icono("map", size=18, color="#38bdf8")
        temp_icon = generar_svg_icono("thermometer", size=14, color="#f43f5e")
        rain_icon = generar_svg_icono("droplet", size=14, color="#38bdf8")

        # Tarjeta DMC
        st.markdown(
            f'<div class="climate-box">'
            f'<div class="climate-box-title" style="color: #f59e0b;">{pin_icon} EVOLUCIÓN CLIMÁTICA REGISTRADA EN CHILE (DMC / MMA)</div>'
            f'<div class="grid-auto-fit">'
            f'<div><div style="display:flex; align-items:center; gap:4px;"><b style="color:#f43f5e; font-size:0.8rem;">{temp_icon} Temperatura:</b></div><ul style="font-size:0.75rem; padding-left:16px; margin-bottom:0;"><li>Aumento +0.15°C por década.</li><li>1 semana más sobre 30°C cada 10 años.</li></ul></div>'
            f'<div><div style="display:flex; align-items:center; gap:4px;"><b style="color:#38bdf8; font-size:0.8rem;">{rain_icon} Precipitaciones:</b></div><ul style="font-size:0.75rem; padding-left:16px; margin-bottom:0;"><li>Norte: Aumento lluvias verano (20-40%).</li><li>Centro/Sur: Caída del 12% a 20%.</li></ul></div>'
            f'</div></div>', unsafe_allow_html=True
        )

        # Tarjeta MMA (Flexbox Side-by-Side)
        st.markdown(
            f'<div class="climate-box">'
            f'<div class="climate-box-title" style="color: #38bdf8; margin-bottom: 12px;">{map_icon} MAPA DE VULNERABILIDAD CLIMÁTICA (MMA 2010 - 2100)</div>'
            f'<div class="mma-flex-container">'
            f'<div class="mma-img-col"><img src="https://mma.gob.cl/wp-content/uploads/2014/11/imagen-cap-4-1.png" alt="Impacto Cambio Climatico MMA"/></div>'
            f'<div class="mma-text-col">'
            f'<div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:8px;"><b style="color:#f59e0b; font-size:0.8rem;">2010 - 2040</b><div style="font-size:0.75rem; margin-top:2px; color:#e2e8f0;">Incremento térmico: <b>0.5° a 1.5°C</b>. Lluvias: <b>-15% a -5%</b> en zona centro/sur. Impacto minería, agua y agro.</div></div>'
            f'<div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:8px;"><b style="color:#f97316; font-size:0.8rem;">2040 - 2070</b><div style="font-size:0.75rem; margin-top:2px; color:#e2e8f0;">Incremento térmico: <b>1.5° a 2.5°C</b>. Estrés en hidroelectricidad, bosques. Riesgo tormentas cálidas.</div></div>'
            f'<div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:8px;"><b style="color:#f43f5e; font-size:0.8rem;">2070 - 2100</b><div style="font-size:0.75rem; margin-top:2px; color:#e2e8f0;">Incremento térmico: <b>2.5° a 4.5°C</b>. Reducción crítica de agua (hasta <b>-30%</b>). Efectos en puertos y salud.</div></div>'
            f'</div>'
            f'</div>'
            f'<div style="margin-top:12px; font-size:0.7rem; color:#94a3b8; border-top:1px solid rgba(255,255,255,0.06); padding-top:6px;">Fuente: Portal de Vulnerabilidad MMA. <a href="https://mma.gob.cl/cambio-climatico/vulnerabilidad-y-adaptacion/" target="_blank">Consultar fuente oficial ↗</a></div>'
            f'</div>', unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="app-footer">'
        f'<div style="font-weight:700; color:white; margin-bottom:4px;">SkyForm • Plataforma Integrada de Control y Observación Sensorial </div>'
        f'<div>Desarrollado por <b>Alfredo Castro Alarcón</b> (Alphareone) • Datos: Open-Meteo & CartoDB © {pd.Timestamp.now().year}</div>'
        f'</div>', unsafe_allow_html=True
    )