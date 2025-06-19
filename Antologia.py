import streamlit as st
from collections import Counter
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# Configuración general
st.set_page_config(page_title="Antología Contemporánea", layout="wide", page_icon="📘")

# Estilos personalizados (tema dark + animaciones)
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #f1f1f1;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.block-container {
    padding-top: 2rem;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}
h1, h2, h3 {
    color: #00ffd5;
    text-shadow: 0 0 6px #00ffd5;
}
.fragmento {
    background-color: #1f1f1f;
    padding: 1rem 1.5rem;
    border-left: 5px solid #00ffd5;
    border-radius: 10px;
    font-style: italic;
    margin-bottom: 1rem;
    transition: background-color 0.4s ease;
}
.fragmento:hover {
    background-color: #272727;
}
.comentario {
    background-color: #2a2a2a;
    padding: 0.8rem 1.2rem;
    border-left: 5px solid #ff0057;
    border-radius: 10px;
    margin-bottom: 2rem;
    font-size: 0.95rem;
}
.sidebar .sidebar-content {
    background-color: #181818;
    color: #00ffd5;
}
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #181818;
    color: #888;
    font-size: 0.9rem;
    text-align: center;
    padding: 8px 0;
    border-top: 1px solid #333;
    z-index: 999;
}
a {
    color: #00ffd5;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Datos de autores y fragmentos (tu data original aquí, omitida para brevedad)
authors = {
    "Ocean Vuong": {
        "image": "https://cdn.zendalibros.com/wp-content/uploads/ocean-vuong.jpg",
        "bio": (
            "Ocean Vuong (1988) es un poeta y novelista vietnamita-estadounidense cuya obra ha recibido "
            "numerosos premios internacionales. Su escritura explora temas complejos como la identidad "
            "racial y sexual, la experiencia migrante y el trauma intergeneracional. Su voz es reconocida "
            "por su lirismo delicado y una sensibilidad profunda hacia la memoria y la pérdida."
        ),
        "works": {
            "On Earth We're Briefly Gorgeous": {
                "cover_image": "https://th.bing.com/th/id/OIP.GBd636f3nRHhv3T9gkiS_gHaLH?rs=1&pid=ImgDetMain",
                "fragment": (
                    "I am writing because they told me to never start a sentence with because. "
                    "But I wasn’t trying to make a sentence — I was trying to break free."
                ),
                "comment": (
                    "Este fragmento ejemplifica la tensión entre la estructura del lenguaje y la necesidad "
                    "de romper con las convenciones para expresar una experiencia personal y cultural. "
                    "Vuong utiliza esta ruptura gramatical como metáfora de la liberación del "
                    "dolor heredado y la afirmación de su identidad queer y migrante. "
                    "El texto invita a cuestionar normas y encontrar poder en la vulnerabilidad."
                )
            },
            "Someday I'll Love Ocean Vuong": {
                "cover_image": "https://i.ytimg.com/vi/zzW7_QzuCjI/maxresdefault.jpg",
                "fragment": (
                    "Let me hold you in my arms until the bones of your sadness crumble."
                ),
                "comment": (
                    "Este verso destaca la ternura y la sanación como actos de resistencia. "
                    "El poema, escrito en forma de carta, refleja una intimidad que busca abrazar "
                    "el sufrimiento con amor y paciencia. El lenguaje de Vuong es visual y táctil, "
                    "con imágenes que evocan fragilidad pero también una esperanza renovada."
                )
            }
        }
    },
    "Samanta Schweblin": {
        "image": "https://th.bing.com/th/id/OIP.wlSnsIoUxUAtGWrKxGOxVQHaFF?rs=1&pid=ImgDetMain",
        "bio": (
            "Samanta Schweblin es una escritora argentina contemporánea conocida por sus cuentos y novelas "
            "que combinan el realismo con elementos fantásticos, de horror y ciencia ficción. "
            "Su obra explora las inquietudes psicológicas y sociales, creando atmósferas cargadas de tensión "
            "y misterio que atrapan al lector y cuestionan la realidad."
        ),
        "works": {
            "Distancia de rescate": {
                "cover_image": "https://sorpresaysuspense.com/wp-content/uploads/2021/05/distancia-de-rescate-cabecera-3.jpg",
                "fragment": "Hay algo importante — algo muy grave — que está por suceder.",
                "comment": (
                    "Esta frase, breve pero poderosa, genera una sensación de inminencia y peligro. "
                    "La novela explora la paranoia ambiental y familiar, mezclando lo cotidiano "
                    "con lo extraño. Schweblin usa un lenguaje directo y preciso que intensifica la atmósfera "
                    "de suspense y amenaza invisible, reflejando ansiedades modernas sobre la fragilidad del mundo."
                )
            },
            "Kentukis": {
                "cover_image": "https://th.bing.com/th/id/R.adf77cd6e6f88ede2f99ea8c35c1463c?rik=Pt00udpb2rIiOA&pid=ImgRaw&r=0",
                "fragment": "La distancia entre lo que somos y lo que miramos puede ser una prisión.",
                "comment": (
                    "En 'Kentukis', Schweblin aborda la vigilancia y la desconexión emocional en la era digital. "
                    "Esta frase subraya cómo la tecnología, lejos de acercarnos, puede alejarnos de nuestra esencia y "
                    "de los otros. La novela pone en cuestión las fronteras entre lo real y lo virtual, lo visible y lo oculto."
                )
            }
        }
    },
    "Javier Zamora": {
        "image": "https://media-cldnry.s-nbcnews.com/image/upload/t_social_share_1200x630_center,f_auto,q_auto:best/mpx/2704722219/2022_09/tdy_javier_hh_220928-qr88yz.jpg",
        "bio": (
            "Javier Zamora es un poeta salvadoreño-estadounidense cuya obra refleja la experiencia migrante "
            "con un tono íntimo y desgarrador. Su poesía aborda temas de frontera, desplazamiento, memoria y familia, "
            "creando una narrativa que visibiliza el dolor y la resistencia de quienes buscan un nuevo hogar."
        ),
        "works": {
            "Unaccompanied": {
                "cover_image": "https://th.bing.com/th/id/OIP.tfIxFVtdCLJgltB3J2a0qQHaEK?rs=1&pid=ImgDetMain",
                "fragment": "I left my name behind... buried beneath the soles of my shoes.",
                "comment": (
                    "Este verso evoca la pérdida y el olvido que sufren muchos migrantes, quienes "
                    "a menudo deben abandonar no solo su tierra sino también su identidad y pasado. "
                    "Zamora utiliza la metáfora del nombre enterrado para reflejar cómo el desplazamiento "
                    "puede despojar de la propia historia, pero también la posibilidad de reconstrucción."
                )
            },
            "Nostalgia": {
                "cover_image": "https://imagenes.elpais.com/resizer/v2/DGRHBBTNMZCI5KPPTO6AT7GF6U.jpg?auth=7ce2181321ca51deaaaae871f9a95dda6de00c724eead442eba8ea5fc3b4f0e5&width=414",
                "fragment": "El viento sabe mi historia, y la repite con voces que nadie escucha.",
                "comment": (
                    "La nostalgia y la memoria son elementos centrales en la poesía de Zamora. "
                    "Aquí, el viento representa la transmisión invisible de las historias personales y colectivas, "
                    "que permanecen aún cuando parecen olvidadas. Su obra recuerda la persistencia del exilio y la necesidad "
                    "de ser escuchado para sanar."
                )
            }
        }
    }
}

# Análisis simple
def analyze_fragment(text):
    words = text.lower().replace("—", " ").replace(".", " ").replace(",", " ").split()
    common_words = Counter(words).most_common(5)
    return common_words

# Estilos personalizados para la sidebar
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        background-color: #1c1c1c;
        color: #f5f5f5;
        padding: 20px;
    }
    .sidebar-title {
        font-size: 26px;
        font-weight: bold;
        color: #4FC3F7;
        margin-bottom: 15px;
    }
    .sidebar-info {
        font-size: 15px;
        color: #B0BEC5;
        margin-top: 10px;
        padding: 10px;
        background-color: #263238;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar mejorada
st.sidebar.markdown('<div class="sidebar-title">📘 Antología</div>', unsafe_allow_html=True)

# 🔧 Siempre al inicio del script (antes de usar `st.session_state.section`)
if "section" not in st.session_state:
    st.session_state.section = "🏠 Portada"  # o cualquier valor predeterminado

# Navegación que cambia el valor del estado
new_selection = st.sidebar.radio(
    "📌 Navegación:",
    options=["🏠 Portada", "👩‍🎓 Autores", "📖 Fragmentos", "✍️ Texto creativo"],
    index=["🏠 Portada", "👩‍🎓 Autores", "📖 Fragmentos", "✍️ Texto creativo"].index(st.session_state.section)
)

# Actualizar si hay cambio de sección
if new_selection != st.session_state.section:
    st.session_state.section = new_selection
    st.rerun()  # <== Cambiado aquí


# Botón para volver a portada
if st.session_state.section != "🏠 Portada":
    if st.sidebar.button("🔙 Volver a Portada"):
        st.session_state.section = "🏠 Portada"
        st.rerun()  # <== Cambiado aquí

if st.session_state.section == "🏠 Portada":
    st.title("📘 Antología de Literatura Contemporánea")
    st.write("_Por: Axel Orlando Gutierrez Morales_")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("¿Qué encontrarás aquí?")
        st.markdown("""
        - **Biografías**: Descubre la vida y obra de tres autores contemporáneos.
        - **Fragmentos Literarios**: Explora textos que abordan temas actuales.
        - **Comentarios Personales**: Reflexiones que acompañan cada fragmento.
        - **Texto Creativo**: Poesía original que expresa emociones actuales.
        """)
        st.info("Nota: Usa la barra lateral para moverte por las secciones.")

        with st.expander("Leer más sobre la antología"):
            st.markdown("""
            Esta antología fue creada para acercarte a la literatura contemporánea desde una perspectiva personal y fresca.
            Los autores seleccionados representan diferentes voces y estilos que enriquecen el panorama literario actual.
            """)

    with col2:
        st.image("https://images.unsplash.com/photo-1559557809-e9b6eabeabfc?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Ym9vayUyMHBlbnxlbnwwfHwwfHx8MA%3D%3D",
                 caption="Lectura y literatura", use_container_width=True)

    st.markdown("---")

elif st.session_state.section == "👩‍🎓 Autores":
    for author, data in authors.items():
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(data["image"], width=130, use_container_width=True)
            with cols[1]:
                st.subheader(f"📖 {author}")
                st.write(data["bio"])
                
        st.markdown("---")  # Separador con espacio

    # Opcional: un toque CSS para sombra y borde en cada autor (solo en apps web)
    st.markdown("""
    <style>
        div.stContainer > div.block-container > div[data-testid="stContainer"] > div {
            padding: 10px 15px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgb(0 255 213 / 0.1);
            transition: box-shadow 0.3s ease;
        }
        div.stContainer > div.block-container > div[data-testid="stContainer"] > div:hover {
            box-shadow: 0 8px 24px rgb(0 255 213 / 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

elif st.session_state.section == "📖 Fragmentos":
    st.header("📖 Fragmentos seleccionados")

    author_choice = st.selectbox("Selecciona un autor para ver sus obras:", list(authors.keys()))
    author_data = authors[author_choice]

    st.subheader(author_choice)
    cols_top = st.columns([1,3])
    with cols_top[0]:
        st.image(author_data["image"], width=150, use_container_width=True)
    with cols_top[1]:
        st.write(author_data["bio"])

    st.markdown("---")

    works = author_data["works"]
    work_choice = st.selectbox("Selecciona una obra:", list(works.keys()))
    work_data = works[work_choice]

    st.markdown(f"### {work_choice}")
    if "cover_image" in work_data:
        st.image(work_data["cover_image"], width=180, caption=work_choice)

    with st.expander("Mostrar fragmento y comentario"):
        st.markdown(f'<div class="fragmento">"{work_data["fragment"]}"</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="comentario">{work_data["comment"]}</div>', unsafe_allow_html=True)
        
elif st.session_state.section == "✍️ Texto creativo":
    st.header("📝 Texto creativo personal")

    st.markdown("""
    Este poema explora la experiencia emocional contemporánea de las relaciones afectivas en la era digital, 
    mostrando cómo los sentimientos más profundos pueden nacer de gestos simples y cotidianos.  
    La vulnerabilidad y la ternura son temas universales que siguen siendo relevantes hoy.
    """)

    # Inicializar si no existe
    if "mostrar_poema" not in st.session_state:
        st.session_state.mostrar_poema = False

    # Texto dinámico del botón
    boton_texto = (
        "🙈 Ocultar poema 'Poema y Poesía ❤️🌹'"
        if st.session_state.mostrar_poema
        else "📝 Mostrar poema 'Poema y Poesía ❤️🌹'"
    )

    # Al hacer clic, cambia estado y recarga
    if st.button(boton_texto, key="poema_toggle"):
        st.session_state.mostrar_poema = not st.session_state.mostrar_poema
        st.rerun()  # ✅ NUEVO método (desde Streamlit 1.40+)


    if st.session_state.mostrar_poema:
        st.markdown("### 🌸 *Poema y Poesía* 🌸")

        # Estilos avanzados
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap');

        .poema-box {
            background: linear-gradient(to bottom, #1e1e1e, #2b2b2b);
            border-left: 5px solid #ff6f91;
            padding: 30px;
            border-radius: 15px;
            font-family: 'Dancing Script', cursive;
            font-size: 24px;
            line-height: 1.8;
            color: #f9f4e7;
            transition: all 0.3s ease-in-out;
            animation: fadeIn 1.2s ease-in;
        }

        .firma {
            margin-top: 25px;
            text-align: right;
            font-size: 20px;
            color: #ffd8a9;
        }

        .comentario {
            margin-top: 30px;
            font-size: 16px;
            font-style: italic;
            color: #cccccc;
            max-height: 150px;
            overflow-y: auto;
        }

        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        </style>
        """, unsafe_allow_html=True)

        # Poema como string
        poema = """
        Quien podría imaginar que  
        esto que siento por ti  
        Empezará con tu simple hola 👋  
        Muchas veces suele ser un saludo.

        Pero para mí fue el comienzo de una historia 📖  
        donde el miedo se hizo presente,  
        cautivado por el color de tus ojos, esos  
        ojitos color café ☕, café que te cuida el

        sueño, café que provoca desvelos,  
        en tus ojos brilla el sol ☀️, y en tu sonrisa  
        mi corazón recibe la brisa del viento 🍃.  

        En cada momento,  
        en cada instante te amo más ❤️,  
        y cuando sonríes,  
        mi corazón canta de alegría 🎶.

        Eres una obra para mis ojos 👁️  
        No soy poeta pero lo intento,  
        tu voz es poesía para mi vida.
        """

        # Mostrar HTML del poema
        st.markdown(f"""
        <div class='poema-box'>{poema.replace('\n', '<br>')}
        <div class='firma'>— Axel Morales 🌹</div>
        </div>
        """, unsafe_allow_html=True)

        # ✅ FUNCIÓN para generar imagen
        def generar_imagen_poema(poema, autor="Axel Morales"):
            ancho, alto = 1080, 1350
            imagen = Image.new("RGB", (ancho, alto), color=(30, 30, 30))
            draw = ImageDraw.Draw(imagen)

            try:
                fuente_poema = ImageFont.truetype("arial.ttf", 36)
                fuente_firma = ImageFont.truetype("arial.ttf", 28)
            except:
                fuente_poema = ImageFont.load_default()
                fuente_firma = ImageFont.load_default()

            margen = 60
            y_texto = margen

            for linea in poema.strip().split("\n"):
                draw.text((margen, y_texto), linea.strip(), font=fuente_poema, fill=(250, 240, 230))
                y_texto += 50

            draw.text((ancho - 350, alto - 100), f"— {autor}", font=fuente_firma, fill=(255, 170, 140))
            return imagen

        # Crear imagen del poema
        poema_img = generar_imagen_poema(poema)
        buffer = io.BytesIO()
        poema_img.save(buffer, format="PNG")

        # Separación visual antes del botón
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Mostrar spinner mientras se prepara la descarga
        with st.spinner("⏳ Preparando imagen del poema para descargar..."):
            st.download_button(
                label="📥 Descargar poema como imagen",
                data=buffer.getvalue(),
                file_name="Axel-Morales-poema.png",
                mime="image/png"
            )

        # Comentario final
        st.markdown("""
        <div class="comentario">
        Este poema refleja la conexión emocional desde un simple saludo hasta el amor profundo.  
        Una carta poética que transmite ternura en cada verso,  
        pero a la vez un amor que no puede ser contenido.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Haz clic para mostrar el poema ❤️")
        
# Pie de página fijo
st.markdown("""
<footer>
    Creado con 💻 por [Axel Orlando Gutierrez Morales] — Junio 2025 |  
    <a href="https://es.wikipedia.org/wiki/Ocean_Vuong" target="_blank">Ocean Vuong</a> | 
    <a href="https://es.wikipedia.org/wiki/Samanta_Schweblin" target="_blank">Samanta Schweblin</a> | 
    <a href="https://es.wikipedia.org/wiki/Javier_Zamora" target="_blank">Javier Zamora</a>
</footer>
""", unsafe_allow_html=True)
