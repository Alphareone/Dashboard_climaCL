import streamlit as st

def aplicar_estilos_base(llave_icono="sol"):
    """
    Aplica estilos base y fondo ambiental dinámico según el clima actual de Chile.
    """
    # Mapas de color y movimiento según el clima
    estilos_clima = {
        "sol": {
            "bg": "radial-gradient(circle at 50% 20%, #1E1B4B 0%, #0F172A 60%, #0A0A16 100%)",
            "glow": "radial-gradient(circle at 80% 10%, rgba(250, 204, 21, 0.18) 0%, transparent 50%)"
        },
        "sol_nube": {
            "bg": "radial-gradient(circle at 50% 20%, #1E293B 0%, #0F172A 70%, #080D1A 100%)",
            "glow": "radial-gradient(circle at 80% 10%, rgba(56, 189, 248, 0.15) 0%, transparent 50%)"
        },
        "nube": {
            "bg": "radial-gradient(circle at 50% 20%, #111827 0%, #0B0F19 70%, #030712 100%)",
            "glow": "radial-gradient(circle at 50% 10%, rgba(148, 163, 184, 0.12) 0%, transparent 50%)"
        },
        "lluvia": {
            "bg": "radial-gradient(circle at 50% 20%, #0F2027 0%, #203A43 50%, #2C5364 100%)",
            "glow": "radial-gradient(circle at 50% 30%, rgba(56, 189, 248, 0.25) 0%, transparent 60%)"
        },
        "lluvia_fuerte": {
            "bg": "radial-gradient(circle at 50% 20%, #0B132B 0%, #1C2541 60%, #0B0C10 100%)",
            "glow": "radial-gradient(circle at 50% 20%, rgba(96, 165, 250, 0.3) 0%, transparent 60%)"
        }
    }

    config_actual = estilos_clima.get(llave_icono, estilos_clima["sol_nube"])

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background: {config_actual['bg']} !important;
            background-size: 200% 200% !important;
            animation: weatherAtmosphere 14s ease-in-out infinite alternate !important;
            color: #F1F5F9;
        }}

        /* Capa de resplandor ambiental interactivo */
        [data-testid="stAppViewContainer"]::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: {config_actual['glow']};
            pointer-events: none;
            z-index: 0;
        }}

        @keyframes weatherAtmosphere {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        /* CONTENEDOR VISTA ÚNICA RESPONSIVA (Móvil, Tablet y Desktop) */
        .main .block-container {{
            max-width: 680px !important;
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
            position: relative;
            z-index: 1;
        }}

        /* TARJETAS GLASSMORPHIC CON BORDES LUMINOSOS */
        .ui-card {{
            background: rgba(15, 23, 42, 0.72);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}

        .ui-card:hover {{
            border-color: rgba(56, 189, 248, 0.3);
        }}

        .pill-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 20px;
            color: #38BDF8;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .hero-temp-large {{
            font-size: clamp(3.2rem, 8vw, 4.5rem);
            font-weight: 800;
            line-height: 0.9;
            color: #FFFFFF;
            letter-spacing: -2px;
        }}

        .hero-desc {{
            font-size: 1.15rem;
            font-weight: 600;
            color: #38BDF8;
            margin-top: 4px;
            margin-bottom: 12px;
        }}

        .hero-submetrics {{
            font-size: 0.82rem;
            color: #94A3B8;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 10px 14px;
            border-radius: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        /* ÍCONOS CON ANIMACIONES INTERACTIVAS */
        .svg-icon {{
            display: inline-block;
            vertical-align: middle;
            filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.5));
        }}

        .anim-spin {{ animation: spin 14s linear infinite; }}
        .anim-float {{ animation: float 4s ease-in-out infinite alternate; }}
        .anim-rain {{ animation: rainPulse 1.2s ease-in-out infinite alternate; }}
        .anim-pulse {{ animation: pulseGlow 2s ease-in-out infinite alternate; }}

        @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
        @keyframes float {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY(-6px); }} }}
        @keyframes rainPulse {{ 0% {{ transform: translateY(-2px); opacity: 0.6; }} 100% {{ transform: translateY(3px); opacity: 1; }} }}
        @keyframes pulseGlow {{ 0% {{ opacity: 0.7; transform: scale(0.98); }} 100% {{ opacity: 1; transform: scale(1.03); }} }}

        /* BOTÓN DE MENÚ LATERAL */
        button[data-testid="stSidebarCollapseButton"] {{
            visibility: visible !important;
            position: fixed !important;
            top: 12px !important;
            left: 12px !important;
            z-index: 99999 !important;
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            color: #38BDF8 !important;
            border-radius: 12px !important;
        }}
        </style>
    """, unsafe_allow_html=True)