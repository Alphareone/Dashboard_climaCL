import streamlit as st

def obtener_fondo_segun_clima(tipo_icono="sun", es_dia=1):
    """
    Selecciona fondos de pantalla estética Pinterest con paisajes representativos
    clasificados por condición meteorológica y ciclo solar (Día / Noche).
    """
    fondos = {
        # DESPEJADO / SOL
        # Día: Panorámica de montañas iluminadas con horizonte despejado
        "sun_dia": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=1920",
        # Noche: Cielos estrellados sobre siluetas montañosas (Estilo Atacama/Elqui)
        "sun_noche": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=1920",
        
        # NUBLADO / PARCIAL
        # Día: Capas de nubes sobre valles montañosos
        "cloud_dia": "https://i.pinimg.com/736x/16/a8/59/16a8596546f510d150b1f5fd31bbd52b.jpg",
        # Noche: Noche mística con nubes bajas e iluminación suave en la costa
        "cloud_noche": "https://i.pinimg.com/1200x/06/89/b6/0689b6419fe8a55d3a9157313d250dbb.jpg",
        
        # LLUVIA / CHUBASCOS
        # Día: Lluvia y neblina cayendo sobre un bosque panorámico
        "rain_dia": "https://i.pinimg.com/736x/a0/66/98/a066984158fdd32fc357792cecdc9125.jpg",
        # Noche: Lluvia nocturna y ambiente húmedo dramático
        "rain_noche": "https://i.pinimg.com/736x/8b/42/1f/8b421f1ca5f8657ce307826710e50eae.jpg",
        
        # TORMENTA ELÉCTRICA
        # Día: Nubarrones de tormenta sobre relieve montañoso
        "storm_dia": "https://images.unsplash.com/photo-1527482797697-8795b05a13fe?q=80&w=1920",
        # Noche: Rayo cayendo en horizonte nocturno
        "storm_noche": "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?q=80&w=1920",
        
        # NIEVE
        # Día: Picos de montañas cubiertos de nieve en gran angular
        "snow_dia": "https://i.pinimg.com/736x/c6/c4/0b/c6c40bb06962cf0518c1dae60ef17085.jpg",
        # Noche: Paisaje nevado bajo la noche clara
        "snow_noche": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?q=80&w=1920",
        
        # NIEBLA / CAMANCHACA
        # Día: Capa densa de niebla rozando la copa de los árboles/cerros
        "fog_dia": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?q=80&w=1920",
        # Noche: Bruma nocturna con luces suaves en el fondo
        "fog_noche": "https://images.unsplash.com/photo-1494783367193-149034c05e8f?q=80&w=1920"
    }

    # Evaluación y mapeo dinámico según el icono recibido de la API
    icono = str(tipo_icono).lower()
    es_dia = int(es_dia)

    if "storm" in icono or "tormenta" in icono:
        return fondos["storm_dia"] if es_dia == 1 else fondos["storm_noche"]
    elif "snow" in icono or "nieve" in icono:
        return fondos["snow_dia"] if es_dia == 1 else fondos["snow_noche"]
    elif "fog" in icono or "niebla" in icono or "bruma" in icono:
        return fondos["fog_dia"] if es_dia == 1 else fondos["fog_noche"]
    elif "rain" in icono or "lluvia" in icono or "chubasco" in icono:
        return fondos["rain_dia"] if es_dia == 1 else fondos["rain_noche"]
    elif "cloud" in icono or "nublado" in icono or "cubierto" in icono:
        return fondos["cloud_dia"] if es_dia == 1 else fondos["cloud_noche"]
    else:
        return fondos["sun_dia"] if es_dia == 1 else fondos["sun_noche"]
def aplicar_estilos_base(tipo_icono="sun", es_dia=1):
    bg_url = obtener_fondo_segun_clima(tipo_icono, es_dia)

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@200;300;400;500;600;700&display=swap');

        .stApp {{
            background: linear-gradient(rgba(11, 15, 25, 0.70), rgba(11, 15, 25, 0.85)), url('{bg_url}') no-repeat center center fixed !important;
            background-size: cover !important;
            font-family: 'SF Pro Display', -apple-system, sans-serif !important;
            transition: background 1s ease-in-out;
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        .main .block-container {{
            max-width: 1200px !important;
            padding: 1.5rem 1rem !important;
            margin: 0 auto !important;
        }}

        /* Tarjeta de Cristal Glassmorphism */
        .glass-card {{
            background: rgba(17, 24, 39, 0.65) !important;
            backdrop-filter: blur(16px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(16px) saturate(160%) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 20px !important;
            padding: 20px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4) !important;
            color: #FFFFFF !important;
            margin-bottom: 12px;
        }}

        div[data-baseweb="select"] > div {{
            background: rgba(0, 0, 0, 0.55) !important;
            backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 14px !important;
            color: #FFF !important;
        }}
        </style>
    """, unsafe_allow_html=True)