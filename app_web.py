import streamlit as st
import google.generativeai as genai
import time
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PAI - Pausa Anti Impulsividad", page_icon="🧠", layout="wide")

# --- FRASES DE ESPERA LOCALES (Costo cero de cuota) ---
reflexiones = [
    "«La mejor respuesta a la ira es la demora». — Séneca",
    "«Entre el estímulo y la respuesta hay un espacio. En ese espacio reside nuestra libertad». — Viktor Frankl",
    "«Cualquiera puede enfadarse, eso es algo muy sencillo. Pero enfadarse con la persona adecuada... eso no es tan sencillo». — Aristóteles",
    "«Cuando te sientas ofendido por las faltas de otro, vuelve la vista a ti mismo». — Marco Aurelio",
    "«Aferrarse a la ira es como beber veneno y esperar que la otra persona muera». — Buda"
]

# --- MEMORIA Y ESTADO ---
if "historial" not in st.session_state:
    st.session_state.historial = []
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None

# --- CONEXIÓN CON LA IA ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

# --- FUNCIONES DE CEREBRO (AHORA TODO EN 1 SOLA LLAMADA) ---
def analizar_mensaje(texto, destinatario, contexto, emocion):
    prompt_sistema = f"""
    Actuá como un experto en Psicología Vincular y Comunicación No Violenta. 
    Analizá este mensaje impulsivo:
    - Destinatario: {destinatario}
    - Contexto: {contexto}
    - Emoción declarada: {emocion}
    - Mensaje: {texto}
    
    Tu respuesta debe ser educativa y reflexiva, siguiendo este formato:
    
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
        res = model.generate_content(prompt_sistema)
        return res.text
    except Exception as e:
        return f"Error: {e}"

def validar_final(borrador):
    prompt = f"El usuario escribió esta versión final basada en tus consejos: '{borrador}'. Hacé un chequeo de 2 líneas: ¿es asertivo? ¿qué mini ajuste le harías?"
    try:
        res = model.generate_content(prompt)
        return res.text
    except:
        return "Buen trabajo. Recordá que el tono lo es todo."

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("⚙️ Configuración PAI")
    st.write("Personalizá el análisis para que sea más preciso.")
    
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

# ==========================================
# CUERPO PRINCIPAL
# ==========================================
st.title("🧠❤️🧘‍♂️ Pausa Anti Impulsividad (PAI)")
st.markdown("### El espacio entre lo que sentís, lo que decís y lo que hacés")

st.markdown("""
Escribí tu mensaje sin filtros. Este es un lugar seguro de descarga. Nadie va a leerlo, solo vos. Vomitá el enojo sin filtros y hacé catársis, que nosotros le ponemos la pausa, la razón y el corazón.
""")

mensaje_crudo = st.text_area("Escribí sin filtros:", height=150, placeholder="Escribí lo que realmente tenés ganas de decir...")

if st.button("Analizar con PAI", type="primary"):
    if mensaje_crudo.strip() == "":
        st.warning("El campo está vacío. No podemos analizar el silencio.")
    else:
        # Mostramos una reflexión local aleatoria mientras procesa
        placeholder_reflexion = st.empty()
        with st.spinner(" "):
            placeholder_reflexion.info(f"✨ **Pausa Activa:**\n{random.choice(reflexiones)}")
            
            # Acá hacemos UNA sola llamada a la IA (soluciona el error 429 de cuota)
            resultado = analizar_mensaje(mensaje_crudo, destinatario, contexto, emocion_usuario)
            
            # Borramos la frase de espera una vez que termina
            placeholder_reflexion.empty()
            
            lineas = resultado.split('\n')
            tox = 50
            clean_text = ""
            for l in lineas:
                if l.startswith("TOXICIDAD:"):
                    try: tox = int(l.replace("TOXICIDAD:", "").strip())
                    except: pass
                else: clean_text += l + "\n"
            
            st.session_state.analisis_actual = {"texto": clean_text, "tox": tox}

# RESULTADOS
if st.session_state.analisis_actual:
    st.divider()
    tox = st.session_state.analisis_actual["tox"]
    st.subheader(f"🌡️ Nivel de Impulsividad: {tox}%")
    st.progress(tox / 100)
    
    if tox > 70: st.error("🚨 **¡FRENO DE MANO!** El nivel de agresión es alto. No envíes nada todavía.")
    
    st.markdown(st.session_state.analisis_actual["texto"])
    
    st.info("💡 **Tip:** Copiá la opción que más te guste y adaptala a tu voz... o donde quieras.")

    # REESCRITURA FINAL
    st.divider()
    st.subheader("✍️ Tu Versión Final")
    st.write("Tomá lo que te sirvió y armá un mensaje con tus palabras. Vamos a validarlo.")
    borrador = st.text_area("Escribí tu borrador final acá:", height=100)
    
    if st.button("Validar mi mensaje"):
        if borrador:
            with st.spinner("Haciendo el último chequeo..."):
                dev = validar_final(borrador)
                st.success(dev)