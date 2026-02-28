import streamlit as st
import google.generativeai as genai
import re

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PAI - Pausa Anti Impulsividad",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded", # Expandido para mostrar tu Branding
    menu_items={
        'About': "Dominio oficial: www.pausaantiimpulsividad.com.ar"
    }
)

# --- INYECCIÓN CSS (Concepto 'Ma' y Branding) ---
st.markdown("""
<style>
    /* Concepto 'Ma': Espacios amplios, diseño despojado y calmo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 950px; /* Limita el ancho para centrar la lectura y dar aire */
    }
    .sidebar-bio {
        font-size: 0.95rem;
        color: #4a4a4a;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .feedback-box {
        background-color: #ffffff;
        border: 1px solid #eaeaea;
        padding: 2.5rem 2rem;
        border-radius: 8px;
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }
    .mail-btn {
        display: inline-block;
        background-color: #212529;
        color: #ffffff !important;
        padding: 12px 28px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 500;
        margin-top: 15px;
        transition: all 0.2s;
    }
    .mail-btn:hover {
        background-color: #343a40;
        transform: translateY(-2px);
    }
    .corporate-cta {
        margin-top: 4rem;
        padding: 1.5rem 2rem;
        background-color: #f8f9fa;
        border-left: 4px solid #0a66c2; /* Azul LinkedIn */
        border-radius: 4px;
        font-size: 0.95rem;
        color: #333;
    }
    .corporate-cta a {
        color: #0a66c2;
        font-weight: 600;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (Identidad y Propósito) ---
with st.sidebar:
    st.header("🧠 PAI")
    st.markdown("### El Autor")
    st.markdown("""
    <div class='sidebar-bio'>
    Diseñado por <b>Javier E. Giangreco</b>.<br><br>
    Profesor de Filosofía, Psicología y Lógica. Licenciado en Educación con Orientación en Gestión. Ingeniero de Criterio explorando la intersección entre humanidad e inteligencia artificial.
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("✍️ Leé la filosofía detrás de esta app en el blog IA: Inteligencia Artesanal", "https://javiergiangreco.substack.com/", use_container_width=True)
    st.divider()
    st.caption("🌐 www.pausaantiimpulsividad.com.ar")

# --- MEMORIA Y ESTADO ---
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None
if "validacion_final" not in st.session_state:
    st.session_state.validacion_final = None

# --- 3. CONEXIÓN CON LA IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    st.error("🔒 Error de configuración: Verificá las llaves de seguridad.")

# --- 4. TUS 7 MODOS DE CONCIENCIA ---
PERSONALIDADES = {
    "Modo Empático (CNV)": "Actuá como experto en Comunicación No Violenta. Focálizate en expresar necesidades insatisfechas sin juzgar ni atacar.",
    "Modo Asertivo": "Actuá como un experto en comunicación asertiva. Tu objetivo es ser firme y claro en la defensa de tus derechos y límites, pero sin caer en la agresión ni en la pasividad.",
    "Modo Legal (El Escudo)": "Actuá como un asesor legal preventivo. Tu prioridad es que el mensaje no sea usado en contra del usuario en un futuro conflicto.",
    "Modo Socrático (Filosófico)": "Actuá como Sócrates. Tu análisis debe girar en torno a preguntas que obliguen al usuario a encontrar la verdad detrás de su impulso.",
    "Modo Zen (Estoico)": "Actuá como un filósofo estoico. Enfocáte en lo que el usuario puede controlar y en la búsqueda de la ataraxia (paz interior).",
    "Modo Espiritual (Católico)": "Actuá desde la espiritualidad cristiana. Focálizate en la caridad, el perdón, la humildad y la paz del corazón. Recordá la importancia de tratar al otro como a un hermano.",
    "Modo Amigo de Fierro (Directo)": "Actuá como un amigo honesto de Buenos Aires. Tono cercano, 'voseo' y firmeza ('Che, bajá un cambio')."
}

# --- 5. FUNCIONES DE CEREBRO ---
def analizar_mensaje(texto, destinatario, contexto, emocion, modo):
    instruccion_modo = PERSONALIDADES[modo]
    prompt_completo = f"""
    {instruccion_modo}
    Analizá este mensaje impulsivo:
    - Destinatario: {destinatario} | Contexto: {contexto} | Emoción: {emocion}
    - Mensaje: {texto}
    
    INSTRUCCIÓN ESTRICTA: No escribas introducciones.
    El valor de TOXICIDAD debe ser ÚNICAMENTE un número del 1 al 100.
    
    Respeta este formato exacto:
    TOXICIDAD: [Número]
    ### ✨ Semilla de Sabiduría ({modo})
    ### 🔬 Diagnóstico del Impulso
    ### 🎯 Intención vs. Realidad
    ### 💡 Propuesta Sugerida
    **Versión Filtrada:** [Texto sugerido]
    ### 🤔 Pregunta Socrática Final
    """
    res = model.generate_content(prompt_completo)
    return res.text

def validar_final(borrador, modo):
    instruccion_modo = PERSONALIDADES[modo]
    prompt = f"""
    {instruccion_modo} 
    El usuario reescribió su mensaje: '{borrador}'. 
    Analizalo de nuevo. ¿Bajó la toxicidad?
    
    Respeta este formato exacto:
    TOXICIDAD: [Número del 1 al 100]
    ### 📝 Devolución Final
    [Tu feedback breve en 2 líneas]
    """
    return model.generate_content(prompt).text

# ==========================================
# 6. DISEÑO DE INTERFAZ PRINCIPAL
# ==========================================

col_tit, col_sello = st.columns([2, 1])
with col_tit:
    st.title("🧠❤️🧘‍♂️ PAI")
    st.caption("Pausa Anti Impulsividad")
with col_sello:
    st.write("") 
    st.markdown("<p style='text-align: right; color: gray; font-size: 0.8rem;'>🔒 Sello de Seguridad PAI: Tu privacidad es nuestro compromiso ético<br>🌐 www.pausaantiimpulsividad.com.ar</p>", unsafe_allow_html=True)

st.markdown("---")

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
            try:
                resultado = analizar_mensaje(mensaje_crudo, destinatario, contexto, emocion_usuario, modo_conciencia)
                
                lineas = resultado.split('\n')
                tox = 50
                clean_text = ""
                for l in lineas:
                    if "TOXICIDAD" in l.upper():
                        match = re.search(r'\d+', l)
                        if match:
                            tox = int(match.group())
                            if tox > 100: tox = 100
                    else: 
                        clean_text += l + "\n"
                
                st.session_state.analisis_actual = {"texto": clean_text.strip(), "tox": tox}
            
            except Exception:
                st.error("🧘 **PAI está meditando profundamente...**")
                st.info("Hubo una pequeña saturación. Por favor, intentá de nuevo en 5 segundos.")

# --- 7. RESULTADOS Y TALLER DE REESCRITURA ---
if st.session_state.analisis_actual:
    st.divider()
    tox = st.session_state.analisis_actual["tox"]
    st.subheader(f"🌡️ Nivel de Impulsividad: {tox}%")
    st.progress(tox / 100)
    
    texto_analisis = st.session_state.analisis_actual["texto"]
    
    # SEMÁFORO DEL PRIMER ANÁLISIS
    if tox >= 65:
        st.error(f"🚨 **¡FRENO DE MANO! (Nivel Crítico)**\n\n{texto_analisis}")
    elif tox >= 30:
        st.warning(f"⚠️ **Atención (Nivel Medio)**\n\n{texto_analisis}")
    else:
        st.success(f"✅ **Bajo Control (Nivel Saludable)**\n\n{texto_analisis}")
    
    st.info("💡 **Tip:** Copiá la respuesta abajo, reescribila con tu voz, tu tono, tu estilo, y volvamos a filtrarla.")

    st.divider()
    st.subheader("✍️ Tu Versión Final")
    borrador = st.text_area("Escribí tu borrador final acá:", height=100)
    
    if st.button("🟡 Analizar con PAI nuevamente"):
        if borrador.strip():
            with st.spinner("Calculando nueva toxicidad..."):
                try:
                    res_v = validar_final(borrador, modo_conciencia)
                    lineas_v = res_v.split('\n')
                    tox_v = 10
                    clean_v = ""
                    for lv in lineas_v:
                        if "TOXICIDAD" in lv.upper():
                            match_v = re.search(r'\d+', lv)
                            if match_v: 
                                tox_v = int(match_v.group())
                                if tox_v > 100: tox_v = 100
                        else: 
                            clean_v += lv + "\n"
                    st.session_state.validacion_final = {"texto": clean_v.strip(), "tox": tox_v}
                except:
                    st.error("No se pudo completar el segundo chequeo. Intentá de nuevo.")

    # SEMÁFORO DE LA VERSIÓN FINAL
    if st.session_state.validacion_final:
        tv = st.session_state.validacion_final["tox"]
        texto_final = st.session_state.validacion_final["texto"]
        
        st.write(f"📊 **Nuevo Nivel de Impulsividad: {tv}%**")
        st.progress(tv / 100)
        
        if tv >= 65:
            st.error(texto_final)
        elif tv >= 30:
            st.warning(texto_final)
        else:
            st.success(texto_final)

    st.divider()
    
    # --- CAPTURA DE VALOR (Historias Anónimas) ---
    st.markdown("""
    <div class="feedback-box">
        <h4>🔥 ¿PAI te salvó de un incendio emocional hoy?</h4>
        <p style="color: #666; font-size: 0.95rem;">Contanos tu historia de forma 100% anónima para que sigamos diseñando pausas que valgan la pena.</p>
        <a href="mailto:javiergiangreco@gmail.com?subject=PAI%20-%20mensajes&body=¡Hola%20Javier!%20Te%20cuento%20mi%20historia%20anónima%20con%20PAI:%0D%0A%0D%0A" class="mail-btn">✉️ Enviar mi historia</a>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Nueva Pausa"):
        st.session_state.analisis_actual = None
        st.session_state.validacion_final = None
        st.rerun()

# --- 8. CALL TO ACTION CORPORATIVO (Footer Global) ---
st.markdown("""
<div class="corporate-cta">
    🏢 <b>¿Querés implementar una versión personalizada de PAI para la comunicación interna de tu empresa?</b><br> 
    <a href="https://www.linkedin.com/in/javiergiangreco/" target="_blank">Conversemos en LinkedIn.</a>
</div>
""", unsafe_allow_html=True)