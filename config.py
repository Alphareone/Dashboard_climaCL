import streamlit as st

def aplicar_estilos_base():
    st.markdown("""
        <style>
        /* Contenedor del fondo animado */
        #ripple-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none; /* Permite hacer click a través del fondo */
            opacity: 0.45; /* Suavidad del efecto */
        }

        /* Capa superior para mantener la legibilidad de la UI */
        .stApp {
            background-color: #0B101D;
            color: #E2E8F0;
            position: relative;
            z-index: 1;
        }

        /* Ocultar elementos nativos */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Estilos Glassmorphic */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        .hero-card {
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.85) 0%, rgba(59, 130, 246, 0.85) 50%, rgba(6, 182, 212, 0.85) 100%);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 24px;
            color: white;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .hero-temp { font-size: 3.8rem; font-weight: 800; line-height: 1; letter-spacing: -1px; }
        .hero-city { font-size: 1.6rem; font-weight: 700; opacity: 0.95; }

        .glass-card {
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 12px 20px -5px rgba(56, 189, 248, 0.15);
        }

        .metric-title { font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
        .metric-num { font-size: 1.6rem; font-weight: 700; color: #F8FAFC; }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
            70% { box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }
            100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
        }
        .live-badge {
            display: inline-block;
            width: 9px;
            height: 9px;
            background-color: #38BDF8;
            border-radius: 50%;
            animation: pulse-glow 2s infinite;
            margin-right: 6px;
        }
        </style>

        <!-- Canvas para las ondas de lluvia -->
        <canvas id="ripple-canvas"></canvas>

        <script>
        (function() {
            const canvas = document.getElementById('ripple-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }
            window.addEventListener('resize', resize);
            resize();

            let ripples = [];

            // Generador de ondas aleatorias estilo gotas de agua
            function addRipple() {
                ripples.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: 1,
                    maxRadius: 40 + Math.random() * 50,
                    alpha: 0.5 + Math.random() * 0.3,
                    speed: 0.6 + Math.random() * 0.8
                });
            }

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Crear ondas periódicamente
                if (Math.random() < 0.04) {
                    addRipple();
                }

                for (let i = 0; i < ripples.length; i++) {
                    let r = ripples[i];
                    ctx.beginPath();
                    ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
                    ctx.strokeStyle = `rgba(56, 189, 248, ${r.alpha})`;
                    ctx.lineWidth = 1.2;
                    ctx.stroke();

                    // Expansión y desvanecimiento progresivo
                    r.radius += r.speed;
                    r.alpha -= (r.speed / r.maxRadius) * 0.6;

                    if (r.alpha <= 0 || r.radius >= r.maxRadius) {
                        ripples.splice(i, 1);
                        i--;
                    }
                }
                requestAnimationFrame(animate);
            }

            animate();
        })();
        </script>
    """, unsafe_allow_html=True)