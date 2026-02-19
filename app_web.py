import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Pausa Cognitiva", page_icon="🧠", layout="wide")

# --- MEMORIA DE LA APLICACIÓN ---
if "historial" not in st.session_state:
    st.session_state.historial = []
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None
if "toxicidad_actual" not in st.session_state:
    st.session_state.toxicidad_actual = 0

# --- TU LLAVE SECRETA ---
# ACORDATE DE PEGAR TU NUEVA API KEY ACÁ
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def asesor_emocional(texto_usuario, contexto):
    instrucciones_sistema = f"""
    Sos un experto en Psicología Cognitivo-Conductual, Comunicación Asertiva y mediación.
    El usuario está bajo estrés y quiere enviar un mensaje impulsivo en este ámbito: {contexto}.
    
    Tu respuesta DEBE seguir estrictamente este formato:
    
    TOXICIDAD: [Escribe SOLO un número del 1 al 100 indicando el nivel de agresividad]
    
    ### 📊 Análisis de Impacto
    [Breve explicación de cómo recibirá la otra persona este mensaje]
    
    ### 🕵️‍♂️ La Intención Oculta
    [¿Qué necesidad no cubierta hay detrás de este enojo?]
    
    ### 💡 Alternativas Sugeridas
    [Escribe cada opción de forma clara]
    
    **Opción A (Profesional / Formal):**
    [Texto de la opción A]
    
    **Opción B (Empática / Vulnerable):**
    [Texto de la opción B]
    
    **Opción C (Firme pero Respetuosa - Poner límite):**
    [Texto de la opción C]
    
    ### 🤔 Pregunta Socrática
    [Una pregunta corta que invite a la reflexión final]
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=instrucciones_sistema
    )

    try:
        response = model.generate_content(texto_usuario)
        return response.text
    except Exception as e:
        return f"TOXICIDAD: 0\nError de conexión: {e}"

def chequeo_final(texto_borrador):
    instrucciones = "El usuario acaba de reescribir un mensaje impulsivo guiado por tus sugerencias previas. Hacé un chequeo final de 2 o 3 líneas. Decile si logró un tono asertivo, y si hace falta, sugerile un micro-ajuste final de vocabulario para que suene natural pero firme."
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=instrucciones)
    try:
        return model.generate_content(texto_borrador).text
    except Exception as e:
        return "Error al chequear."

# ==========================================
# BARRA LATERAL 
# ==========================================
with st.sidebar:
    st.title("⚙️ Ajustes del Asesor")
    
    st.subheader("1. Entorno del Mensaje")
    st.markdown("¿A quién va dirigido?")
    contexto_elegido = st.selectbox(
        "Seleccioná el contexto:",
        [
            "Ámbito Corporativo / Consultoría",
            "Ámbito Educativo / Académico",
            "Parejas",
            "Familia",
            "Amigos",
            "Proveedores / Clientes",
            "Lectores / Redes Sociales",
            "Otros / Genérico"
        ]
    )
    
    st.divider()
    st.subheader("📚 Historial de la Sesión")
    if st.session_state.historial:
        for i, item in enumerate(st.session_state.historial):
            st.markdown(f"**Caso {i+1}:** _{item['mensaje'][:25]}..._")
    else:
        st.info("Aún no procesaste ningún mensaje.")

# ==========================================
# PANTALLA PRINCIPAL
# ==========================================
st.title("🧠❤️🧘‍♂️ Pausa Anti Impulsividad (PAI)")

# TEXTO ENGANCHADOR (Punto 3)
st.markdown("### Descargá todo acá. Es un espacio seguro.")
st.markdown("Escribí eso que te está quemando la cabeza (y los dedos). Nadie lo va a leer, tu texto no se guarda ni se envía a ninguna parte. **Vomitá el enojo sin filtros, que nosotros le ponemos la pausa y la razón.**")

mensaje_crudo = st.text_area("Tu mensaje en crudo:", height=150, placeholder="Escribí acá todo tu descargo...")

if st.button("Analizar y Reflexionar", type="primary"):
    if mensaje_crudo.strip() == "":
        st.warning("El lienzo está en blanco. Escribí algo primero.")
    else:
        with st.spinner("Decodificando la emoción y cruzando datos..."):
            time.sleep(3) 
            resultado_completo = asesor_emocional(mensaje_crudo, contexto_elegido)
            
            lineas = resultado_completo.split('\n')
            toxicidad = 50
            texto_limpio = ""
            
            for linea in lineas:
                if linea.startswith("TOXICIDAD:"):
                    try: 
                        toxicidad = int(linea.replace("TOXICIDAD:", "").strip())
                    except:
                        pass
                else:
                    texto_limpio += linea + "\n"
            
            # Guardamos en la memoria para que no se borre al usar la segunda caja
            st.session_state.analisis_actual = texto_limpio
            st.session_state.toxicidad_actual = toxicidad
            
            st.session_state.historial.append({
                "mensaje": mensaje_crudo,
                "contexto": contexto_elegido,
                "respuesta": texto_limpio
            })

# MOSTRAR RESULTADOS SI YA SE HIZO EL ANÁLISIS
if st.session_state.analisis_actual:
    st.divider()
    st.subheader(f"🌡️ Termómetro Emocional: {st.session_state.toxicidad_actual}% de Toxicidad")
    st.progress(st.session_state.toxicidad_actual) 
    
    if st.session_state.toxicidad_actual > 75:
        st.error("🚨 ¡ALTO! Este mensaje tiene un alto potencial destructivo para el vínculo.")
    elif st.session_state.toxicidad_actual > 40:
        st.warning("⚠️ Cuidado. Hay una tensión evidente que podría generar un conflicto innecesario.")
    else:
        st.success("✅ Tono manejable, pero vamos a pulirlo para mayor claridad.")
    
    st.markdown(st.session_state.analisis_actual)
    
    # TIP ACTUALIZADO (Punto 4)
    st.info("💡 **Tip para copiar:** Podés seleccionar el texto de la opción que más te guste y copiarlo directamente para llevarlo a tu mail, WhatsApp, chat... o donde quieras.")

    # ==========================================
    # CAJA DE REESCRITURA (Punto 5)
    # ==========================================
    st.divider()
    st.subheader("✍️ Tu Versión Final")
    st.markdown("Armá tu mensaje final tomando las sugerencias, pero **con tus propias palabras y estilo**. Vamos a hacerle un último chequeo antes de que lo envíes.")
    
    borrador_usuario = st.text_area("Escribí tu borrador acá:", height=100)
    
    if st.button("Validar mi versión final"):
        if borrador_usuario.strip() == "":
            st.warning("Escribí tu versión en la caja de arriba para poder chequearla.")
        else:
            with st.spinner("Evaluando el tono final..."):
                devolucion = chequeo_final(borrador_usuario)
                st.success(devolucion)