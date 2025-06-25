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
    },
    "Ada Limón": {
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBDNHXvOKhxDw02Wm2gfLfWD12e24_LqJw8A&s",
        "bio": (
            "Ada Limón es una poeta estadounidense contemporánea, reconocida por su estilo lírico y accesible, "
            "que explora con profundidad las complejidades de la experiencia humana cotidiana. "
            "Su obra reflexiona sobre la conexión con la naturaleza, la vulnerabilidad emocional y la resiliencia. "
            "Limón ha recibido numerosos premios y su poesía ha sido alabada por su capacidad para transformar lo mundano "
            "en algo profundamente significativo."
        ),
        "works": {
            "The Carrying": {
                "cover_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVGI-j4qsTk-my2A0Id7N8ZZSRdDcdSSLoxQ&s",
                "fragment": (
                    "Even after all this time, the sun never says to the earth, 'You owe me.'\n"
                    "Look what happens with a love like that,\n"
                    "It lights the whole sky."
                ),
                "comment": (
                    "En este fragmento, Ada Limón utiliza la naturaleza como metáfora para ilustrar el amor incondicional y la generosidad. "
                    "El sol representa una fuerza que da sin esperar nada a cambio, iluminando el mundo entero con su entrega constante. "
                    "La simplicidad del lenguaje oculta una profunda reflexión sobre la bondad y el sacrificio en las relaciones humanas."
                )
            },
            "The Leash": {
                "cover_image": "https://i.pinimg.com/originals/e7/63/90/e763906740a3fb0178e8aec90fa63bfa.png",
                "fragment": (
                    "Tell me about the trees in your childhood.\n"
                    "Tell me about the water.\n"
                    "Tell me about the dirt."
                ),
                "comment": (
                    "En este poema, Ada Limón evoca la conexión profunda con la naturaleza y la memoria, "
                    "pidiendo un regreso a las raíces y al entorno que nos forma. La invitación a hablar de los árboles, el agua y la tierra simboliza "
                    "la búsqueda de identidad y el anclaje emocional en el mundo natural. Es un llamado a reconocer cómo nuestro pasado y entorno moldean "
                    "nuestra experiencia y poesía, revelando una sensibilidad delicada y un aprecio por lo esencial en la vida."
                )
            }
        }
    },
    "Rupi Kaur": {
    "image": "https://www.globalindian.com/wp-content/uploads/2021/07/rupikaur-gallery.jpg",
    "bio": (
        "Rupi Kaur, poeta y artista visual canadiense de origen punjabi, se ha convertido en una voz influyente "
        "en la poesía contemporánea global, especialmente entre los jóvenes. "
        "Su estilo directo, íntimo y poderoso, aborda temas de amor, trauma, feminismo y sanación, "
        "rompiendo esquemas tradicionales de la poesía para acercarla a un público masivo. "
        "Kaur es conocida por sus breves pero impactantes versos, acompañados de ilustraciones propias."
    ),
    "works": {
        "Milk and Honey": {
            "cover_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPXm9A8zSHor87XajiKMfT_DvNZZ0wCt0slA&s",
            "fragment": (
                "I want to apologize to all the women\n"
                "I have called beautiful\n"
                "before I've called them intelligent or brave."
            ),
            "comment": (
                "Este verso desafía las prioridades sociales sobre cómo valoramos a las mujeres, "
                "instando a reconocer y celebrar sus cualidades internas como la inteligencia y el valor, "
                "más allá de los estándares superficiales de belleza. "
                "La poesía de Kaur busca empoderar y sanar a través de un lenguaje accesible y emocionalmente honesto."
            )
        },
     "The Sun and Her Flowers": {
            "cover_image": "https://m.media-amazon.com/images/I/71qQgwFbo+L.jpg",
            "fragment": (
                "you must want to spend the rest of your life with yourself first\n"
                "before you can be with anyone else"
            ),
            "comment": (
                "En este poema, Rupi Kaur profundiza en la importancia del amor propio y la autoaceptación como pilares esenciales para cualquier relación sana. "
                "Nos invita a reflexionar sobre la necesidad de estar en paz con uno mismo antes de poder compartir nuestra vida y amor con otros. "
                "Es un llamado a la introspección y al cuidado personal, resaltando que la relación más duradera y significativa es la que tenemos con nosotros mismos. "
                "Este mensaje conecta con temas universales de sanación, crecimiento personal y empoderamiento, que atraviesan toda su obra."
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
        st.info("Nota: Usa la barra lateral para moverte por las secciones. Esta se activa en la parte superior izquierda con el icono >> y se oculta con <<.")

        with st.expander("Leer más sobre la antología"):
            st.markdown("""
            Esta antología fue creada para acercarte a la literatura contemporánea desde una perspectiva personal y fresca.
            Los autores seleccionados representan diferentes voces y estilos que enriquecen el panorama literario actual.
            Disfruta el recorrido 
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

    # Función para crear imagen de poema (debe ir aquí, no indentada más adentro)
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

    # Poemas
    poema1 = """
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

    poema2 = """
    Eres tan bella como los jardines de la Reina 🌿👑,  
    con la paz que duerme en el lago azul 🌊💤.  
    Tan sabia como Monomon la sabia 🧠✨,  
    única como el Cañón envuelto en su bruma sutil 🌫️🌀.

    Tan especial como todo Hollow Nest 🏰🕷️,  
    un misterio tallado en piedra y luz 🔮🪨.  
    Básicamente, eres perfecta,  
    mi propia leyenda entre sombras y musgo azul 💙🌌
    """

    # Mostrar primer poema
    if "mostrar_poema" not in st.session_state:
        st.session_state.mostrar_poema = False

    boton_poema1 = (
        "🙈 Ocultar poema 'Poema y Poesía ❤️🌹'"
        if st.session_state.mostrar_poema
        else "📝 Mostrar poema 'Poema y Poesía ❤️🌹'"
    )

    if st.button(boton_poema1, key="poema_toggle"):
        st.session_state.mostrar_poema = not st.session_state.mostrar_poema
        st.rerun()

    if st.session_state.mostrar_poema:
        st.markdown("### 🌸 *Poema y Poesía* 🌸")

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

        st.markdown(f"""
        <div class='poema-box'>{poema1.replace('\n', '<br>')}
        <div class='firma'>— Axel Morales 🌹</div>
        </div>
        """, unsafe_allow_html=True)

        poema_img = generar_imagen_poema(poema1)
        buffer = io.BytesIO()
        poema_img.save(buffer, format="PNG")

        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.spinner("⏳ Preparando imagen del poema para descargar..."):
            st.download_button(
                label="📥 Descargar poema como imagen",
                data=buffer.getvalue(),
                file_name="Axel-Morales-poema.png",
                mime="image/png"
            )

        st.markdown("""
        <div class="comentario">
        Este poema refleja la conexión emocional desde un simple saludo hasta el amor profundo.  
        Una carta poética que transmite ternura en cada verso,  
        pero a la vez un amor que no puede ser contenido.
        </div>
        """, unsafe_allow_html=True)


    # Mostrar segundo poema
    if "mostrar_poema2" not in st.session_state:
        st.session_state.mostrar_poema2 = False

    boton_poema2 = (
        "🙈 Ocultar poema 'Leyenda Azul'"
        if st.session_state.mostrar_poema2
        else "📝 Mostrar poema 'Leyenda Azul'"
    )

    if st.button(boton_poema2, key="poema2_toggle"):
        st.session_state.mostrar_poema2 = not st.session_state.mostrar_poema2
        st.rerun()

    if st.session_state.mostrar_poema2:
        st.markdown("### 🌌 *Leyenda Azul* 🌌")

        # Estilos especiales para este poema inspirado en Hollow Knight
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Uncial+Antiqua&display=swap');

        .poema-box {
            background: linear-gradient(135deg, #0b1a2f 0%, #243b55 100%);
            border-left: 5px solid #6a93d1;
            padding: 30px;
            border-radius: 20px;
            font-family: 'Uncial Antiqua', serif;
            font-size: 22px;
            line-height: 1.7;
            color: #cbd6f7;
            box-shadow: 0 0 15px 3px rgba(106, 147, 209, 0.5);
            transition: all 0.4s ease-in-out;
        }

        .firma {
            margin-top: 25px;
            text-align: right;
            font-size: 18px;
            color: #8da1ca;
            font-style: italic;
        }

        .comentario-poema2 {
            margin-top: 20px;
            font-size: 16px;
            font-style: italic;
            color: #a0aec0;
            max-width: 600px;
            background: rgba(15, 25, 45, 0.6);
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid #49638f;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='poema-box'>{poema2.replace('\n', '<br>')}
        <div class='firma'>— Axel Morales 🌙</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='comentario-poema2'>
            Este poema está inspirado en el universo de <em>Hollow Knight</em>, un mundo lleno de misterio, belleza y leyendas ocultas,
            donde la naturaleza y la oscuridad se entrelazan en una danza eterna. Cada verso busca capturar la esencia de sus paisajes
            sombríos y encantadores, y la sensación de una leyenda que trasciende el tiempo y el espacio.
        </div>
        """, unsafe_allow_html=True)

    # Si ninguno está abierto, muestra info
    if not st.session_state.mostrar_poema and not st.session_state.mostrar_poema2:
        st.info("Haz clic para mostrar un poema ❤️")


# Pie de página fijo
st.markdown("""
<footer>
    Creado con 💻 por [Axel Orlando Gutierrez Morales] — Junio 2025 |  
    <a href="https://es.wikipedia.org/wiki/Ocean_Vuong" target="_blank">Ocean Vuong</a> | 
    <a href="https://es.wikipedia.org/wiki/Samanta_Schweblin" target="_blank">Samanta Schweblin</a> | 
    <a href="https://es.wikipedia.org/wiki/Javier_Zamora" target="_blank">Javier Zamora</a>
</footer>
""", unsafe_allow_html=True)
