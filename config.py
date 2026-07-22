import streamlit as st

def obtener_fondo_segun_clima(llave_clima="sol_nube", is_day=1):
    # Nueva imagen de Unsplash asignada para el modo noche
    fondo_noche_personalizado = "https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?fm=jpg&q=60&w=3000&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Y2llbG8lMjBlc3RyZWxsYWRvfGVufDB8fDB8fHww"

    fondos = {
        "despejado_dia": "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd?q=80&w=1920",
        "despejado_noche": fondo_noche_personalizado,
        "nublado_dia": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1920",
        "nublado_noche": fondo_noche_personalizado,
        "lluvia": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?q=80&w=1920",
        "tormenta": "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?q=80&w=1920",
        "nieve": "https://images.unsplash.com/photo-1483921020237-2ff51e8e4b22?q=80&w=1920"
    }

    if "lluvia" in llave_clima or "chubasco" in llave_clima:
        return fondos["lluvia"]
    elif "tormenta" in llave_clima:
        return fondos["tormenta"]
    elif "nieve" in llave_clima:
        return fondos["nieve"]
    elif "nublado" in llave_clima or "cubierto" in llave_clima:
        return fondos["nublado_dia"] if is_day else fondos["nublado_noche"]
    else:
        return fondos["despejado_dia"] if is_day else fondos["despejado_noche"]


def aplicar_estilos_base(llave_icono="sol_nube", is_day=1):
    bg_url = obtener_fondo_segun_clima(llave_icono, is_day)

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@200;300;400;500;600;700&display=swap');

        .stApp {{
            background: url('{bg_url}') no-repeat center center fixed !important;
            background-size: cover !important;
            font-family: 'SF Pro Display', -apple-system, sans-serif !important;
            transition: background 1s ease-in-out;
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        .main .block-container {{
            max-width: 680px !important;
            padding: 1.5rem 1rem !important;
            margin: 0 auto !important;
        }}

        /* Tarjeta de Cristal Glassmorphism */
        .glass-card {{
            background: rgba(0, 0, 0, 0.42) !important;
            backdrop-filter: blur(22px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(22px) saturate(160%) !important;
            border: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 28px !important;
            padding: 24px 20px !important;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5) !important;
            color: #FFFFFF !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.6);
            margin-bottom: 20px;
            position: relative;
        }}

        /* ANIMACIONES CSS */
        @keyframes floating {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}

        @keyframes pulseGlow {{
            0% {{ opacity: 0.85; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.03); }}
            100% {{ opacity: 0.85; transform: scale(1); }}
        }}

        .animated-icon {{
            animation: floating 3.5s ease-in-out infinite;
        }}

        .animated-temp {{
            animation: pulseGlow 4s ease-in-out infinite;
        }}

        /* Brújula Anular de Viento */
        .compass-ring {{
            width: 58px;
            height: 58px;
            border: 2px solid rgba(234, 179, 8, 0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            position: relative;
            background: rgba(0,0,0,0.25);
            box-shadow: 0 0 12px rgba(234, 179, 8, 0.3);
        }}

        .compass-pointer {{
            position: absolute;
            top: -2px;
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-bottom: 10px solid #EF4444;
        }}

        /* Estilo para el buscador desplegable */
        div[data-baseweb="select"] > div {{
            background: rgba(0, 0, 0, 0.55) !important;
            backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 14px !important;
            color: #FFF !important;
        }}
        </style>
    """, unsafe_allow_html=True)