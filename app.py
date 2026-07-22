import streamlit as st
import datetime

st.set_page_config(page_title="P.I.C.O.S Chile Weather", page_icon="⚡", layout="centered")

from config import aplicar_estilos_base
from telemetry import obtener_datos_clima, traducir_codigo_clima
from components import (
    renderizar_tarjeta_clima_movil,
    renderizar_curva_hourly_outlook,
    renderizar_grid_metricas,
    renderizar_radar_map
)

# RED DE COBERTURA OFICIAL CHILE
comunas_chile = {
    "Quilpué (Marga Marga)": (-33.0472, -71.4427),
    "Viña del Mar (Valparaíso)": (-33.0245, -71.5518),
    "Valparaíso Centro": (-33.0472, -71.6127),
    "Santiago Central": (-33.4489, -70.6693),
    "Concepción (Biobío)": (-36.8201, -73.0444),
    "Antofagasta": (-23.6509, -70.3975),
    "La Serena (Coquimbo)": (-29.9027, -71.2519),
    "Temuco (Araucanía)": (-38.7359, -72.5904),
    "Puerto Montt (Los Lagos)": (-41.4693, -72.9424),
    "Punta Arenas (Magallanes)": (-53.1638, -70.9171)
}

# SIDEBAR DE CONFIGURACIÓN
st.sidebar.title("⚙️ Red Telemétrica Chile")
comuna_sel = st.sidebar.selectbox("📍 Zona / Comuna de Chile", list(comunas_chile.keys()))
lat, lon = comunas_chile[comuna_sel]

# CONSULTA EN TIEMPO REAL
datos_clima = obtener_datos_clima(lat, lon)

# APLICAR FONDO DINÁMICO SEGÚN EL CLIMA ACTUAL DE LA ZONA
llave_clima = "sol_nube"
if datos_clima and "current" in datos_clima:
    w_code = datos_clima["current"].get("weather_code", 0)
    _, llave_clima = traducir_codigo_clima(w_code)

aplicar_estilos_base(llave_icono=llave_clima)

# NAVEGACIÓN EN VISTA ÚNICA COMPACTA
tab_dashboard, tab_radar, tab_setup = st.tabs(["Dashboard Clima", "Radar Territorial", "Configuración Zona"])

# --- PESTAÑA 1: DASHBOARD PRINCIPAL ---
with tab_dashboard:
    if datos_clima and "current" in datos_clima:
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M hrs")
        
        # 1. Main Weather Hero Card
        renderizar_tarjeta_clima_movil(datos_clima["current"], comuna_sel, fecha_actual)
        
        # 2. Hourly Outlook (Flujo Climático)
        st.markdown('''
            <div class="ui-card">
                <div style="font-size: 0.85rem; font-weight: 800; color: #FFF;">Registro de Flujo Climático</div>
                <div style="font-size: 0.72rem; color: #64748B; margin-bottom: 8px;">Evolución proyectada para las próximas 12 horas</div>
            </div>
        ''', unsafe_allow_html=True)
        
        if "hourly" in datos_clima:
            fig_hourly = renderizar_curva_hourly_outlook(datos_clima["hourly"])
            st.plotly_chart(fig_hourly, width="stretch")
            
        # 3. Grid de métricas en directo
        renderizar_grid_metricas(datos_clima["current"])

# --- PESTAÑA 2: RADAR TERRITORIAL ---
with tab_radar:
    st.markdown('''
        <div class="ui-card">
            <span class="pill-badge">MONITOREO RADAR CHILE</span>
            <h3 style="margin: 6px 0; color: #FFF;">Escaneo Teleférico Geoespacial</h3>
            <p style="font-size: 0.8rem; color: #64748B;">Monitoreo en tiempo real para las coordenadas de la zona seleccionada.</p>
        </div>
    ''', unsafe_allow_html=True)
    
    capa = st.radio("Capa telemétrica:", ["Lluvia / Precipitación", "Flujo de Viento", "Cobertura Nubosa"], horizontal=True)
    fig_radar = renderizar_radar_map(lat, lon)
    st.plotly_chart(fig_radar, width="stretch")

# --- PESTAÑA 3: CONFIGURACIÓN ZONA ---
with tab_setup:
    st.markdown('''
        <div class="ui-card">
            <span class="pill-badge">RED DE ESTACIONES</span>
            <h2 style="margin: 6px 0; color: #FFF; font-weight: 800;">Territorio Nacional</h2>
            <p style="font-size: 0.85rem; color: #64748B;">Monitoreo continuo en tiempo real exclusivo para Chile.</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="ui-card" style="padding: 14px;">
            <div style="font-size: 0.75rem; color: #64748B;">PAÍS</div>
            <div style="font-weight: 700; color: #FFF;">República de Chile</div>
        </div>
        <div class="ui-card" style="padding: 14px;">
            <div style="font-size: 0.75rem; color: #64748B;">UNIDADES OFICIALES</div>
            <div style="font-weight: 700; color: #FFF;">Métrico (°C, km/h, hPa)</div>
        </div>
    ''', unsafe_allow_html=True)