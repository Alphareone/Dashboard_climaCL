Aquí tienes el archivo **`README.md` completo y unificado** en un solo bloque de código de Markdown, listo para copiar y pegar:

```markdown
# 🛰️ Plataforma Integrada de Control y Observación Sensorial

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/)
[![Folium](https://img.shields.io/badge/Folium-Maps-77B900?style=flat-square&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)

Una suite de telemetría, análisis meteorológico y observación ambiental en tiempo real diseñada para el territorio chileno. La plataforma combina métricas atmosféricas, dinámica de vientos, calidad del aire y cartografía interactiva bajo un diseño industrial avanzado tipo *Command Center* (Glassmorphism UI).

---

## 📌 Descripción General

La **Plataforma Integrada de Control y Observación Sensorial** consolida variables meteorológicas críticas y de calidad ambiental en una interfaz unificada y de alto impacto visual. Consume las APIs abiertas de **Open-Meteo** para procesar telemetría de más de **60 comunas y ciudades principales distribuidas en las 16 regiones de Chile**.

---

## ✨ Características Clave

* **🛰️ Telemetría Atmosférica Instantánea:** Monitoreo en tiempo real de temperatura, sensación térmica, humedad relativa, presión barométrica, dirección/velocidad/ráfagas de viento y visibilidad.
* **🌱 Calidad del Aire y Material Particulado:** Medición integrada del índice de calidad del aire (AQI) y concentración de partículas finas ($PM_{2.5}$, $PM_{10}$).
* **🗺️ Cobertura Geográfica de Chile:** Mapeo interactivo en modo oscuro (*CartoDB Dark*) centrado automáticamente en las coordenadas exactas de la estación seleccionada.
* **📈 Análisis de Tendencia Térmica:** Gráficas vectoriales tipo *sparkline* interactivas para rastrear variaciones de temperatura durante las últimas 24 horas.
* **☀️ Ciclo Solar y Radiación:** Visualización del arco solar parabólico con estimación de amanecer, atardecer e índice UV máximo.
* **🔄 Automatización y Caché:** Actualización automática programada cada 30 minutos (`st_autorefresh`) con caché eficiente de 1800 segundos para optimizar el consumo de la API.
* **🎨 UI/UX Personalizada:** Estética *Dark Mode Glassmorphism* con íconos vectoriales SVG animados.

---

## 🛠️ Stack Tecnológico

| Capa / Módulo | Tecnología Utilizada |
| :--- | :--- |
| **Lenguaje Base** | Python 3.14 |
| **Frontend & UI** | Streamlit + Custom HTML5 / CSS3 (Glassmorphism) |
| **Visualización de Datos** | Plotly (Gráficos) + Folium / Streamlit-Folium (Mapas) |
| **Procesamiento de Datos** | Pandas |
| **Proveedores de Telemetría** | Open-Meteo Weather API & Air Quality API |
| **Control de Frecuencia** | Streamlit Autorefresh |

---

## 📂 Estructura del Proyecto

```text
Dashboard_climaCL/
├── app.py              # Punto de entrada principal y configuración del Sidebar
├── telemetry.py        # Módulo de integración con APIs, caché y catálogo de Chile
├── ui_skyform.py       # Renderizado de componentes UI, estilos CSS e íconos SVG
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

Desarrollado por **[Alfredo Castro Alarcón ](https://github.com/Alphareone)** — *Plataforma Integrada de Control y Observación Sensorial.*

```

```