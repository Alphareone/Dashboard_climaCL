import requests
import pandas as pd

def obtener_datos_clima(lat, lon):
    """
    Obtiene telemetría completa de Open-Meteo para monitoreo en tiempo real,
    curva por horas y pronóstico extendido a 7 días.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature", 
            "precipitation", "weather_code", "wind_speed_10m", "wind_direction_10m",
            "uv_index", "et0_fao_evapotranspiration"
        ],
        "hourly": [
            "temperature_2m", "precipitation_probability", "precipitation", "wind_speed_10m"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"
        ],
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error cargando telemetría: {e}")
        return None

def generar_alertas_inteligentes(datos_clima, ciudad):
    """
    Genera banners de alerta de riesgo extremo al estilo Google Weather.
    """
    if not datos_clima or "current" not in datos_clima:
        return []

    curr = datos_clima["current"]
    alertas = []

    # Alerta de Riesgo de Inundación / Lluvia Fuerte
    if curr.get("precipitation", 0) > 5 or datos_clima.get("hourly", {}).get("precipitation", [0])[0] > 5:
        alertas.append({
            "titulo": f"Riesgo de inundación repentina o anegamiento en {ciudad}",
            "msg": "Se registran/esperan lluvias de fuerte intensidad. Las condiciones locales pueden variar.",
            "tipo": "error"
        })
    
    # Alerta de Viento Fuerte
    if curr.get("wind_speed_10m", 0) > 35:
        alertas.append({
            "titulo": f"Alerta por Ráfagas de Viento en {ciudad}",
            "msg": "Vientos superiores a 35 km/h detectados. Precaución con caída de ramas o cortes de suministro.",
            "tipo": "warning"
        })

    # Alerta UV Extremo
    if curr.get("uv_index", 0) >= 8:
        alertas.append({
            "titulo": f"Alerta de Radiación UV Extrema",
            "msg": "Nivel de radiación solar peligroso. Se recomienda evitar exposición prolongada.",
            "tipo": "warning"
        })

    return alertas