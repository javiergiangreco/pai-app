import streamlit as st
import google.generativeai as genai
import re  # Sumamos esta herramienta para extraer números sin errores

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PAI - Pausa Anti Impulsividad", page_icon="🧠", layout="wide")

# --- MEMORIA Y ESTADO ---
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None

# --- CONEXIÓN CON LA IA ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# --- PERSONALIDADES ---
PERSONALIDADES = {
    "Modo Zen (Estoico)": "Actuá como un filósofo estoico (Marco Aurelio/Séneca). Enfocáte en lo que el usuario puede controlar, el desapego y la ataraxia.",
    "Modo Legal (El Escudo)": "Actuá como un asesor legal preventivo. Tu prioridad es evitar admisiones de culpa o lenguaje que pueda usarse en contra del usuario.",
    "Modo Socrático (Filosófico)": "Actuá como Sócrates. Tu análisis debe girar en torno a preguntas que obliguen al usuario a cuestionar su propio impulso.",
    "Modo Empático (CNV)": "Actuá como experto en Comunicación No Violenta. Focálizate en expresar sentimientos y necesidades insatisfechas sin juzgar.",
    "Modo Amigo de Fierro (Directo)": "Actuá como un amigo honesto de Buenos Aires. Hablá de 'vos', con tono cercano pero firme ('Che, bajá un cambio')."
}

# --- FUNCIÓN DE CEREBRO ---
def analizar_mensaje(texto, destinatario, contexto, emocion, modo):
    instruccion_modo = PERSONALIDADES[modo]
    prompt_completo = f"""
    {instruccion_modo}
    Analizá este mensaje impulsivo:
    - Destinatario: {destinatario} | Contexto: {contexto} | Emoción: {emocion}
    - Mensaje: {texto}
    
    INSTRUCCIÓN ESTRICTA: No escribas introducciones, ni saludos.
    El valor de TOXICIDAD debe ser ÚNICAMENTE un número del 1 al 100 (sin el símbolo %, sin /100).
    
    Respeta este formato exacto:
    TOXICIDAD: [Número del 1 al 100]
    ### ✨ Semilla de Sabiduría ({modo})
    [Frase pertinente al modo]
    ### 🔬 Diagnóstico del Impulso
    [Explicación]
    ### 🎯 Intención vs. Realidad
    [Análisis]
    ### 💡 Propuesta Sugerida
    **Versión Filtrada:** [Texto sugerido]
    ### 🤔 Pregunta Socrática Final
    [Pregunta de cierre]
    """
    try:
        res = model.generate_content(prompt_completo)
        return res.text
    except Exception as e:
        return f"TOXICIDAD: 0\n🚨 Error: {e}"

# ==========================================
# CUERPO PRINCIPAL (DISEÑO LIMPIO)
# ==========================================

# Fila 1: Título y Sello de Seguridad
col_tit, col_sello = st.columns([2, 1])
with col_tit:
    st.title("🧠❤️🧘‍♂️ PAI")
    st.caption("Pausa Anti Impulsividad")
with col_sello:
    st.write("") 
    st.markdown("<p style='text-align: right; color: gray; font-size: 0.8rem;'>🔒 Sello de Seguridad PAI: Tu privacidad es nuestro compromiso ético</p>", unsafe_allow_html=True)

st.markdown("---")

# Fila 2: Las 4 Preguntas de Configuración
c1, c2 = st.columns(2)
with c1:
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, mi ex...")
    emocion_usuario = st.text_input("🎭 Tu Emoción", placeholder="Ej: Enojo, injusticia...")
with c2:
    contexto = st.text_input("📂 Contexto corto", placeholder="Ej: Me criticó en público...")
    modo_conciencia = st.selectbox("🧘 Elije tu Filtro", list(PERSONALIDADES.keys()))

st.markdown("---")

mensaje_crudo = st.text_area("Escribí sin filtros tu descarga emocional:", height=120)
st.caption("🔒 Tu descarga es efímera: este mensaje se autodestruirá al cerrar la sesión.")

if st.button("Analizar con PAI", type="primary"):
    if not mensaje_crudo.strip():
        st.warning("Escribí algo primero.")
    else:
        with st.spinner(f"Analizando en {modo_conciencia}..."):
            resultado = analizar_mensaje(mensaje_crudo, destinatario, contexto, emocion_usuario, modo_conciencia)
            
            lineas = resultado.split('\n')
            tox = 50
            clean_text = ""
            for l in lineas:
                if "TOXICIDAD" in l.upper():
                    try: 
                        # Magia de Regex: Pesca el primer número real de la oración
                        match = re.search(r'\d+', l)
                        if match:
                            tox = int(match.group())
                            if tox > 100: tox = 100 # Tope visual inquebrantable
                    except: pass
                else: 
                    clean_text += l + "\n"
            
            st.session_state.analisis_actual = {"texto": clean_text.strip(), "tox": tox}

# RESULTADOS
if st.session_state.analisis_actual:
    st.divider()
    tox = st.session_state.analisis_actual["tox"]
    st.subheader(f"🌡️ Nivel de Impulsividad: {tox}%")
    st.progress(tox / 100)
    
    if tox > 70: st.error("🚨 **¡FRENO DE MANO!** El nivel de agresión es peligroso.")
    
    st.markdown(st.session_state.analisis_actual["texto"])
    
    st.divider()
    if st.button("🔄 Nueva Pausa"):
        st.session_state.analisis_actual = None
        st.rerun()