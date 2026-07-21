import streamlit as st
import plotly.graph_objects as go
import pydeck as pdk
import pandas as pd
from datetime import datetime
import pytz

SVG_ICONS = {
    "radar": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00F0FF" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12 19 5"/><circle cx="12" cy="12" r="2" fill="#00F0FF"/></svg>',
    "activity": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00F0FF" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    "grid": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00F0FF" stroke-width="2"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>',
    "map": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00FF66" stroke-width="2"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/></svg>',
    "shield": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF0055" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
}

def render_header(zona_horaria, nombre_zona, theme_mode):
    tz = pytz.timezone(zona_horaria)
    now = datetime.now(tz)
    txt_color = "#FFFFFF" if theme_mode == "Oscuro Cyberpunk" else "#0F172A"

    col1, col2, col3 = st.columns([4.2, 1.8, 2])
    
    with col1:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: rgba(0, 240, 255, 0.1); padding: 8px; border-radius: 4px; border: 1px solid #00F0FF; display:flex; align-items:center;">
                    {SVG_ICONS['radar']}
                </div>
                <div>
                    <h2 style="margin: 0; color: {txt_color}; font-family: 'Orbitron'; font-size: 1.15rem; letter-spacing: 2px;">
                        SISTEMA F.U.I.S.T.E. B.U.E.N.O.
                    </h2>
                    <span style="color: #00F0FF; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.5px;">
                        [ FLUJO Y UNIFICACIÓN DE INTELIGENCIA SISTEMÁTICA DE TELEMETRÍA ESTACIONAL ]
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; background: rgba(0, 255, 102, 0.08); border: 1px solid #00FF66; padding: 8px 12px; border-radius: 4px;">
                <span class="live-dot"></span>
                <span style="color: #00FF66; font-family: 'Orbitron'; font-size: 0.72rem; font-weight: 800; letter-spacing: 1px;">
                    F.U.I.S.T.E. LIVE
                </span>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="text-align: right; color: {txt_color}; font-family: 'JetBrains Mono';">
                <div style="font-size: 1.2rem; font-weight: 800; color: #00F0FF;">{now.strftime('%H:%M:%S')}</div>
                <div style="font-size: 0.72rem; opacity: 0.8;">CLT // {now.strftime('%d-%b-%Y').upper()}</div>
            </div>
        """, unsafe_allow_html=True)

def render_mapa_3d_chile(nodos_dict, zona_seleccionada, theme_mode):
    data_mapa = []
    for nombre, info in nodos_dict.items():
        es_sel = (nombre == zona_seleccionada)
        data_mapa.append({
            "nombre": nombre,
            "lat": info["lat"],
            "lon": info["lon"],
            "elevation": 120000 if es_sel else 25000,
            "color": [255, 0, 85, 230] if es_sel else [0, 240, 255, 180],
            "radius": 25000 if es_sel else 12000
        })
    
    df_mapa = pd.DataFrame(data_mapa)
    nodo_actual = nodos_dict[zona_seleccionada]

    view_state = pdk.ViewState(
        latitude=nodo_actual["lat"],
        longitude=nodo_actual["lon"],
        zoom=5.8,
        pitch=45,
        bearing=-10
    )

    column_layer = pdk.Layer(
        "ColumnLayer",
        data=df_mapa,
        get_position=["lon", "lat"],
        get_elevation="elevation",
        elevation_scale=1,
        radius="radius",
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    map_style = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json" if theme_mode == "Oscuro Cyberpunk" else "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

    deck = pdk.Deck(
        layers=[column_layer],
        initial_view_state=view_state,
        map_style=map_style,
        tooltip={"text": "NODO OPERATIVO F.U.I.S.T.E.: {nombre}"}
    )

    st.pydeck_chart(deck, use_container_width=True)

def render_chart_historico(df_hourly, theme_mode):
    fig = go.Figure()
    grid_c = "#1E293B" if theme_mode == "Oscuro Cyberpunk" else "#E2E8F0"
    txt_c = "#00F0FF" if theme_mode == "Oscuro Cyberpunk" else "#0F172A"

    fig.add_trace(go.Scatter(
        x=df_hourly["Hora"], y=df_hourly["Temp"],
        name="Temperatura (°C)", mode='lines+markers',
        line=dict(color="#00F0FF", width=3, shape='spline'),
        marker=dict(size=5, color="#00F0FF")
    ))
    
    fig.add_trace(go.Scatter(
        x=df_hourly["Hora"], y=df_hourly["Humedad"],
        name="Humedad (%)", mode='lines+markers', yaxis="y2",
        line=dict(color="#00FF66", width=2, dash='dot'),
        marker=dict(size=4, color="#00FF66")
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=240,
        margin=dict(l=5, r=5, t=10, b=5),
        legend=dict(orientation="h", y=1.15, x=0.1, font=dict(color=txt_c, size=10)),
        xaxis=dict(showgrid=True, gridcolor=grid_c, tickfont=dict(color=txt_c, size=10)),
        yaxis=dict(showgrid=True, gridcolor=grid_c, tickfont=dict(color=txt_c, size=10)),
        yaxis2=dict(overlaying="y", side="right", showgrid=False, tickfont=dict(color="#00FF66", size=10))
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def generar_html_reporte_pdf(nodo_nombre, data, indices):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Reporte F.U.I.S.T.E. B.U.E.N.O.</title>
        <style>
            body {{ font-family: 'Helvetica', sans-serif; background: #0b0f19; color: #e2e8f0; padding: 30px; }}
            .header {{ border-bottom: 2px solid #00f0ff; padding-bottom: 10px; margin-bottom: 20px; }}
            h1 {{ color: #00f0ff; font-size: 20px; margin: 0; }}
            .card {{ background: #131b2e; border: 1px solid #1e293b; padding: 15px; margin-bottom: 15px; border-radius: 4px; }}
            .value {{ font-size: 24px; font-weight: bold; color: #00ff66; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SISTEMA F.U.I.S.T.E. B.U.E.N.O. - INFORME TÉCNICO</h1>
            <p>NODO EVALUADO: <strong>{nodo_nombre.upper()}</strong> | FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        <div class="card">
            <h3>TELEMETRÍA ATMOSFÉRICA</h3>
            <p>Temperatura Actual: <span class="value">{data['Temp']} °C</span> (Sensación: {data['Sensacion']} °C)</p>
            <p>Humedad Relativa: <span class="value">{data['Humedad']} %</span></p>
            <p>Viento: <strong>{data['Viento']} km/h</strong> | Presión: <strong>{data['Presion']} hPa</strong></p>
        </div>
        <div class="card">
            <h3>EVALUACIÓN DE RIESGOS ESTACIONALES</h3>
            <p>Punto de Rocío: <strong>{indices['PuntoRocio']} °C</strong></p>
            <p>Riesgo de Incendios: <strong style="color:{indices['ColorIncendio']};">{indices['RiesgoIncendio']}</strong></p>
            <p>Riesgo Agrícola: <strong style="color:{indices['ColorHelada']};">{indices['RiesgoHelada']}</strong></p>
        </div>
    </body>
    </html>
    """