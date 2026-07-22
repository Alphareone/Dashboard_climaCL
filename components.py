import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

def aplicar_estilos_skyform_dinamico(clima):
    es_noche = clima.get('es_noche', False)
    cond = clima.get('condicion', '').lower()
    
    if es_noche:
        bg_url = "https://images.unsplash.com/photo-1509773896068-7fd415d91e2e?q=80&w=1920"
    elif "lluvia" in cond or "llovizna" in cond:
        bg_url = "https://images.unsplash.com/photo-1519692933481-e162a57d6721?q=80&w=1920"
    elif "nublado" in cond:
        bg_url = "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920"
    else:
        bg_url = "https://images.unsplash.com/photo-1601297183305-6df142704ea2?q=80&w=1920"

    st.markdown(f"""
        <style>
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        button[data-testid="stSidebarCollapsedControl"],
        section[data-testid="stSidebar"] button[aria-label="Close"] {{
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }}

        section[data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.95) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(16px) !important;
        }}

        .main .block-container {{
            padding-top: 0.8rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }}
        
        header, footer, #MainMenu {{ visibility: hidden; }}
        
        .stApp {{
            background: linear-gradient(rgba(11, 19, 37, 0.78), rgba(11, 19, 37, 0.88)), url('{bg_url}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            color: #e2e8f0;
        }}
        
        .bento-card {{
            background: rgba(19, 28, 49, 0.48) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 14px;
            padding: 0.7rem 0.9rem !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 0.4rem !important;
        }}
        
        .hero-card {{
            background: {"linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(30, 58, 138, 0.75))" if es_noche else "linear-gradient(135deg, rgba(2, 132, 199, 0.8), rgba(59, 130, 246, 0.7))"} !important;
            backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 0.8rem 1.1rem !important;
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .hero-temp {{
            font-size: 2.7rem !important;
            font-weight: 800;
            line-height: 1;
        }}

        .metric-title {{
            font-size: 0.68rem !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
            font-weight: 700;
        }}

        .metric-val {{
            font-size: 1.05rem !important;
            font-weight: 700;
            color: #ffffff;
        }}

        .daily-box {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 0.35rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(8px);
        }}

        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        .spin-slow {{
            animation: spin 15s linear infinite;
            filter: drop-shadow(0 0 5px rgba(245, 158, 11, 0.6));
        }}
        </style>
    """, unsafe_allow_html=True)


def renderizer_reloj_tiempo_real():
    clock_html = """
    <div style="
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 12px;
        padding: 5px 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        color: #38bdf8;
        font-family: monospace;
        font-size: 0.92rem;
        font-weight: 700;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        width: fit-content;
        margin-left: auto;
    ">
        <span style="
            height: 8px;
            width: 8px;
            background-color: #00ff88;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #00ff88;
        "></span>
        <span id="liveClock">--:--:--</span>
    </div>

    <script>
        function updateClock() {
            const now = new Date();
            const options = { 
                timeZone: 'America/Santiago', 
                hour: '2-digit', 
                minute: '2-digit', 
                second: '2-digit', 
                hour12: false 
            };
            const timeStr = now.toLocaleTimeString('es-CL', options);
            const el = document.getElementById('liveClock');
            if (el) {
                el.innerText = timeStr;
            }
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """
    components.html(clock_html, height=40)


def renderizar_hero_card(clima):
    st.markdown(f"""
        <div class="hero-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; font-size: 0.65rem; font-weight: 700;">AHORA</span>
                    <h2 style="margin: 4px 0 0 0; font-size: 1.3rem;">{clima.get('comuna')}</h2>
                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.85;">{clima.get('condicion')}</p>
                </div>
                <img src="{clima.get('icono_url')}" style="width: 52px; height: 52px; filter: drop-shadow(0 0 8px rgba(255,255,255,0.3));">
            </div>
            <div style="margin-top: 6px; display: flex; align-items: baseline; gap: 12px;">
                <span class="hero-temp">{clima.get('temperatura')}°</span>
                <span style="font-size: 0.85rem; opacity: 0.9;">Máx: {clima.get('temp_max')}° / Mín: {clima.get('temp_min')}°</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def renderizar_grafico_tendencia(clima):
    hourly = clima.get("hourly", {})
    if not hourly or "temperature_2m" not in hourly:
        return

    horas = [h.split("T")[-1] for h in hourly.get("time", [])[:10]]
    temps = hourly.get("temperature_2m", [])[:10]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=horas, y=temps,
        mode='lines+markers',
        line=dict(color='#38bdf8', width=2.5, shape='spline'),
        marker=dict(size=5, color='#00d2ff'),
        fill='tozeroy',
        fillcolor='rgba(56, 189, 248, 0.12)'
    ))

    fig.update_layout(
        margin=dict(l=5, r=5, t=10, b=5),
        height=100,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#94a3b8", size=9)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, tickfont=dict(color="#94a3b8", size=9))
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def renderizar_condiciones_grid(clima):
    st.markdown(f"""
        <div class="bento-card">
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>
                    <div>
                        <div class="metric-title">Humedad</div>
                        <div class="metric-val">{clima.get('humedad')}%</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="spin-slow"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
                    <div>
                        <div class="metric-title">Índice UV</div>
                        <div class="metric-val">{clima.get('uv_index')}</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 1 14 16H2"/></svg>
                    <div>
                        <div class="metric-title">Viento</div>
                        <div class="metric-val">{clima.get('viento_velo')} <span style="font-size: 0.7rem;">km/h</span></div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>
                    <div>
                        <div class="metric-title">Visibilidad</div>
                        <div class="metric-val">{clima.get('visibilidad')} <span style="font-size: 0.7rem;">km</span></div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def renderizar_modulo_lluvia_viento(clima):
    """Renderiza el módulo de probabilidad de lluvia y ráfagas sin sangrías de markdown"""
    prob_lluvia = clima.get('prob_lluvia', 0)
    rafagas = clima.get('rafagas_viento', 0)
    presion = clima.get('presion', 1013.2)
    
    html_content = f"""<div class="bento-card">
<div class="metric-title" style="margin-bottom: 8px;">PRECIPITACIÓN & DINÁMICA DE VIENTO</div>
<div style="margin-bottom: 8px;">
<div style="display: flex; justify-content: space-between; font-size: 0.72rem; margin-bottom: 3px;">
<span style="color: #94a3b8;">Probabilidad Lluvia</span>
<span style="color: #38bdf8; font-weight: 700;">{prob_lluvia}%</span>
</div>
<div style="width: 100%; background: rgba(255,255,255,0.08); height: 6px; border-radius: 3px; overflow: hidden;">
<div style="width: {prob_lluvia}%; background: linear-gradient(90deg, #0284c7, #38bdf8); height: 100%;"></div>
</div>
</div>
<div style="margin-bottom: 8px;">
<div style="display: flex; justify-content: space-between; font-size: 0.72rem; margin-bottom: 3px;">
<span style="color: #94a3b8;">Ráfagas de Viento</span>
<span style="color: #818cf8; font-weight: 700;">{rafagas} km/h</span>
</div>
<div style="width: 100%; background: rgba(255,255,255,0.08); height: 6px; border-radius: 3px; overflow: hidden;">
<div style="width: {min(rafagas * 2, 100)}%; background: linear-gradient(90deg, #6366f1, #818cf8); height: 100%;"></div>
</div>
</div>
<div>
<div style="display: flex; justify-content: space-between; font-size: 0.72rem; margin-bottom: 3px;">
<span style="color: #94a3b8;">Presión Barométrica</span>
<span style="color: #00ff88; font-weight: 700;">{presion} hPa</span>
</div>
<div style="width: 100%; background: rgba(255,255,255,0.08); height: 6px; border-radius: 3px; overflow: hidden;">
<div style="width: {min(max((presion - 980) * 2, 10), 100)}%; background: linear-gradient(90deg, #059669, #00ff88); height: 100%;"></div>
</div>
</div>
</div>"""

    st.markdown(html_content, unsafe_allow_html=True)


def renderizar_arco_solar(clima):
    """Renderiza el Arco Solar Parabólico SVG sin emojis ni sangrías de markdown"""
    amanecer = clima.get('amanecer', '07:30')
    atardecer = clima.get('atardecer', '18:30')
    aqi = clima.get('aqi', 15)
    pm2_5 = clima.get('pm2_5', 0.0)
    
    html_content = f"""<div class="bento-card">
<div class="metric-title" style="margin-bottom: 4px;">CICLO SOLAR Y CALIDAD DEL AIRE</div>
<div style="position: relative; width: 100%; text-align: center; padding: 2px 0;">
<svg width="100%" height="48" viewBox="0 0 200 50" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M 20 45 A 80 35 0 0 1 180 45" stroke="rgba(255, 255, 255, 0.2)" stroke-width="2" stroke-dasharray="4 4" fill="none"/>
<circle cx="130" cy="20" r="5" fill="#f59e0b" filter="drop-shadow(0 0 6px #f59e0b)"/>
<circle cx="20" cy="45" r="3" fill="#38bdf8"/>
<circle cx="180" cy="45" r="3" fill="#818cf8"/>
</svg>
</div>
<div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8; margin-top: -6px;">
<span>Amanecer: <b style="color: #e2e8f0;">{amanecer}</b></span>
<span>Atardecer: <b style="color: #e2e8f0;">{atardecer}</b></span>
</div>
<div style="margin-top: 6px; display: flex; justify-content: space-between; font-size: 0.72rem; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 4px;">
<span>AQI: <b style="color:#00ff88;">{aqi}</b></span>
<span>PM2.5: <b>{pm2_5} µg/m³</b></span>
</div>
</div>"""

    st.markdown(html_content, unsafe_allow_html=True)


def renderizar_mapa_integradom(lat, lon):
    fig = go.Figure(go.Scattermapbox(
        lat=[lat], lon=[lon],
        mode='markers+text',
        marker=dict(size=14, color='#00d2ff'),
        text=["Estación Telemetría"], textposition="top center"
    ))
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=lat, lon=lon),
            zoom=10.5
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=190,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def renderizar_pronostico_7dias(clima):
    cols = st.columns(len(clima.get("daily_forecast", [])))
    for idx, day in enumerate(clima.get("daily_forecast", [])):
        with cols[idx]:
            st.markdown(f"""
                <div class="daily-box">
                    <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700;">{day['day_name']}</div>
                    <img src="{day['icon_url']}" style="width: 26px; height: 26px; margin: 2px 0;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #ffffff;">{day['max_temp']}°</div>
                    <div style="font-size: 0.7rem; color: #64748b;">{day['min_temp']}°</div>
                </div>
            """, unsafe_allow_html=True)