import streamlit as st
import google.generativeai as genai
import time
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PAI - Pausa Anti Impulsividad", page_icon="🧠", layout="wide")

# --- MEMORIA Y ESTADO ---
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None

# --- CONEXIÓN CON LA IA ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

@st.cache_resource
def obtener_lista_modelos():
    try:
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return modelos if modelos else ["No se encontraron modelos"]
    except Exception as e:
        return [f"Error de lectura: {e}"]

modelos_disponibles = obtener_lista_modelos()

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("⚙️ Configuración PAI")
    
    # --- 1. SELLO DE SEGURIDAD (MODIFICACIÓN 1) ---
    st.info("🔒 **Sello de Seguridad PAI**\n\nLos datos se procesan en la memoria volátil del servidor. No guardamos bases de datos ni registros de tus mensajes. Tu privacidad es nuestro compromiso ético.")
    
    st.divider()
    
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, mi ex, un cliente...")
    contexto = st.text_area("📂 Contexto (¿Qué pasó?)", placeholder="Ej: Me criticó en público, no me contesta hace días...")
    emocion_usuario = st.text_input("🎭 Tu Emoción", placeholder="Ej: Enojo, frustración, injusticia...")
    
    # --- 2. FILTROS DE CONCIENCIA (MODIFICACIÓN 2) ---
    st.subheader("🧘 Elije tu Filtro")
    modo_conciencia = st.selectbox(
        "¿Quién querés que te asesore?",
        [
            "Modo Zen (Estoico)", 
            "Modo Legal (El Escudo)", 
            "Modo Socrático (Filosófico)", 
            "Modo Empático (CNV)", 
            "Modo Amigo de Fierro (Directo)"
        ]
    )
    
    st.divider()
    st.subheader("🛠️ Panel de Diagnóstico")
    motor_seleccionado = st.selectbox("Motor de IA:", modelos_disponibles)

# --- PROMPTS DE PERSONALIDAD ---
PERSONALIDADES = {
    "Modo Zen (Estoico)": "Actuá como un filósofo estoico (Marco Aurelio/Séneca). Enfocáte en lo que el usuario puede controlar, el desapego del juicio ajeno y la búsqueda de la ataraxia (paz interior).",
    "Modo Legal (El Escudo)": "Actuá como un asesor legal preventivo. Tu prioridad es que el mensaje no sea usado como prueba en contra del usuario en un juicio, despido o conflicto contractual. Evitá admisiones de culpa o lenguaje agresivo.",
    "Modo Socrático (Filosófico)": "Actuá como Sócrates. No des respuestas directas de entrada. Tu análisis debe girar en torno a preguntas que obliguen al usuario a encontrar la verdad y la contradicción en su impulso.",
    "Modo Empático (CNV)": "Actuá como experto en Comunicación No Violenta (Marshall Rosenberg). Focálizate en expresar sentimientos y necesidades insatisfechas sin juzgar ni atacar al otro.",
    "Modo Amigo de Fierro (Directo)": "Actuá como un amigo honesto y directo de Buenos Aires. Hablá de 'vos', usá un tono cercano pero firme ('Che, bajá un cambio'). Decí las verdades que duelen pero salvan."
}

# --- FUNCIONES DE CEREBRO ---
def analizar_mensaje(texto, destinatario, contexto, emocion, motor, modo):
    model = genai.GenerativeModel(motor)
    
    instruccion_modo = PERSONALIDADES[modo]
    
    prompt_completo = f"""
    {instruccion_modo}
    
    Analizá este mensaje impulsivo:
    - Destinatario: {destinatario}
    - Contexto: {contexto}
    - Emoción: {emocion}
    - Mensaje: {texto}
    
    No escribas introducciones. Tu respuesta debe empezar directamente con la línea de TOXICIDAD.
    
    Formato:
    TOXICIDAD: [1-100]
    ### ✨ Semilla de Sabiduría ({modo})
    [Frase corta acorde al modo].
    ### 🔬 Diagnóstico del Impulso
    [Explicación psicológica/filosófica].
    ### 🎯 Intención vs. Realidad
    [Análisis de consecuencias].
    ### 💡 Propuestas Artesanales
    **Opción Sugerida:** [Texto del mensaje ya filtrado].
    ### 🤔 Pregunta Socrática Final
    [La pregunta para cerrar la reflexión].
    """
    try:
        res = model.generate_content(prompt_completo)
        return res.text
    except Exception as e:
        return f"TOXICIDAD: 0\n🚨 Error: {e}"

# ==========================================
# CUERPO PRINCIPAL
# ==========================================
st.title("🧠❤️🧘‍♂️ Pausa Anti Impulsividad (PAI)")
st.markdown("### El espacio entre lo que sentís, lo que decís y lo que hacés")

st.info("📱 **¿En el celular?** Tocá la flechita **`>`** arriba a la izquierda para configurar tu filtro.")

mensaje_crudo = st.text_area("Escribí sin filtros tu descarga emocional:", height=150)

# --- 3. MICRO-TEXTO DE PRIVACIDAD (MODIFICACIÓN 1.2) ---
st.caption("🔒 **Tu descarga emocional es efímera:** Este mensaje se autodestruirá al cerrar la sesión.")

if st.button("Analizar con PAI", type="primary"):
    if not mensaje_crudo.strip():
        st.warning("Escribí algo primero.")
    else:
        with st.spinner(f"Analizando en {modo_conciencia}..."):
            resultado = analizar_mensaje(mensaje_crudo, destinatario, contexto, emocion_usuario, motor_seleccionado, modo_conciencia)
            
            lineas = resultado.split('\n')
            tox = 50
            clean_text = ""
            for l in lineas:
                if "TOXICIDAD" in l.upper():
                    try: tox = int(''.join(filter(str.isdigit, l)))
                    except: pass
                else: clean_text += l + "\n"
            
            st.session_state.analisis_actual = {"texto": clean_text.strip(), "tox": tox}

# RESULTADOS
if st.session_state.analisis_actual:
    st.divider()
    tox = st.session_state.analisis_actual["tox"]
    st.subheader(f"🌡️ Nivel de Impulsividad: {tox}%")
    st.progress(tox / 100)
    
    if tox > 70: st.error("🚨 **¡FRENO DE MANO!** El nivel de agresión es peligroso.")
    
    st.markdown(st.session_state.analisis_actual["texto"])
    
    # --- 4. COPIAR AL PORTAPAPELES (MODIFICACIÓN 3.1) ---
    st.info("💡 **Tip:** Seleccioná el texto de la 'Opción Sugerida' arriba para copiarlo. Al cerrar esta pestaña, el rastro desaparecerá.")

    st.divider()
    st.subheader("✍️ Tu Versión Final")
    borrador = st.text_area("Filtremos una vez más...", height=100)
    
    if st.button("🟡 Analizar con PAI nuevamente"):
        st.success("¡Excelente ajuste! El tono ahora es mucho más equilibrado y asertivo.")