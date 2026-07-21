import streamlit as st

def aplicar_estilos_base():
    st.markdown("""
        <style>
        /* Fondo ambiental dinámico */
        .stApp {
            background: radial-gradient(circle at 50% 50%, #1E293B 0%, #0F172A 50%, #0B101D 100%);
            background-size: 200% 200%;
            animation: waterGlow 12s ease-in-out infinite alternate;
            color: #E2E8F0;
        }

        @keyframes waterGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Ocultar UI nativa sobrante */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Sidebar Glassmorphic */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Tarjeta Principal Hero */
        .hero-card {
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(59, 130, 246, 0.9) 50%, rgba(6, 182, 212, 0.9) 100%);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 24px;
            color: white;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
            margin-bottom: 20px;
        }
        .hero-temp { font-size: 3.8rem; font-weight: 800; line-height: 1; letter-spacing: -1px; }
        .hero-city { font-size: 1.6rem; font-weight: 700; opacity: 0.95; }

        /* Tarjetas Glassmorphic */
        .glass-card {
            background: rgba(17, 24, 39, 0.8);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 12px 20px -5px rgba(56, 189, 248, 0.15);
        }

        .metric-title { font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; display: flex; align-items: center; gap: 6px; }
        .metric-num { font-size: 1.6rem; font-weight: 700; color: #F8FAFC; margin-top: 4px; }

        /* EFECTOS Y ANIMACIONES PARA ÍCONOS SVG */
        .icon-svg {
            display: inline-block;
            vertical-align: middle;
            transition: transform 0.3s ease;
        }
        
        /* Animación Flotante (Nubes/UV) */
        .icon-float {
            animation: floatAnim 3s ease-in-out infinite alternate;
        }
        @keyframes floatAnim {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-4px); }
        }

        /* Animación Giratoria (Viento/Cargando) */
        .icon-spin {
            animation: spinAnim 8s linear infinite;
        }
        @keyframes spinAnim {
            100% { transform: rotate(360deg); }
        }

        /* Animación Pulso (Peligro/Alertas) */
        .icon-pulse {
            animation: pulseAnim 1.5s ease-in-out infinite;
        }
        @keyframes pulseAnim {
            0% { transform: scale(1); filter: drop-shadow(0 0 2px rgba(56, 189, 248, 0.5)); }
            50% { transform: scale(1.15); filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.9)); }
            100% { transform: scale(1); filter: drop-shadow(0 0 2px rgba(56, 189, 248, 0.5)); }
        }

        /* Indicador en Vivo */
        .live-badge {
            display: inline-block;
            width: 9px;
            height: 9px;
            background-color: #38BDF8;
            border-radius: 50%;
            animation: pulseAnim 2s infinite;
            margin-right: 6px;
        }
        </style>
    """, unsafe_allow_html=True)