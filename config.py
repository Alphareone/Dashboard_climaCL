import streamlit as st

def load_css(theme_mode):
    if theme_mode == "Oscuro Cyberpunk":
        bg_color = "#080D1A"
        panel_bg = "#0F172A"
        border_color = "#1E293B"
        text_color = "#E2E8F0"
        accent_blue = "#00F0FF"
        accent_green = "#00FF66"
    else:
        bg_color = "#F8FAFC"
        panel_bg = "#FFFFFF"
        border_color = "#E2E8F0"
        text_color = "#0F172A"
        accent_blue = "#0284C7"
        accent_green = "#16A34A"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@600;800;900&display=swap');

    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'JetBrains Mono', monospace;
    }}

    .cyber-panel {{
        background: {panel_bg};
        border: 1px solid {border_color};
        border-left: 4px solid {accent_blue};
        padding: 16px;
        border-radius: 4px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    .cyber-panel-green {{
        background: {panel_bg};
        border: 1px solid {border_color};
        border-left: 4px solid {accent_green};
        padding: 16px;
        border-radius: 4px;
        margin-bottom: 12px;
    }}

    .panel-tag {{
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: {accent_blue};
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}

    .panel-tag-green {{
        color: {accent_green};
    }}

    .metric-big {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        line-height: 1;
        margin: 4px 0;
    }}

    .unit-label {{
        font-size: 0.9rem;
        font-weight: 400;
        margin-left: 4px;
        opacity: 0.8;
    }}

    .sub-status {{
        font-size: 0.75rem;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        margin-top: 6px;
    }}

    .live-dot {{
        height: 8px;
        width: 8px;
        background-color: {accent_green};
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px {accent_green};
        animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
        0% {{ transform: scale(0.95); opacity: 0.8; }}
        50% {{ transform: scale(1.2); opacity: 1; }}
        100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)