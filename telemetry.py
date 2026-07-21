import requests
import pandas as pd

NODOS_CHILE = {
    "Arica": {"region": "Arica y Parinacota", "lat": -18.4783, "lon": -70.3126},
    "Iquique": {"region": "Tarapacá", "lat": -20.2133, "lon": -70.1503},
    "Antofagasta": {"region": "Antofagasta", "lat": -23.6509, "lon": -70.3975},
    "Copiapó": {"region": "Atacama", "lat": -27.3668, "lon": -70.3322},
    "La Serena": {"region": "Coquimbo", "lat": -29.9027, "lon": -71.2520},
    "Valparaíso / Viña": {"region": "Valparaíso", "lat": -33.0472, "lon": -71.6127},
    "Quilpué": {"region": "Valparaíso", "lat": -33.0483, "lon": -71.4428},
    "Santiago": {"region": "Metropolitana", "lat": -33.4489, "lon": -70.6693},
    "Rancagua": {"region": "O'Higgins", "lat": -34.1701, "lon": -70.7444},
    "Talca": {"region": "Maule", "lat": -35.4264, "lon": -71.6554},
    "Concepción": {"region": "Biobío", "lat": -36.8270, "lon": -73.0503},
    "Temuco": {"region": "La Araucanía", "lat": -38.7359, "lon": -72.5904},
    "Puerto Montt": {"region": "Los Lagos", "lat": -41.4693, "lon": -72.9424},
    "Coyhaique": {"region": "Aysén", "lat": -45.5752, "lon": -72.0662},
    "Punta Arenas": {"region": "Magallanes", "lat": -53.1638, "lon": -70.9171}
}

def MapearCondicion(temp, precip, viento):
    if precip > 0.5:
        return "🌧️", "Lluvia"
    elif precip > 0.0:
        return "🌦️", "Llovizna"
    elif viento > 25:
        return "💨", "Viento Fuerte"
    elif temp >= 24:
        return "☀️", "Soleado"
    elif temp <= 5:
        return "❄️", "Helada Zonal"
    else:
        return "⛅", "Parcial"

def obtener_clima_en_vivo(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,surface_pressure,wind_speed_10m,uv_index,visibility&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FSantiago"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            c = data.get("current", {})
            icono, condicion = MapearCondicion(c.get("temperature_2m", 0.0), c.get("precipitation", 0.0), c.get("wind_speed_10m", 0.0))
            
            clima = {
                "temp": c.get("temperature_2m", 0.0),
                "humedad": c.get("relative_humidity_2m", 0),
                "sensacion": c.get("apparent_temperature", 0.0),
                "precip": c.get("precipitation", 0.0),
                "presion": c.get("surface_pressure", 0.0),
                "viento": c.get("wind_speed_10m", 0.0),
                "uv": c.get("uv_index", 0.0),
                "visibilidad": round(c.get("visibility", 10000) / 1000, 1),
                "icono": icono,
                "condicion": condicion
            }
            
            h = data.get("hourly", {})
            df_hourly = pd.DataFrame({
                "Hora": pd.to_datetime(h.get("time", [])[:24]),
                "Temperatura (°C)": h.get("temperature_2m", [])[:24],
                "Humedad (%)": h.get("relative_humidity_2m", [])[:24],
                "Viento (km/h)": h.get("wind_speed_10m", [])[:24]
            })
            
            d = data.get("daily", {})
            df_daily = pd.DataFrame({
                "Fecha": pd.to_datetime(d.get("time", [])),
                "Max": d.get("temperature_2m_max", []),
                "Min": d.get("temperature_2m_min", [])
            })
            
            return clima, df_hourly, df_daily
    except Exception as e:
        print(f"Error API: {e}")
    return None, None, None

def obtener_resumen_red_nodos():
    lats = [str(n["lat"]) for n in NODOS_CHILE.values()]
    lons = [str(n["lon"]) for n in NODOS_CHILE.values()]
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={','.join(lats)}&longitude={','.join(lons)}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&timezone=America%2FSantiago"
    
    lista = []
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            res_data = r.json()
            if not isinstance(res_data, list):
                res_data = [res_data]
                
            for idx, (nombre, info) in enumerate(NODOS_CHILE.items()):
                c = res_data[idx].get("current", {})
                t = c.get("temperature_2m", 0.0)
                p = c.get("precipitation", 0.0)
                v = c.get("wind_speed_10m", 0.0)
                icono, tag = MapearCondicion(t, p, v)
                
                lista.append({
                    "Ciudad": nombre,
                    "Región": info["region"],
                    "lat": info["lat"],
                    "lon": info["lon"],
                    "Temp": t,
                    "Humedad": c.get("relative_humidity_2m", 0),
                    "Viento": v,
                    "Icono": icono,
                    "Condicion": tag,
                    "Etiqueta": f"{icono} {nombre}: {t}°C"
                })
    except Exception as e:
        print(f"Error Red: {e}")
        
    df_resumen = pd.DataFrame(lista)
    if not df_resumen.empty:
        df_resumen["Tamaño_Nodo"] = df_resumen["Temp"].apply(lambda t: float(max(t + 20.0, 5.0)))
        
    return df_resumen