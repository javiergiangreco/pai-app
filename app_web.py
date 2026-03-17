import streamlit as st
import google.generativeai as genai
import re

# --- 1. CONFIGURACIÓN DE PÁGINA (Identidad PWA) ---
# Al poner PAI y el emoji 🧠, así se verá cuando lo instalen en el celu.
st.set_page_config(
    page_title="PAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Dominio oficial: www.pausaantiimpulsividad.com.ar"}
)

# --- 2. ESTILOS Y TRUCOS VISUALES (El 'Ma' y Mobile Check) ---
st.markdown("""
    <style>
        /* Concepto 'Ma': Espacios y calma */
        .block-container { padding-top: 1.5rem; max-width: 850px; }
        
        /* OCULTAR EN PC Y MOSTRAR EN MÓVIL (Punto 1) */
        .mobile-only { display: none; }
        @media (max-width: 768px) {
            .mobile-only { display: block; margin-bottom: 20px; }
        }

        /* Estilo para la leyenda de privacidad (Punto 4) */
        .privacy-note {
            font-size: 0.85rem;
            color: #6c757d;
            font-style: italic;
            margin-bottom: 5px;
        }

        /* Botón del blog en la barra lateral */
        .blog-btn {
            display: block; padding: 0.7rem; background-color: #f8f9fa; 
            border: 1px solid #ddd; border-radius: 8px; text-decoration: none; 
            color: #333 !important; text-align: center; font-weight: 500;
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
    # Instrucción para instalar como App (Punto 3)
    st.caption("📲 **Instalá PAI:** En tu celu, tocá los 3 puntos del navegador y seleccioná 'Instalar' o 'Agregar a inicio'.")

# --- 4. CEREBRO IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash") # Usamos 1.5 por estabilidad
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

# CONTENEDOR MÓVIL (Punto 1)
st.markdown('<div class="mobile-only">', unsafe_allow_html=True)
with st.expander("👤 Acerca del Autor"):
    st.markdown("""
        Diseñado por **Javier E. Giangreco**.
        * Profesor e Ingeniero de Criterio.
        * [IA: Inteligencia Artesanal](https://javiergiangreco.substack.com/)
        * 📲 *Para instalar como app: tocá los 3 puntos del navegador y seleccioná 'Instalar'.*
    """)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Campos de entrada
c1, c2 = st.columns(2)
with c1:
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, un grupo...")
    emocion = st.text_input("🎭 Tu Emoción", placeholder="Ej: Frustración, enojo...")
with c2:
    contexto = st.text_input("📂 Contexto corto", placeholder="Ej: Mail fuera de hora...")
    filtro = st.selectbox("🧘 Elije tu Filtro", list(PERSONALIDADES.keys()))

st.markdown("---")

# LEYENDA DE PRIVACIDAD (Punto 4)
st.markdown('<p class="privacy-note">🔒 Garantía de Privacidad: Tu mensaje se procesa de forma efímera; no guardamos registro de lo que escribís.</p>', unsafe_allow_html=True)

mensaje_crudo = st.text_area("Escribí acá tu descarga sin filtros:", height=150)

# (Lógica de análisis que ya tenés armada...)
# st.button("Analizar con PAI")...

# --- 6. FOOTER LEGAL (Punto 2) ---
st.markdown("---")
st.caption("""
⚠️ **Aviso de Responsabilidad:** PAI es una herramienta orientativa basada en IA. El accionar final es **exclusiva responsabilidad del usuario**. 
No reemplaza asesoramiento profesional. **Uso sugerido para mayores de 13 años.**
""")