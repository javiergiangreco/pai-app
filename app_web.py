import streamlit as st
import google.generativeai as genai
import time
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PAI - Pausa Anti Impulsividad", page_icon="🧠", layout="wide")

# --- MEMORIA Y ESTADO ---
if "historial" not in st.session_state:
    st.session_state.historial = []
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None

# --- CONEXIÓN CON LA IA ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

@st.cache_resource
def obtener_lista_modelos():
    """Lee exactamente qué modelos están disponibles en tu cuenta de Google."""
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
    
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, mi ex, un cliente...")
    contexto = st.text_area("📂 Contexto (¿Qué pasó?)", placeholder="Ej: Me criticó en público, no me contesta hace días...")
    
    st.subheader("🎭 Tu Emoción")
    emocion_usuario = st.text_input("¿Cómo te sentís?", placeholder="Ej: Enojo, frustración, tristeza, injusticia...")
    
    with st.expander("📚 Diccionario de Emociones"):
        st.markdown("""
        **Enojo:** Respuesta a un obstáculo o injusticia.
        **Frustración:** Cuando algo no sale como esperabas.
        **Decepción:** Falla en tus expectativas sobre el otro.<br><br>
        <a href="http://atlasofemotions.org/" target="_blank">👉 Explorar Atlas of Emotions</a>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.subheader("🛠️ Panel de Diagnóstico")
    st.write("Elegí el motor a usar:")
    motor_seleccionado = st.selectbox("Motores disponibles:", modelos_disponibles)

# --- FUNCIONES DE CEREBRO ---
def analizar_mensaje(texto, destinatario, contexto, emocion, motor):
    model = genai.GenerativeModel(motor)
    
    prompt_completo = f"""
    Actuá como un experto en Psicología Vincular y Comunicación No Violenta. 
    Analizá este mensaje impulsivo:
    - Destinatario: {destinatario}
    - Contexto: {contexto}
    - Emoción declarada: {emocion}
    - Mensaje: {texto}
    
    INSTRUCCIÓN ESTRICTA: No escribas NINGUNA introducción amable ni saludos. 
    Tu respuesta debe empezar directamente con la línea de TOXICIDAD.
    
    Sigue exactamente este formato:
    
    TOXICIDAD: [Número del 1 al 100]
    
    ### ✨ Semilla de Sabiduría Personalizada
    [Una sola frase corta de filosofía o psicología que invite a la calma, pertinente a este conflicto].
    
    ### 🔬 Diagnóstico del Impulso
    [Explicá por qué el usuario se siente así y qué sesgo está operando].
    
    ### 🎯 Intención vs. Realidad
    [¿Qué quiere lograr el usuario y qué va a lograr realmente con este mensaje?].
    
    ### 📞 Recomendación de Canal
    [¿WhatsApp, Mail o Cara a Cara? Explicá por qué].
    
    ### 💡 Propuestas Artesanales
    **Opción Asertiva:** [Texto]
    **Opción Empática:** [Texto]
    
    ### 🤔 Pregunta Socrática
    [Una pregunta final para cerrar el proceso de reflexión].
    """
    try:
        res = model.generate_content(prompt_completo)
        return res.text
    except Exception as e:
        return f"TOXICIDAD: 0\n🚨 Error de sistema con el motor {motor}:\n{e}\n\n👉 Por favor, elegí otro motor en la barra lateral e intentá de nuevo."

def validar_final(borrador, motor):
    model = genai.GenerativeModel(motor)
    prompt = f"El usuario escribió esta versión final: '{borrador}'. Hacé un chequeo de 2 líneas: ¿es asertivo? ¿qué mini ajuste le harías?"
    try:
        return model.generate_content(prompt).text
    except:
        return "Buen trabajo. Recordá que el tono lo es todo."

# ==========================================
# CUERPO PRINCIPAL
# ==========================================
st.title("🧠❤️🧘‍♂️ Pausa Anti Impulsividad (PAI)")
st.markdown("### El espacio entre lo que sentís, lo que decís y lo que hacés")

# --- AVISO CLAVE PARA CELULARES ---
st.info("📱 **¿Estás en el celular?** Tocá la flechita **`>`** arriba a la izquierda para configurar a quién le escribís y qué sentís antes de analizar.")

st.markdown("""
Escribí tu mensaje sin filtros. Este es un lugar seguro de descarga. Nadie va a leerlo, solo vos. Vomitá el enojo sin filtros y hacé catársis, que nosotros le ponemos la pausa, la razón y el corazón.
""")

mensaje_crudo = st.text_area("Escribí sin filtros:", height=150, placeholder="Escribí lo que realmente tenés ganas de decir...")

if st.button("Analizar con PAI", type="primary"):
    if mensaje_crudo.strip() == "":
        st.warning("El campo está vacío. No podemos analizar el silencio.")
    else:
        with st.spinner("Analizando con el motor seleccionado..."):
            resultado = analizar_mensaje(mensaje_crudo, destinatario, contexto, emocion_usuario, motor_seleccionado)
            
            lineas = resultado.split('\n')
            tox = 50
            clean_text = ""
            for l in lineas:
                if "TOXICIDAD" in l.upper():
                    try: 
                        tox = int(''.join(filter(str.isdigit, l)))
                        if tox > 100: tox = 100
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
    
    if tox > 70: st.error("🚨 **¡FRENO DE MANO!** El nivel de agresión es alto. No envíes nada todavía.")
    
    st.markdown(st.session_state.analisis_actual["texto"])
    
    st.info("💡 **Tip:** Copiá la opción que más te guste, reescribila con tus palabras, y volvamos a filtrar el mensaje.")

    # REESCRITURA FINAL
    st.divider()
    st.subheader("✍️ Tu Versión Final")
    st.write("Filtremos una vez más...")
    
    borrador = st.text_area("Escribí tu borrador final acá:", height=100)
    
    if st.button("🟡 Analizar con PAI nuevamente"):
        if borrador:
            with st.spinner("Haciendo el último chequeo..."):
                dev = validar_final(borrador, motor_seleccionado)
                st.success(dev)