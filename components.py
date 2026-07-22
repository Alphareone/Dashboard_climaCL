import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

ICONS = {
    "temp": '<svg class="icon-svg icon-pulse" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F87171" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
    "uv": '<svg class="icon-svg icon-float" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FACC15" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    "wind": '<svg class="icon-svg icon-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
    "humidity": '<svg class="icon-svg icon-float" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    "rain": '<svg class="icon-svg icon-pulse" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><path d="M16 13v8M8 13v8M12 15v8M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/></svg>'
}

def renderizar_banner_alerta(alertas):
    """Muestra banners de riesgo prominentes como Google Weather"""
    for al in alertas:
        st.markdown(f'''
            <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #EF4444; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
                <h4 style="color: #FCA5A5; margin: 0 0 6px 0; font-size: 1.1rem;">⚠️ {al['titulo']}</h4>
                <p style="color: #E2E8F0; margin: 0; font-size: 0.9rem;">{al['msg']}</p>
            </div>
        ''', unsafe_allow_html=True)

def renderizar_grafico_google_style(hourly_data, variable_sel):
    """Renderiza el gráfico continuo de la curva del día estilo Google Weather"""
    df_hourly = pd.DataFrame({
        "Hora": [pd.to_datetime(t).strftime('%H:00') for t in hourly_data["time"][:24]],
        "Temperatura": hourly_data["temperature_2m"][:24],
        "Precipitaciones": hourly_data["precipitation_probability"][:24],
        "Viento": hourly_data["wind_speed_10m"][:24]
    })

    eje_y = variable_sel
    color_linea = "#FACC15" if variable_sel == "Temperatura" else ("#38BDF8" if variable_sel == "Precipitaciones" else "#818CF8")
    unidad = "°C" if variable_sel == "Temperatura" else ("%" if variable_sel == "Precipitaciones" else " km/h")

    fig = go.Figure()
    
    # Línea suave con relleno de área
    fig.add_trace(go.Scatter(
        x=df_hourly["Hora"],
        y=df_hourly[eje_y],
        mode='lines+text',
        text=[f"{v}{unidad}" for v in df_hourly[eje_y]],
        textposition="top center",
        line=dict(color=color_linea, width=3, shape='spline'),
        fill='tozeroy',
        fillcolor=f"rgba({ '250, 204, 21' if variable_sel == 'Temperatura' else '56, 189, 248' }, 0.1)"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False, color="#94A3B8"),
        yaxis=dict(showgrid=False, showticklabels=False),
        height=220
    )
    return fig

def renderizar_pronostico_7dias(daily_data):
    """Muestra la fila con los 7 días de pronóstico estilo Google"""
    st.markdown("### 📅 Pronóstico Semanal")
    cols = st.columns(7)
    
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    for i in range(min(7, len(daily_data["time"]))):
        fecha = pd.to_datetime(daily_data["time"][i])
        nombre_dia = dias_semana[fecha.weekday()]
        max_t = int(daily_data["temperature_2m_max"][i])
        min_t = int(daily_data["temperature_2m_min"][i])
        prob_lluvia = daily_data.get("precipitation_probability_max", [0]*7)[i]

        with cols[i]:
            st.markdown(f'''
                <div class="glass-card" style="text-align: center; padding: 12px 6px;">
                    <div style="font-weight: 700; color: #94A3B8; font-size: 0.9rem;">{nombre_dia}</div>
                    <div style="margin: 8px 0;">{ICONS['rain'] if prob_lluvia > 40 else ICONS['temp']}</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #F8FAFC;">{max_t}°</div>
                    <div style="font-size: 0.85rem; color: #64748B;">{min_t}°</div>
                </div>
            ''', unsafe_allow_html=True)

def renderizar_mapa_multicapa(ciudades_data, capa_seleccionada):
    df = pd.DataFrame(ciudades_data)
    mapa_cols = {"Temperatura (°C)": "temperatura", "Velocidad del Viento (km/h)": "viento", "Radiación / Índice UV": "uv"}
    col_activa = mapa_cols.get(capa_seleccionada, "temperatura")
    
    fig = px.scatter_map(
        df, lat="lat", lon="lon", size=col_activa, color=col_activa, hover_name="nombre",
        color_continuous_scale="Plasma" if col_activa == "uv" else "Viridis", zoom=4.3, center={"lat": -36.5, "lon": -71.5}
    )
    fig.update_layout(
        map_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        map=dict(bounds=dict(west=-78.0, east=-65.0, south=-56.0, north=-17.0))
    )
    return fig