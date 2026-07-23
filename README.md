
# 🛰️ Plataforma Integrada de Control y Observación Sensorial

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/)
[![Folium](https://img.shields.io/badge/Folium-Maps-77B900?style=flat-square&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)

Una suite de telemetría, análisis meteorológico y observación ambiental en tiempo real diseñada para el territorio chileno. La plataforma combina métricas atmosféricas, dinámica de vientos, calidad del aire y cartografía interactiva bajo un diseño industrial avanzado estilo **Command Center / Bento Grid Glassmorphism UI**.

---

## 📌 Descripción General

La **Plataforma Integrada de Control y Observación Sensorial** consolida variables meteorológicas críticas, de calidad ambiental y análisis climáticos en una interfaz unificada, totalmente libre de emojis y construida mediante componentes vectoriales SVG puros. Consume las APIs abiertas de **Open-Meteo** para procesar telemetría de más de **60 comunas y ciudades principales distribuidas en las 16 regiones de Chile**.

---

## ✨ Características Clave

* **🛰️ Telemetría Atmosférica Instantánea:** Monitoreo en tiempo real de temperatura, sensación térmica, humedad relativa, presión barométrica, dirección, velocidad y ráfagas de viento, visibilidad y punto de rocío.
* **🌱 Calidad del Aire y Material Particulado:** Medición integrada del índice de calidad del aire (AQI) y concentración de partículas finas ($PM_{2.5}$).
* **📊 Visualización Bento Grid & Métricas Dinámicas:** Layout responsivo modular adaptado al 100% de zoom con selector interactivo de métricas (Temperatura, Precipitaciones, Viento) y micrográficos en vivo (*Sparklines*).
* **⏱️ Pronóstico Horario e Histórico Extendido:** 
  - Carrusel horizontal con el pronóstico de las próximas 24 horas.
  - Pronóstico extendido a 7 días.
  - Gráfico interactivo en Plotly con el histórico de precipitación acumulada en Chile (1970 - Presente).
* **🗺️ Cobertura Geográfica & Ciclo Solar:** Mapeo interactivo en modo oscuro (*CartoDB Dark*) centrado automáticamente en la ubicación seleccionada y seguimiento del ciclo solar (salida/puesta de sol e índice UV).
* **🏛️ Módulo de Impacto Climático (MMA / DMC):** Análisis integrado de vulnerabilidad y cambio climático según la Dirección Meteorológica de Chile y el Ministerio del Medio Ambiente (Horizontes 2010–2040, 2040–2070 y 2070–2100).
* **🔄 Automatización y Caché:** Actualización automática programada cada 30 minutos (`st_autorefresh`) con caché eficiente para optimizar el consumo de la API.
* **🎨 UI/UX SVG Vectorial:** Iconografía basada exclusivamente en código SVG integrado (sin emojis de sistema) para una presentación profesional e impecable en cualquier dispositivo o sistema operativo.

---

## 🛠️ Stack Tecnológico

| Capa / Módulo | Tecnología Utilizada |
| :--- | :--- |
| **Lenguaje Base** | Python 3.10+ |
| **Frontend & UI** | Streamlit + Custom HTML5 / CSS3 / SVG Vectorial |
| **Visualización de Datos** | Plotly (Gráficos) + Folium / Streamlit-Folium (Mapas) |
| **Procesamiento de Datos** | Pandas + NumPy |
| **Proveedores de Telemetría** | Open-Meteo Weather API & Air Quality API |
| **Control de Frecuencia** | Streamlit Autorefresh |

---

## 📂 Estructura del Proyecto

```text
Dashboard_climaCL/
├── app.py              # Punto de entrada principal y configuración de la aplicación
├── telemetry.py        # Módulo de integración con APIs, caché y catálogo de Chile
├── ui_skyform.py       # Renderizado de la UI Bento Grid, componentes SVG y gráficos Plotly
├── config.py           # Estilos base CSS, fuentes y configuración visual
└── requirements.txt    # Dependencias y librerías del proyecto

```

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio y acceder a la carpeta:**

```bash
git clone [https://github.com/Alphareone/Dashboard_climaCL.git](https://github.com/Alphareone/Dashboard_climaCL.git)
cd Dashboard_climaCL

```

2. **Crear y activar un entorno virtual (opcional pero recomendado):**

```bash
python -m venv venv

# En Windows:
.\venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt

```

4. **Lanzar la aplicación:**

```bash
python -m streamlit run app.py

```

---

## ✒️ Autor

Desarrollado por **[Alfredo Castro Alarcón](https://github.com/Alphareone)** — *Plataforma Integrada de Control y Observación Sensorial.*

```

```
