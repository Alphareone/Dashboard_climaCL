import requests
import pandas as pd
import numpy as np

NODOS_CHILE = {
    "Arica / Parinacota": {"region": "Arica y Parinacota", "lat": -18.4783, "lon": -70.3126},
    "Iquique": {"region": "Tarapacá", "lat": -20.2133, "lon": -70.1503},
    "Antofagasta": {"region": "Antofagasta", "lat": -23.6509, "lon": -70.3975},
    "Copiapó": {"region": "Atacama", "lat": -27.3668, "lon": -70.3322},
    "La Serena / Coquimbo": {"region": "Coquimbo", "lat": -29.9533, "lon": -71.3395},
    "Valparaíso / Viña": {"region": "Valparaíso", "lat": -33.0472, "lon": -71.6127},
    "Santiago Center": {"region": "Metropolitana", "lat": -33.4489, "lon": -70.6693},
    "Rancagua": {"region": "O'Higgins", "lat": -34.1701, "lon": -70.7444},
    "Talca": {"region": "Maule", "lat": -35.4264, "lon": -71.6554},
    "Chillán": {"region": "Ñuble", "lat": -36.6066, "lon": -72.1034},
    "Concepción / Talcahuano": {"region": "Biobío", "lat": -36.8270, "lon": -73.0503},
    "Temuco": {"region": "Araucanía", "lat": -38.7359, "lon": -72.5904},
    "Valdivia": {"region": "Los Ríos", "lat": -39.8142, "lon": -73.2459},
    "Puerto Montt": {"region": "Los Lagos", "lat": -41.4693, "lon": -72.9424},
    "Coyhaique": {"region": "Aysén", "lat": -45.5752, "lon": -72.0662},
    "Punta Arenas": {"region": "Magallanes", "lat": -53.1638, "lon": -70.9171}
}

def cargar_telemetria_real(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,surface_pressure,wind_speed_10m,wind_direction_10m,uv_index&hourly=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=America%2FSantiago"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            curr = data.get("current", {})
            hourly = data.get("hourly", {})
            
            temp = curr.get("temperature_2m", 15.0)
            hum = curr.get("relative_humidity_2m", 60)
            sens = curr.get("apparent_temperature", temp)
            wind = curr.get("wind_speed_10m", 10.0)
            press = curr.get("surface_pressure", 1013.25)
            uv = curr.get("uv_index", 0.0)
            precip = curr.get("precipitation", 0.0)

            df_hourly = pd.DataFrame({
                "Hora": [t.split("T")[1][:5] for t in hourly.get("time", [])[:24]],
                "Temp": hourly.get("temperature_2m", [])[:24],
                "Humedad": hourly.get("relative_humidity_2m", [])[:24],
                "Presion": hourly.get("surface_pressure", [])[:24],
                "Viento": hourly.get("wind_speed_10m", [])[:24]
            })

            telemetria = {
                "Temp": temp, "Humedad": hum, "Sensacion": sens,
                "Viento": wind, "Presion": press, "UV": uv,
                "Precip": precip
            }
            return telemetria, df_hourly
    except Exception:
        pass
    
    # Fallback si falla el servicio
    df_fallback = pd.DataFrame({
        "Hora": [f"{h:02d}:00" for h in range(24)],
        "Temp": [15.0]*24, "Humedad": [60]*24, "Presion": [1013.2]*24, "Viento": [10.0]*24
    })
    return {"Temp": 15.0, "Humedad": 60, "Sensacion": 14.5, "Viento": 10.0, "Presion": 1013.25, "UV": 3.0, "Precip": 0.0}, df_fallback

def calcular_indices_operativos(temp, hum, viento, uv):
    a, b = 17.27, 237.7
    alpha = ((a * temp) / (b + temp)) + np.log(hum / 100.0)
    dew_point = np.round((b * alpha) / (a - alpha), 1)
    
    dew_diff = temp - dew_point
    fire_risk_val = dew_diff * (temp + 273.15)
    
    if fire_risk_val < 1000:
        fire_risk, fire_color = "BAJO // SIN ALERTA", "#00FF66"
    elif fire_risk_val < 4000:
        fire_risk, fire_color = "MODERADO // PRECAUCIÓN", "#FFD700"
    else:
        fire_risk, fire_color = "EXTREMO // FUISTE BUENO (ALERTA ROJA)", "#FF0055"

    if temp <= 0:
        frost_risk, frost_color = "HELADA EN PROCESO // PELIGRO", "#00F0FF"
    elif temp <= 3 and hum > 85:
        frost_risk, frost_color = "ALTO RIESGO DE HELADA SECA/BLANCA", "#FFD700"
    else:
        frost_risk, frost_color = "CONDICIÓN NORMAL AGRO", "#00FF66"

    return {
        "PuntoRocio": dew_point,
        "RiesgoIncendio": fire_risk,
        "ColorIncendio": fire_color,
        "RiesgoHelada": frost_risk,
        "ColorHelada": frost_color
    }