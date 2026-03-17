import streamlit as st
import google.generativeai as genai
import re

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Dominio oficial: www.pausaantiimpulsividad.com.ar"}
)

# --- 2. ESTILOS Y TRUCOS VISUALES ---
st.markdown("""
    <style>
        /* Concepto 'Ma': Espacios y calma */
        .block-container { padding-top: 1.5rem; max-width: 850px; }
        
        /* OCULTAR EXPANDER EN PC Y MOSTRAR EN MÓVIL */
        @media (min-width: 768px) {
            [data-testid="stExpander"] {
                display: none;
            }
        }

        /* Estilo para la leyenda de privacidad */
        .privacy-note {
            font-size: 0.85rem;
            color: #6c757d;
            font-style: italic;
            margin-bottom: 5px;
        }

        /* Botón del blog unificado */
        .blog-btn {
            display: block; padding: 0.7rem; background-color: #f8f9fa; 
            border: 1px solid #ddd; border-radius: 8px; text-decoration: none; 
            color: #333 !important; text-align: center; font-weight: 500; margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. BARRA LATERAL (Escritorio) ---
with st.sidebar:
    st.header("🧠 PAI")
    st.markdown("### El Autor")
    st.markdown("""
        Diseñado por **Javier E. Giangreco**.
        * **Profesor** de Filosofía, Psicología y Lógica.
        * **Licenciado** en Educación (Gestión).
        * **Ingeniero de Criterio**.
    """)
    st.markdown(f'<a href="https://javiergiangreco.substack.com/" target="_blank" class="blog-btn">✍️ IA: Inteligencia Artesanal</a>', unsafe_allow_html=True)
    st.divider()

# --- 4. CEREBRO IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("Error de conexión.")

PERSONALIDADES = {
    "Modo Empático (CNV)": "Actuá como experto en Comunicación No Violenta.",
    "Modo Asertivo": "Actuá como experto en comunicación asertiva.",
    "Modo Legal (El Escudo)": "Actuá como asesor legal preventivo.",
    "Modo Socrático (Filosófico)": "Actuá como Sócrates.",
    "Modo Zen (Estoico)": "Actuá como un filósofo estoico.",
    "Modo Espiritual (Católico)": "Actuá desde la espiritualidad cristiana.",
    "Modo Amigo de Fierro (Directo)": "Actuá como un amigo honesto de Buenos Aires."
}

# --- 5. INTERFAZ PRINCIPAL ---
st.title("🧠❤️🧘‍♂️ PAI")
st.caption("Pausa Anti Impulsividad")

# --- EXPANDER (Solo visible en móvil, texto idéntico a la barra lateral) ---
with st.expander("👤 Acerca del Autor"):
    st.markdown("""
        Diseñado por **Javier E. Giangreco**.
        * **Profesor** de Filosofía, Psicología y Lógica.
        * **Licenciado** en Educación (Gestión).
        * **Ingeniero de Criterio**.
    """)
    st.markdown(f'<a href="https://javiergiangreco.substack.com/" target="_blank" class="blog-btn">✍️ IA: Inteligencia Artesanal</a>', unsafe_allow_html=True)

st.markdown("---")

# --- CAMPOS DE ENTRADA ---
c1, c2 = st.columns(2)
with c1:
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, un grupo...")
    emocion = st.text_input("🎭 Tu Emoción", placeholder="Ej: Frustración, enojo...")
with c2:
    contexto = st.text_input("📂 Contexto corto", placeholder="Ej: Mail fuera de hora...")
    filtro = st.selectbox("🧘 Elije tu Filtro", list(PERSONALIDADES.keys()))

st.markdown("---")

# --- LEYENDA DE PRIVACIDAD ---
st.markdown('<p class="privacy-note">🔒 Garantía de Privacidad: Tu mensaje se procesa de forma efímera; no guardamos registro de lo que escribís.</p>', unsafe_allow_html=True)

mensaje_crudo = st.text_area("Escribí acá tu descarga sin filtros:", height=150)

# (Lógica de análisis que ya tenés armada...)
# st.button("Analizar con PAI")...

# --- 6. FOOTER LEGAL ---
st.markdown("---")
st.caption("""
⚠️ **Aviso de Responsabilidad:** PAI es una herramienta orientativa basada en IA. El accionar final es **exclusiva responsabilidad del usuario**. 
No reemplaza asesoramiento profesional. **Uso sugerido para mayores de 13 años.**
""")