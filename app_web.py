import streamlit as st
import google.generativeai as genai
import re

# --- 1. CONFIGURACIÓN DE PÁGINA (PWA Ready) ---
# Al cambiar el ícono a 🧠 y el título a PAI, cuando el usuario
# lo instale en su celu se verá con ese nombre y emoji profesional.
st.set_page_config(
    page_title="PAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Dominio oficial: www.pausaantiimpulsividad.com.ar"
    }
)

# --- 2. PULIDO ESTÉTICO (Concepto 'Ma') ---
# Ajustamos los márgenes para dar aire y usamos una tipografía limpia.
st.markdown("""
<style>
    /* Concepto 'Ma': Espacios amplios y calma visual */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 900px;
    }
    
    /* Tipografía para lectura pausada */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    .sidebar-bio {
        font-size: 0.95rem;
        color: #4a4a4a;
        line-height: 1.6;
    }

    .blog-btn {
        display: block; 
        padding: 0.85rem; 
        background-color: #f8f9fa; 
        border: 1px solid #ddd; 
        border-radius: 8px; 
        text-decoration: none; 
        color: #333 !important; 
        text-align: center;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (Identidad) ---
with st.sidebar:
    st.header("🧠 PAI")
    st.markdown("### El Autor")
    st.markdown("""
    <div class='sidebar-bio'>
        Diseñado por <b>Javier E. Giangreco</b>.<br><br>
        <ul style="padding-left: 20px;">
            <li><b>Profesor</b> de Filosofía, Psicología y Lógica.</li>
            <li><b>Licenciado</b> en Educación (Gestión).</li>
            <li><b>Ingeniero de Criterio</b> en la intersección Humano-IA.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <a href="https://javiergiangreco.substack.com/" target="_blank" class="blog-btn">
        ✍️ Leé la filosofía en el blog <br><b>IA: Inteligencia Artesanal</b>
    </a>
    """, unsafe_allow_html=True)
    st.divider()
    st.caption("🌐 www.pausaantiimpulsividad.com.ar")

# --- 4. CEREBRO DE LA APP ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    st.error("🔒 Error de configuración: Verificá las llaves de seguridad.")

PERSONALIDADES = {
    "Modo Empático (CNV)": "Actuá como experto en Comunicación No Violenta.",
    "Modo Asertivo": "Actuá como experto en comunicación asertiva.",
    "Modo Legal (El Escudo)": "Actuá como asesor legal preventivo.",
    "Modo Socrático (Filosófico)": "Actuá como Sócrates.",
    "Modo Zen (Estoico)": "Actuá como un filósofo estoico.",
    "Modo Espiritual (Católico)": "Actuá desde la espiritualidad cristiana.",
    "Modo Amigo de Fierro (Directo)": "Actuá como un amigo honesto de Buenos Aires (voseo)."
}

# --- 5. INTERFAZ PRINCIPAL ---
st.title("🧠❤️🧘‍♂️ PAI")
st.caption("Pausa Anti Impulsividad")

# --- INYECCIÓN DE IDENTIDAD MÓVIL (Punto 1) ---
# Esto garantiza que en celulares vean quién sos sin buscar la flecha.
with st.expander("📖 Acerca del Autor e Ingeniería de Criterio"):
    st.markdown("""
    Diseñado por **Javier E. Giangreco**. Profesor e Ingeniero de Criterio especializado en la gestión humana asistida por tecnología.
    
    [Visitar el blog **IA: Inteligencia Artesanal**](https://javiergiangreco.substack.com/)
    """)

st.markdown("---")

# Mantenemos los campos de entrada tal como están
c1, c2 = st.columns(2)
with c1:
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, un grupo de WhatsApp...")
    emocion_usuario = st.text_input("🎭 Tu Emoción", placeholder="Ej: Frustración, urgencia...")
with c2:
    contexto = st.text_input("📂 Contexto corto", placeholder="Ej: Me mandó un mail fuera de hora...")
    modo_conciencia = st.selectbox("🧘 Elije tu Filtro", list(PERSONALIDADES.keys()))

st.markdown("---")
mensaje_crudo = st.text_area("Escribí sin filtros tu descarga emocional:", height=150)

# (Aquí continúa tu lógica de análisis y botones que ya funciona genial)
# ... [Lógica de st.button("Analizar con PAI") y semáforo] ...

# --- 6. BLINDAJE LEGAL (Punto 2) ---
# Footer con el disclaimer sugerido por Marie.
st.markdown("---")
st.caption("""
⚠️ **Aviso de Responsabilidad:** PAI es una herramienta de asistencia comunicacional basada en inteligencia artificial. 
Las sugerencias generadas son de carácter orientativo. El accionar final y sus consecuencias son **exclusiva responsabilidad del usuario**. 
No reemplaza el asesoramiento profesional legal o psicológico. **Uso sugerido para mayores de 13 años.**
""")

st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 2rem;'>
    PAI - Pausa Anti Impulsividad © 2026<br>
    Sello de Seguridad: Procesamiento de datos efímero y volátil.
</div>
""", unsafe_allow_html=True)