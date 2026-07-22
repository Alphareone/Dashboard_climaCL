from datetime import datetime
import pandas as pd
import requests
import streamlit as st

WMO_MAP = {
    0: {"desc": "Cielo Despejado", "type": "sun"},
    1: {"desc": "Principalmente Despejado", "type": "sun_cloud"},
    2: {"desc": "Parcialmente Nublado", "type": "sun_cloud"},
    3: {"desc": "Nublado", "type": "cloud"},
    45: {"desc": "Niebla", "type": "fog"},
    48: {"desc": "Niebla Escarchada", "type": "fog"},
    51: {"desc": "Llovizna Ligera", "type": "rain_light"},
    53: {"desc": "Llovizna Moderada", "type": "rain"},
    55: {"desc": "Llovizna Densa", "type": "rain"},
    61: {"desc": "Lluvia Ligera", "type": "rain_light"},
    63: {"desc": "Lluvia Moderada", "type": "rain"},
    65: {"desc": "Lluvia Fuerte", "type": "rain_heavy"},
    71: {"desc": "Nieve Ligera", "type": "snow"},
    73: {"desc": "Nieve Moderada", "type": "snow"},
    75: {"desc": "Nieve Fuerte", "type": "snow"},
    80: {"desc": "Chubascos Leves", "type": "rain_light"},
    81: {"desc": "Chubascos Moderados", "type": "rain"},
    82: {"desc": "Chubascos Violentos", "type": "storm"},
    95: {"desc": "Tormenta Eléctrica", "type": "storm"},
    96: {"desc": "Tormenta con Granizo Leve", "type": "storm"},
    99: {"desc": "Tormenta con Granizo Fuerte", "type": "storm"},
}

TERRITORIO_CHILE = {
    "Arica y Parinacota": {
        "Arica": (-18.4783, -70.3126),
        "Putre": (-18.1964, -69.5592),
    },
    "Tarapacá": {
        "Iquique": (-20.2133, -70.1503),
        "Alto Hospicio": (-20.2689, -70.1009),
        "Pozo Almonte": (-20.2597, -69.7862),
    },
    "Antofagasta": {
        "Antofagasta": (-23.6509, -70.3975),
        "Calama": (-22.4544, -68.9294),
        "Tocopilla": (-22.0917, -70.1978),
        "San Pedro de Atacama": (-22.9087, -68.1997),
        "Mejillones": (-23.1036, -70.4503),
    },
    "Atacama": {
        "Copiapó": (-27.3668, -70.3323),
        "Vallenar": (-28.5752, -70.7583),
        "Caldera": (-27.0673, -70.8258),
        "Chañaral": (-26.3478, -70.6222),
    },
    "Coquimbo": {
        "La Serena": (-29.9027, -71.2520),
        "Coquimbo": (-29.9533, -71.3436),
        "Ovalle": (-30.5983, -71.2003),
        "Illapel": (-31.6308, -71.1653),
        "Vicuña": (-30.0319, -70.7081),
    },
    "Valparaíso": {
        "Valparaíso": (-33.0472, -71.6127),
        "Viña del Mar": (-33.0245, -71.5518),
        "Quilpué": (-33.0489, -71.4429),
        "Villa Alemana": (-33.0422, -71.3736),
        "Quillota": (-32.8803, -71.2472),
        "San Antonio": (-33.5938, -71.6078),
        "Los Andes": (-32.8336, -70.5983),
        "San Felipe": (-32.7508, -70.7258),
    },
    "Región Metropolitana": {
        "Santiago": (-33.4489, -70.6693),
        "Puente Alto": (-33.6117, -70.5758),
        "Maipú": (-33.5111, -70.7581),
        "Providencia": (-33.4314, -70.6092),
        "Las Condes": (-33.4117, -70.5694),
        "San Bernardo": (-33.5925, -70.7042),
        "Melipilla": (-33.6853, -71.2164),
        "Talagante": (-33.6644, -70.9272),
        "Colina": (-33.2031, -70.6750),
    },
    "O'Higgins": {
        "Rancagua": (-34.1701, -70.7444),
        "Machalí": (-34.1814, -70.6508),
        "San Fernando": (-34.5839, -70.9889),
        "Pichilemu": (-34.3869, -72.0042),
        "Rengo": (-34.4069, -70.8586),
    },
    "Maule": {
        "Talca": (-35.4264, -71.6554),
        "Curicó": (-34.9828, -71.2394),
        "Linares": (-35.8467, -71.5931),
        "Constitución": (-35.3333, -72.4167),
        "Cauquenes": (-35.9672, -72.3158),
    },
    "Ñuble": {
        "Chillán": (-36.6066, -72.1034),
        "San Carlos": (-36.4244, -71.9583),
        "Bulnes": (-36.7422, -72.2986),
    },
    "Biobío": {
        "Concepción": (-36.8270, -73.0503),
        "Talcahuano": (-36.7167, -73.1167),
        "Los Ángeles": (-37.4697, -72.3536),
        "San Pedro de la Paz": (-36.8406, -73.1039),
        "Coronel": (-37.0167, -73.1333),
        "Chillán Viejo": (-36.6231, -72.1311),
    },
    "Araucanía": {
        "Temuco": (-38.7359, -72.5904),
        "Padre Las Casas": (-38.7589, -72.5914),
        "Villarrica": (-39.2833, -72.2333),
        "Pucón": (-39.2817, -71.9750),
        "Angol": (-37.7964, -72.7158),
    },
    "Los Ríos": {
        "Valdivia": (-39.8142, -73.2459),
        "La Unión": (-40.2933, -73.0817),
        "Río Bueno": (-40.3183, -72.9567),
        "Panguipulli": (-39.6433, -72.3325),
    },
    "Los Lagos": {
        "Puerto Montt": (-41.4693, -72.9424),
        "Osorno": (-40.5739, -73.1331),
        "Puerto Varas": (-41.3194, -72.9853),
        "Castro": (-42.4825, -73.7636),
        "Ancud": (-41.8683, -73.8239),
    },
    "Aysén": {
        "Coyhaique": (-45.5752, -72.0662),
        "Puerto Aysén": (-45.4056, -72.6931),
        "Chile Chico": (-46.5408, -71.7258),
    },
    "Magallanes": {
        "Punta Arenas": (-53.1638, -70.9171),
        "Puerto Natales": (-51.7269, -72.5061),
        "Porvenir": (-53.2958, -70.3683),
    },
}


@st.cache_data(ttl=1800)
def obtener_telemetria_completa(lat, lon, ciudad, region):
    url_weather = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,"
        "precipitation,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        "&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,"
        "precipitation_probability,precipitation,rain,weather_code,surface_pressure,visibility,"
        "wind_speed_10m,wind_direction_10m,uv_index"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum"
        "&timezone=auto"
    )

    url_air_quality = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
        "&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi"
        "&timezone=auto"
    )

    try:
        res_w = requests.get(url_weather, timeout=10).json()
        res_aq = requests.get(url_air_quality, timeout=10).json()

        current = res_w.get("current", {})
        daily = res_w.get("daily", {})
        hourly = res_w.get("hourly", {})
        aq_current = res_aq.get("current", {})

        wmo_code = current.get("weather_code", 0)
        wmo_info = WMO_MAP.get(wmo_code, {"desc": "Desconocido", "type": "sun"})

        df_hourly = pd.DataFrame(hourly)
        if not df_hourly.empty:
            df_hourly["time"] = pd.to_datetime(df_hourly["time"])

        df_daily = pd.DataFrame(daily)
        if not df_daily.empty:
            df_daily["time"] = pd.to_datetime(df_daily["time"])

        vis_meters = hourly.get("visibility", [10000])[0] if hourly.get("visibility") else 10000
        vis_km = round(vis_meters / 1000.0, 1)

        prob_lluvia = hourly.get("precipitation_probability", [0])[0] if hourly.get("precipitation_probability") else 0

        return {
            "ciudad": ciudad,
            "region": region,
            "lat": lat,
            "lon": lon,
            "actual": {
                "temperatura": current.get("temperature_2m"),
                "sensacion": current.get("apparent_temperature"),
                "humedad": current.get("relative_humidity_2m"),
                "presion": current.get("surface_pressure"),
                "viento_velocidad": current.get("wind_speed_10m"),
                "viento_direccion": current.get("wind_direction_10m"),
                "viento_rafagas": current.get("wind_gusts_10m"),
                "precipitacion": current.get("precipitation"),
                "probabilidad_lluvia": prob_lluvia,
                "visibilidad_km": vis_km,
                "es_dia": current.get("is_day", 1),
                "wmo_code": wmo_code,
                "condicion": wmo_info["desc"],
                "tipo_icono": wmo_info["type"],
            },
            "diario": {
                "temp_max": daily.get("temperature_2m_max", [None])[0],
                "temp_min": daily.get("temperature_2m_min", [None])[0],
                "salida_sol": daily.get("sunrise", [""])[0],
                "puesta_sol": daily.get("sunset", [""])[0],
                "uv_max": daily.get("uv_index_max", [None])[0],
                "precipitacion_total": daily.get("precipitation_sum", [None])[0],
            },
            "calidad_aire": {
                "aqi": aq_current.get("us_aqi"),
                "pm2_5": aq_current.get("pm2_5"),
                "pm10": aq_current.get("pm10"),
                "co": aq_current.get("carbon_monoxide"),
                "no2": aq_current.get("nitrogen_dioxide"),
                "so2": aq_current.get("sulphur_dioxide"),
                "o3": aq_current.get("ozone"),
            },
            "df_hourly": df_hourly,
            "df_daily": df_daily,
            "timestamp": datetime.now().strftime("%d/%m/%Y"),
        }
    except Exception as e:
        st.error(f"Error al obtener datos de telemetría: {e}")
        return None