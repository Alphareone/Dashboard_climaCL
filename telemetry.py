import requests
import pytz
from datetime import datetime

ICON_BASE = "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/"

# Coordenadas y Regiones de Chile
TERRITORIO_CHILE = {
    "Arica y Parinacota": {
        "Arica": {"lat": -18.4783, "lon": -70.3126}
    },
    "Tarapacá": {
        "Iquique": {"lat": -20.2133, "lon": -70.1503}
    },
    "Antofagasta": {
        "Antofagasta": {"lat": -23.6509, "lon": -70.3975},
        "Calama": {"lat": -22.4544, "lon": -68.9292}
    },
    "Atacama": {
        "Copiapó": {"lat": -27.3668, "lon": -70.3323}
    },
    "Coquimbo": {
        "La Serena": {"lat": -29.9027, "lon": -71.2519},
        "Coquimbo": {"lat": -29.9533, "lon": -71.3395}
    },
    "Valparaíso": {
        "Quilpué": {"lat": -33.0486, "lon": -71.4426},
        "Valparaíso": {"lat": -33.0472, "lon": -71.6127},
        "Viña del Mar": {"lat": -33.0245, "lon": -71.5518},
        "Villa Alemana": {"lat": -33.0425, "lon": -71.3736},
        "Quillota": {"lat": -32.8833, "lon": -71.2500}
    },
    "Metropolitana de Santiago": {
        "Santiago (Centro)": {"lat": -33.4489, "lon": -70.6693},
        "Puente Alto": {"lat": -33.6117, "lon": -70.5758},
        "Maipú": {"lat": -33.5111, "lon": -70.7581},
        "Providencia": {"lat": -33.4314, "lon": -70.6093},
        "Las Condes": {"lat": -33.4117, "lon": -70.5806}
    },
    "O'Higgins": {
        "Rancagua": {"lat": -34.1701, "lon": -70.7407}
    },
    "Maule": {
        "Talca": {"lat": -35.4264, "lon": -71.6554},
        "Curicó": {"lat": -34.9828, "lon": -71.2394}
    },
    "Ñuble": {
        "Chillán": {"lat": -36.6063, "lon": -72.1034}
    },
    "Bío Bío": {
        "Concepción": {"lat": -36.8201, "lon": -73.0444},
        "Talcahuano": {"lat": -36.7167, "lon": -73.1167},
        "Los Ángeles": {"lat": -37.4697, "lon": -72.3528}
    },
    "Araucanía": {
        "Temuco": {"lat": -38.7359, "lon": -72.5904},
        "Pucón": {"lat": -39.2817, "lon": -71.9744}
    },
    "Los Ríos": {
        "Valdivia": {"lat": -39.8142, "lon": -73.2459}
    },
    "Los Lagos": {
        "Puerto Montt": {"lat": -41.4693, "lon": -72.9424},
        "Castro": {"lat": -42.4721, "lon": -73.7732}
    },
    "Aysén": {
        "Coyhaique": {"lat": -45.5712, "lon": -72.0685}
    },
    "Magallanes y Antártica Chilena": {
        "Punta Arenas": {"lat": -53.1638, "lon": -70.9171}
    }
}

WMO_MAP = {
    0: {"desc": "Despejado", "icon": "day.svg"},
    1: {"desc": "Algo Nublado", "icon": "cloudy-day-1.svg"},
    2: {"desc": "Parcialmente Nublado", "icon": "cloudy-day-3.svg"},
    3: {"desc": "Nublado", "icon": "cloudy.svg"},
    45: {"desc": "Niebla", "icon": "cloudy.svg"},
    48: {"desc": "Niebla Escarchada", "icon": "cloudy.svg"},
    51: {"desc": "Llovizna Ligera", "icon": "rainy-4.svg"},
    53: {"desc": "Llovizna Moderada", "icon": "rainy-5.svg"},
    55: {"desc": "Llovizna Densa", "icon": "rainy-6.svg"},
    61: {"desc": "Lluvia Débil", "icon": "rainy-4.svg"},
    63: {"desc": "Lluvia Moderada", "icon": "rainy-5.svg"},
    65: {"desc": "Lluvia Fuerte", "icon": "rainy-6.svg"},
    71: {"desc": "Nieve Débil", "icon": "snowy-4.svg"},
    80: {"desc": "Chubascos Débiles", "icon": "rainy-4.svg"},
    81: {"desc": "Chubascos Moderados", "icon": "rainy-5.svg"},
    82: {"desc": "Chubascos Violentos", "icon": "rainy-7.svg"},
    95: {"desc": "Tormenta Eléctrica", "icon": "thunder.svg"}
}

def obtener_telemetria_completa(lat: float, lon: float, comuna: str, region: str):
    try:
        url_meteo = "https://api.open-meteo.com/v1/forecast"
        params_meteo = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m", "relative_humidity_2m", "apparent_temperature",
                "is_day", "precipitation", "weather_code", "surface_pressure",
                "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "uv_index", "visibility"
            ],
            "hourly": ["temperature_2m", "precipitation_probability", "wind_speed_10m"],
            "daily": ["sunrise", "sunset", "temperature_2m_max", "temperature_2m_min", "weather_code"],
            "timezone": "America/Santiago"
        }
        res_meteo = requests.get(url_meteo, params=params_meteo, timeout=10).json()

        url_air = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params_air = {
            "latitude": lat,
            "longitude": lon,
            "current": ["european_aqi", "pm10", "pm2_5"],
            "timezone": "America/Santiago"
        }
        res_air = requests.get(url_air, params=params_air, timeout=10).json()

        curr = res_meteo.get("current", {})
        daily = res_meteo.get("daily", {})
        hourly = res_meteo.get("hourly", {})
        curr_air = res_air.get("current", {})

        es_noche = curr.get("is_day", 1) == 0
        wmo_info = WMO_MAP.get(curr.get("weather_code", 0), {"desc": "Desconocido", "icon": "cloudy.svg"})
        
        nombre_icono = wmo_info["icon"]
        if es_noche and "day" in nombre_icono:
            nombre_icono = nombre_icono.replace("day", "night")

        timezone_cl = pytz.timezone("America/Santiago")
        ahora_cl = datetime.now(timezone_cl)
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        daily_forecast = []
        if "time" in daily:
            for i in range(min(7, len(daily["time"]))):
                f_date = datetime.strptime(daily["time"][i], "%Y-%m-%d")
                w_code = daily["weather_code"][i] if "weather_code" in daily else 0
                w_icon = WMO_MAP.get(w_code, {"icon": "day.svg"})["icon"]
                daily_forecast.append({
                    "day_name": dias_semana[f_date.weekday()][:3],
                    "max_temp": round(daily["temperature_2m_max"][i]),
                    "min_temp": round(daily["temperature_2m_min"][i]),
                    "icon_url": f"{ICON_BASE}{w_icon}"
                })

        return {
            "comuna": comuna,
            "region": region,
            "lat": lat,
            "lon": lon,
            "dia_nombre": dias_semana[ahora_cl.weekday()],
            "temperatura": round(curr.get("temperature_2m", 0.0) or 0.0, 1),
            "sensacion": round(curr.get("apparent_temperature", 0.0) or 0.0, 1),
            "humedad": curr.get("relative_humidity_2m", 0) or 0,
            "presion": round(curr.get("surface_pressure", 0.0) or 0.0, 1),
            "precipitacion": curr.get("precipitation", 0.0) or 0.0,
            "visibilidad": round((curr.get("visibility", 10000) or 10000) / 1000, 1),
            "viento_velo": round(curr.get("wind_speed_10m", 0.0) or 0.0, 1),
            "viento_dir": curr.get("wind_direction_10m", 0) or 0,
            "es_noche": es_noche,
            "uv_index": curr.get("uv_index", 0.0) or 0.0,
            "condicion": wmo_info["desc"],
            "icono_url": f"{ICON_BASE}{nombre_icono}",
            "fecha_actual": ahora_cl.strftime("%d/%m/%Y"),
            "amanecer": daily.get("sunrise", ["--T--"])[0].split("T")[-1] if daily.get("sunrise") else "--:--",
            "atardecer": daily.get("sunset", ["--T--"])[0].split("T")[-1] if daily.get("sunset") else "--:--",
            "temp_max": daily.get("temperature_2m_max", [0])[0] if daily.get("temperature_2m_max") else 0,
            "temp_min": daily.get("temperature_2m_min", [0])[0] if daily.get("temperature_2m_min") else 0,
            "aqi": curr_air.get("european_aqi", 0) or 0,
            "pm2_5": curr_air.get("pm2_5", 0.0) or 0.0,
            "hourly": hourly,
            "daily_forecast": daily_forecast
        }
    except Exception as e:
        print(f"Error procesando telemetría: {e}")
        return None