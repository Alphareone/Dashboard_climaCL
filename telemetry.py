import requests

def obtener_datos_clima(lat, lon):
    """
    Obtiene telemetría avanzada de Open-Meteo incluyendo variables
    ciudadanas, agrícolas y de viento.
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
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "uv_index", "wind_speed_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "uv_index_max", "et0_fao_evapotranspiration"],
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error cargando telemetría: {e}")
        return None

def generar_alertas_inteligentes(datos_clima):
    """
    Simulador de IA / Machine Learning que detecta anomalías y emite alertas.
    """
    if not datos_clima or "current" not in datos_clima:
        return []

    curr = datos_clima["current"]
    alertas = []

    # Detección de Viento
    if curr.get("wind_speed_10m", 0) > 35:
        alertas.append({"nivel": "warning", "msg": "⚠️ **Ráfagas Fuertes:** Vientos superiores a 35 km/h detectados."})
    
    # Detección de Radiación UV
    if curr.get("uv_index", 0) >= 8:
        alertas.append({"nivel": "error", "msg": "🚨 **Peligro UV:** Índice UV extremadamente alto. Proteja su piel."})
    
    # Detección de Riesgo de Helada
    if curr.get("temperature_2m", 10) <= 3:
        alertas.append({"nivel": "info", "msg": "❄️ **Alerta Agrícola:** Posibles heladas en las próximas horas."})

    # Detección de Calentamiento / Ola de calor
    if curr.get("temperature_2m", 0) >= 30:
        alertas.append({"nivel": "warning", "msg": "🔥 **Ola de Calor:** Temperatura por encima del promedio confortable."})

    if not alertas:
        alertas.append({"nivel": "success", "msg": "✅ **Condiciones Estables:** No se detectan anomalías meteorológicas de riesgo."})

    return alertas