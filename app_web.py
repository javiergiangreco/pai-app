import streamlit as st
import google.generativeai as genai
import re

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PAI",
    page_icon="icono.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Dominio oficial: www.pausaantiimpulsividad.com.ar"}
)

# --- 2. ESTILOS Y TRUCOS VISUALES (Concepto 'Ma') ---
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; max-width: 850px; }
        
        /* OCULTAR EXPANDER EN PC Y MOSTRAR EN MÓVIL */
        @media (min-width: 768px) {
            [data-testid="stExpander"] { display: none; }
        }

        .privacy-note {
            font-size: 0.85rem; color: #6c757d; font-style: italic; margin-bottom: 5px;
        }

        .blog-btn {
            display: block; padding: 0.7rem; background-color: #f8f9fa; 
            border: 1px solid #ddd; border-radius: 8px; text-decoration: none; 
            color: #333 !important; text-align: center; font-weight: 500; margin-top: 10px;
        }
        
        .feedback-box {
            background-color: #ffffff; border: 1px solid #eaeaea; padding: 2rem;
            border-radius: 8px; text-align: center; margin-top: 2rem; margin-bottom: 2rem;
        }
        
        .mail-btn {
            display: inline-block; background-color: #212529; color: #ffffff !important;
            padding: 10px 25px; border-radius: 6px; text-decoration: none; font-weight: 500; margin-top: 10px;
        }
        
        .corporate-cta {
            margin-top: 3rem; padding: 1.5rem; background-color: #f8f9fa;
            border-left: 4px solid #0a66c2; border-radius: 4px; font-size: 0.95rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. BARRA LATERAL (Escritorio) ---
with st.sidebar:
    st.image("icono.png", width=100)
    st.markdown("### El Autor")
    st.markdown("""
        Diseñado por **Javier E. Giangreco**.
        * **Profesor** de Filosofía, Psicología y Lógica.
        * **Licenciado** en Educación (Gestión).
        * **Ingeniero de Criterio**.
    """)
    st.markdown(f'<a href="https://javiergiangreco.substack.com/" target="_blank" class="blog-btn">✍️ IA: Inteligencia Artesanal</a>', unsafe_allow_html=True)
    st.divider()
    st.caption("📲 **¿Querés usar PAI como App?** Abrí el menú de tu navegador (⋮) y elegí **'Agregar a la pantalla principal'**.")

# --- MEMORIA Y ESTADO ---
if "analisis_actual" not in st.session_state:
    st.session_state.analisis_actual = None
if "validacion_final" not in st.session_state:
    st.session_state.validacion_final = None

# --- 4. CEREBRO IA Y FUNCIONES ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Volvemos a tu modelo 2.5 original
    model = genai.GenerativeModel("gemini-2.5-flash")
except:
    st.error("Error de conexión con la IA.")

PERSONALIDADES = {
    "Modo Empático (CNV)": "Actuá como experto en Comunicación No Violenta. Focálizate en expresar necesidades insatisfechas sin juzgar ni atacar.",
    "Modo Asertivo": "Actuá como un experto en comunicación asertiva. Tu objetivo es ser firme y claro en la defensa de tus derechos y límites, pero sin caer en la agresión ni en la pasividad.",
    "Modo Legal (El Escudo)": "Actuá como un asesor legal preventivo. Tu prioridad es que el mensaje no sea usado en contra del usuario en un futuro conflicto.",
    "Modo Socrático (Filosófico)": "Actuá como Sócrates. Tu análisis debe girar en torno a preguntas que obliguen al usuario a encontrar la verdad detrás de su impulso.",
    "Modo Zen (Estoico)": "Actuá como un filósofo estoico. Enfocáte en lo que el usuario puede controlar y en la búsqueda de la ataraxia (paz interior).",
    "Modo Espiritual (Católico)": "Actuá desde la espiritualidad cristiana. Focálizate en la caridad, el perdón, la humildad y la paz del corazón. Recordá la importancia de tratar al otro como a un hermano.",
    "Modo Amigo de Fierro (Directo)": "Actuá como un amigo honesto de Buenos Aires. Tono cercano, 'voseo' y firmeza ('Che, bajá un cambio')."
}

# --- APAGAMOS LOS FILTROS DE SEGURIDAD (Sintaxis oficial en lista) ---
CONFIG_SEGURIDAD = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

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
    return model.generate_content(prompt_completo, safety_settings=CONFIG_SEGURIDAD).text

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
    return model.generate_content(prompt, safety_settings=CONFIG_SEGURIDAD).text

# --- 5. INTERFAZ PRINCIPAL ---
col1, col2 = st.columns([1, 10]) # Los números manejan la proporción del espacio
with col1:
    st.image("icono.png", width=60)
with col2:
    st.title("PAI")
st.caption("Pausa Anti Impulsividad")

# EXPANDER MÓVIL (Mismo texto que la barra lateral)
with st.expander("👤 Acerca del Autor"):
    st.image("icono.png", width=70)
    st.markdown("""
        Diseñado por **Javier E. Giangreco**.
        * **Profesor** de Filosofía, Psicología y Lógica.
        * **Licenciado** en Educación (Gestión).
        * **Ingeniero de Criterio**.
    """)
    st.markdown(f'<a href="https://javiergiangreco.substack.com/" target="_blank" class="blog-btn">✍️ IA: Inteligencia Artesanal</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("📲 **¿Querés usar PAI como App?** Abrí el menú de tu navegador (⋮) y elegí **'Agregar a la pantalla principal'**.")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    destinatario = st.text_input("👤 ¿A quién le escribís?", placeholder="Ej: Mi jefe, un grupo...")
    emocion_usuario = st.text_input("🎭 Tu Emoción", placeholder="Ej: Frustración, enojo...")
with c2:
    contexto = st.text_input("📂 Contexto corto", placeholder="Ej: Mail fuera de hora...")
    modo_conciencia = st.selectbox("🧘 Elije tu Filtro", list(PERSONALIDADES.keys()), index=1)

st.markdown("---")

# LEYENDA DE PRIVACIDAD
st.markdown('<p class="privacy-note">🔒 Garantía de Privacidad: Tu mensaje se autodestruirá al cerrar sesión.</p>', unsafe_allow_html=True)
mensaje_crudo = st.text_area("Escribí acá tu descarga sin filtros:", height=120)

# --- 6. EJECUCIÓN DEL ANÁLISIS ---
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
                            tox = min(int(match.group()), 100)
                    else: 
                        clean_text += l + "\n"
                st.session_state.analisis_actual = {"texto": clean_text.strip(), "tox": tox}
            except Exception:
                st.error("🧘 **PAI está meditando profundamente...** Hubo una saturación. Intentá de nuevo.")

# --- 7. RESULTADOS Y SEGUNDA VUELTA ---
if st.session_state.analisis_actual:
    st.divider()
    tox = st.session_state.analisis_actual["tox"]
    st.subheader(f"🌡️ Nivel de Impulsividad: {tox}%")
    st.progress(tox / 100)
    
    texto_analisis = st.session_state.analisis_actual["texto"]
    
    if tox >= 65: st.error(f"🚨 **¡FRENO DE MANO! (Nivel Crítico)**\n\n{texto_analisis}")
    elif tox >= 30: st.warning(f"⚠️ **Atención (Nivel Medio)**\n\n{texto_analisis}")
    else: st.success(f"✅ **Bajo Control (Nivel Saludable)**\n\n{texto_analisis}")
    
    st.info("💡 **Tip:** Copiá la respuesta abajo, reescribila con tu voz y volvamos a filtrarla.")
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
                            if match_v: tox_v = min(int(match_v.group()), 100)
                        else: clean_v += lv + "\n"
                    st.session_state.validacion_final = {"texto": clean_v.strip(), "tox": tox_v}
                except:
                    st.error("No se pudo completar el chequeo. Intentá de nuevo.")

    if st.session_state.validacion_final:
        tv = st.session_state.validacion_final["tox"]
        texto_final = st.session_state.validacion_final["texto"]
        st.write(f"📊 **Nuevo Nivel de Impulsividad: {tv}%**")
        st.progress(tv / 100)
        
        if tv >= 65: st.error(texto_final)
        elif tv >= 30: st.warning(texto_final)
        else: st.success(texto_final)

    # Botones de cierre y reinicio
    st.markdown("""
    <div class="feedback-box">
        <h4>🔥 ¿PAI te salvó de un incendio emocional hoy?</h4>
        <p style="color: #666; font-size: 0.95rem;">Contanos tu historia anónima para seguir mejorando.</p>
        <a href="mailto:javiergiangreco@gmail.com?subject=PAI%20-%20mensajes" class="mail-btn">✉️ Escribime a javiergiangreco@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Nueva Pausa"):
        st.session_state.analisis_actual = None
        st.session_state.validacion_final = None
        st.rerun()

# --- 8. FOOTER LEGAL Y CORPORATIVO ---
st.markdown("---")
st.caption("""
⚠️ **Aviso de Responsabilidad:** PAI es una herramienta orientativa basada en IA. El accionar final es **exclusiva responsabilidad del usuario**. 
No reemplaza asesoramiento profesional. **Uso sugerido para mayores de 13 años.**
""")

st.markdown("""
<div class="corporate-cta">
    🏢 <b>¿Querés implementar una versión personalizada de PAI para la comunicación interna de tu empresa?</b><br> 
    <a href="https://www.linkedin.com/in/javiergiangreco/" target="_blank">Conversemos en LinkedIn.</a>
</div>
""", unsafe_allow_html=True)