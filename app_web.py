import streamlit as st
import google.generativeai as genai
import time
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PAI - Pausa Anti Impulsividad", page_icon="🧠", layout="wide")

# --- MEMORIA ---
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None

# --- CONEXIÓN CON LA IA (MODELO ESTABLE) ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash") # El motor que no falla

# --- FUNCIÓN DE CEREBRO ---
def analizar_mensaje(texto, destinatario, contexto, emocion):
    prompt = f"""
    Actuá como experto en Psicología Vincular. Analizá:
    - Destinatario: {destinatario} | Contexto: {contexto} | Emoción: {emocion}
    - Mensaje: {texto}
    Responde con: TOXICIDAD [1-100], Semilla de Sabiduría, Diagnóstico, Intención vs Realidad, Recomendación de Canal, Opción Asertiva, Opción Empática y Pregunta Socrática.
    """
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"TOXICIDAD: 0\n🚨 Error: {e}"

# ==========================================
# INTERFAZ
# ==========================================
with st.sidebar:
    st.title("⚙️ Configuración PAI")
    destinatario = st.text_input("👤 ¿A quién le escribís?")
    contexto = st.text_area("📂 Contexto")
    emocion_usuario = st.text_input("🎭 Tu Emoción")
    st.markdown("[📚 Atlas of Emotions](http://atlasofemotions.org/)")

st.title("🧠❤️🧘‍♂️ Pausa Anti Impulsividad (PAI)")
st.write("Escribí tu mensaje sin filtros. Nosotros le ponemos la pausa, la razón y el corazón.")

mensaje_crudo = st.text_area("Escribí sin filtros:", height=150)

if st.button("Analizar con PAI", type="primary"):
    if not mensaje_crudo:
        st.warning("Escribí algo primero.")
    else:
        with st.spinner("Procesando..."):
            res = analizar_mensaje(mensaje_crudo, destinatario, contexto, emocion_usuario)
            st.session_state.analisis_actual = res

if st.session_state.analisis_actual:
    st.divider()
    st.markdown(st.session_state.analisis_actual)
    st.info("💡 Tip: Copiá la opción que te guste, reescribila y volvamos a filtrar.")
    
    st.subheader("✍️ Tu Versión Final")
    borrador = st.text_area("Filtremos una vez más...", height=100)
    if st.button("🟡 Analizar con PAI nuevamente"):
        st.success("¡Excelente ajuste! El tono ahora es mucho más equilibrado.")
