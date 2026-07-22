import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from telemetry import traducir_codigo_clima

# BIBLIOTECA DE ÍCONOS VECTORIALES INTERACTIVOS SVG (SIN EMOJIS)
ICONS_SVG = {
    "location": '<svg class="svg-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2.5"><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>',
    "sol": '<svg class="svg-icon anim-spin" width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#FACC15" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    "sol_nube": '<svg class="svg-icon anim-float" width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9 h1.79a4.5 4.5 0 1 1 0 9z"/><path d="M12 2v2M4.22 4.22l1.42 1.42M1 12h2" stroke="#FACC15"/></svg>',
    "nube": '<svg class="svg-icon anim-float" width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9 h1.79a4.5 4.5 0 1 1 0 9z"/></svg>',
    "nubes": '<svg class="svg-icon anim-float" width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9 h1.79a4.5 4.5 0 1 1 0 9z"/><path d="M22 10a3 3 0 0 0-5.83-1" stroke="#475569"/></svg>',
    "lluvia": '<svg class="svg-icon anim-rain" width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M16 13v6M8 13v6M12 15v6M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/></svg>',
    "lluvia_fuerte": '<svg class="svg-icon anim-rain" width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2.5"><path d="M16 13v8M8 13v8M12 14v8M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/></svg>',
    "viento": '<svg class="svg-icon anim-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
    "humedad": '<svg class="svg-icon anim-pulse" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    "presion": '<svg class="svg-icon anim-pulse" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FACC15" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "uv": '<svg class="svg-icon anim-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2"/></svg>'
}

def renderizar_tarjeta_clima_movil(curr, ciudad, fecha_str):
    temp_act = int(curr.get("temperature_2m", 0))
    temp_sens = int(curr.get("apparent_temperature", temp_act))
    viento = int(curr.get("wind_speed_10m", 0))
    uv = curr.get("uv_index", 0)
    w_code = curr.get("weather_code", 0)
    
    estado_texto, llave_icono = traducir_codigo_clima(w_code)
    icono_svg = ICONS_SVG.get(llave_icono, ICONS_SVG["sol_nube"])

    st.markdown(f'''
        <div class="ui-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span class="pill-badge">{ICONS_SVG["location"]} {ciudad.upper()}, CHILE</span>
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 600;">{fecha_str}</span>
            </div>
            <div style="font-size: 0.72rem; color: #38BDF8; font-weight: 700; letter-spacing: 0.08em;">ESTADO OFICIAL EN TIEMPO REAL</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0;">
                <div>
                    <div class="hero-temp-large">{temp_act}°C</div>
                    <div class="hero-desc">{estado_texto}</div>
                </div>
                <div>{icono_svg}</div>
            </div>
            <div class="hero-submetrics">
                <span>Sensación: <b>{temp_sens}°C</b></span>
                <span>Viento: <b>{viento} km/h</b></span>
                <span>UV Index: <b>{uv}</b></span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

def renderizar_curva_hourly_outlook(hourly_data):
    horas = [pd.to_datetime(t).strftime('%H:00') for t in hourly_data["time"][:12]]
    temps = hourly_data["temperature_2m"][:12]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=horas, y=temps,
        mode='lines+markers+text',
        text=[f"{int(t)}°" for t in temps],
        textposition="top center",
        line=dict(color='#38BDF8', width=3, shape='spline'),
        marker=dict(size=6, color='#60A5FA'),
        fill='tozeroy',
        fillcolor='rgba(56, 189, 248, 0.12)'
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=25, b=0),
        xaxis=dict(showgrid=False, color="#64748B", tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, showticklabels=False), height=160
    )
    return fig

def renderizar_grid_metricas(curr):
    col1, col2, col3 = st.columns(3)
    hum = curr.get("relative_humidity_2m", "--")
    viento = curr.get("wind_speed_10m", "--")
    presion = int(curr.get("surface_pressure", 1013))
    
    with col1:
        st.markdown(f'''
            <div class="ui-card" style="padding: 14px; text-align: center;">
                <div style="margin-bottom: 4px;">{ICONS_SVG["humedad"]}</div>
                <div style="font-size: 0.68rem; color: #64748B; font-weight: 700;">HUMEDAD</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #FFF; margin-top: 2px;">{hum}%</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''
            <div class="ui-card" style="padding: 14px; text-align: center;">
                <div style="margin-bottom: 4px;">{ICONS_SVG["viento"]}</div>
                <div style="font-size: 0.68rem; color: #64748B; font-weight: 700;">FUERZA VIENTO</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #FFF; margin-top: 2px;">{viento} <small style="font-size:0.65rem">km/h</small></div>
            </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
            <div class="ui-card" style="padding: 14px; text-align: center;">
                <div style="margin-bottom: 4px;">{ICONS_SVG["presion"]}</div>
                <div style="font-size: 0.68rem; color: #64748B; font-weight: 700;">PRESIÓN</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #FFF; margin-top: 2px;">{presion} <small style="font-size:0.65rem">hPa</small></div>
            </div>
        ''', unsafe_allow_html=True)

def renderizar_radar_map(lat, lon):
    df = pd.DataFrame([{"lat": lat, "lon": lon, "size": 20}])
    fig = px.scatter_map(
        df, lat="lat", lon="lon", size="size", zoom=7, center={"lat": lat, "lon": lon}
    )
    fig.update_layout(
        map_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320
    )
    return fig