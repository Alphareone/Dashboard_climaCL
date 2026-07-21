import streamlit as st

def aplicar_estilos_base():
    st.markdown("""
        <style>
        /* Fondo general UI estilo Dark Glass OS */
        .stApp {
            background-color: #0B101D;
            color: #E2E8F0;
        }
        
        /* Ocultar marca de agua y menús por defecto */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Sidebar Personalizado */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Banner Hero Principal */
        .hero-card {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #06B6D4 100%);
            border-radius: 20px;
            padding: 24px;
            color: white;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
            margin-bottom: 20px;
            position: relative;
            transition: all 0.3s ease;
        }
        .hero-card:hover {
            box-shadow: 0 15px 30px -5px rgba(59, 130, 246, 0.6);
            transform: translateY(-2px);
        }
        .hero-temp {
            font-size: 3.8rem;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -1px;
        }
        .hero-city {
            font-size: 1.6rem;
            font-weight: 700;
            opacity: 0.95;
        }
        
        /* Tarjetas Glassmorphic Interactivas */
        .glass-card {
            background: #111827;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 12px 20px -5px rgba(56, 189, 248, 0.15);
        }
        
        .metric-title {
            font-size: 0.75rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
        }
        .metric-num {
            font-size: 1.6rem;
            font-weight: 700;
            color: #F8FAFC;
        }

        /* Pulsación Live Indicator */
        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
            70% { box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }
            100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
        }
        .live-badge {
            display: inline-block;
            width: 9px;
            height: 9px;
            background-color: #38BDF8;
            border-radius: 50%;
            animation: pulse-glow 2s infinite;
            margin-right: 6px;
        }
        </style>
    """, unsafe_allow_html=True)