import requests

def obtener_datos_clima(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature", 
            "precipitation", "weather_code", "wind_speed_10m", "wind_direction_10m",
            "uv_index", "surface_pressure"
        ],
        "hourly": [
            "temperature_2m", "precipitation_probability", "precipitation", "wind_speed_10m"
        ],
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params, timeout=12)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error cargando datos telemétricos: {e}")
        return None

def traducir_codigo_clima(code):
    """Traducción oficial de códigos WMO a estados del tiempo en Chile"""
    codigos = {
        0: ("Despejado / Soleado", "sol"),
        1: ("Principalmente Despejado", "sol_nube"),
        2: ("Parcialmente Nublado", "nube"),
        3: ("Nublado", "nubes"),
        45: ("Neblina en la zona", "neblina"),
        48: ("Neblina con escarcha", "neblina"),
        51: ("Llovizna ligera", "lluvia"),
        53: ("Llovizna moderada", "lluvia"),
        55: ("Llovizna intensa", "lluvia_fuerte"),
        61: ("Lluvia ligera", "lluvia"),
        63: ("Lluvia moderada", "lluvia"),
        65: ("Lluvia intensa", "lluvia_fuerte"),
        71: ("Nieve ligera en cordillera", "nieve"),
        73: ("Nieve moderada", "nieve"),
        80: ("Chubascos aislados", "lluvia"),
        81: ("Chubascos moderados", "lluvia_fuerte"),
        95: ("Tormenta eléctrica en desarrollo", "tormenta")
    }
    return codigos.get(code, ("Condición Estable", "sol_nube"))