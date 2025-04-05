import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Chatbot de Restaurante", page_icon="🍔")

# Título y descripción
st.title("🍽️ Asistente Virtual de Restaurante")
st.subheader("¡Bienvenido! Puedo ayudarte a elegir platillos de nuestro menú")

# Estilo personalizado
st.markdown("""
<style>
    .main {
        background-color: #f9f7f2;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Configuración de la API Key (igual que en MelodyBot)
GEMINI_API_KEY = "AIzaSyB7JY2tkAVEmksw1CEFVMxT-2LBCAcCQco"
genai.configure(api_key=GEMINI_API_KEY)

# Selección del modelo
MODEL = "gemini-1.5-flash"

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Bienvenido a nuestro restaurante. 🍽️ Soy tu asistente virtual para ayudarte con nuestro menú. Puedo recomendarte:\n\n"
                                         "• Entradas deliciosas 🥗\n"
                                         "• Platos principales 🍲\n"
                                         "• Postres tentadores 🧁\n"
                                         "• Bebidas refrescantes 🥤\n\n"
                                         "¿Qué te gustaría ordenar hoy?"}
    ]

# Mostrar mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("¿Qué te gustaría ordenar hoy?"):
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            # Información del menú para la instrucción
            menu_info = """
            MENÚ DEL RESTAURANTE:
            - ENTRADAS:
              * Guacamole con totopos ($120)
              * Queso fundido con chorizo ($150)
              * Sopa de tortilla ($100)
              * Ensalada mixta ($90)
            
            - PLATOS PRINCIPALES:
              * Tacos de carne asada (4 piezas - $180)
              * Enchiladas de pollo ($160)
              * Chiles rellenos ($170)
              * Mole poblano con arroz ($190)
              * Pescado a la veracruzana ($220)
            
            - POSTRES:
              * Flan de caramelo ($80)
              * Churros con chocolate ($70)
              * Pastel de tres leches ($90)
              * Helado de vainilla ($60)
            
            - BEBIDAS:
              * Agua fresca de jamaica/horchata/tamarindo ($40)
              * Refresco ($45)
              * Cerveza nacional ($60)
              * Cerveza importada ($80)
              * Margarita ($110)
            """
            
            # Crear modelo
            model = genai.GenerativeModel(MODEL)
            
            # Historial completo para contexto
            historial_conversacion = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            # Generar respuesta con instrucción
            respuesta = model.generate_content(
                f"Actúa como un asistente virtual de restaurante. Eres amable y servicial. Usa esta información del menú:\n\n{menu_info}\n\n"
                f"Historial de conversación:\n{historial_conversacion}\n\n"
                f"Responde a la última consulta del usuario de manera conversacional y amigable. "
                f"Puedes recomendar platillos, describir ingredientes, sugerir combinaciones, "
                f"informar sobre precios y preguntar sobre preferencias alimenticias.", 
                stream=False
            )
            
            # Extraer el texto de la respuesta
            respuesta_texto = respuesta.text if hasattr(respuesta, 'text') else "Lo siento, no pude procesar tu solicitud."
            
            # Mostrar la respuesta en la interfaz
            st.markdown(respuesta_texto)
            
            # Añadir respuesta al historial
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            st.error(f"¡Vaya! Hubo un error al procesar tu solicitud: {str(e)}")
            st.session_state.messages.append(
                {"role": "assistant", "content": "Disculpa, no pude responder. ¿Podrías intentarlo de nuevo?"}
            )

# Botón para reiniciar conversación
if st.button("Reiniciar conversación"):
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Bienvenido a nuestro restaurante. 🍽️ Soy tu asistente virtual para ayudarte con nuestro menú. Puedo recomendarte:\n\n"
                                         "• Entradas deliciosas 🥗\n"
                                         "• Platos principales 🍲\n"
                                         "• Postres tentadores 🧁\n"
                                         "• Bebidas refrescantes 🥤\n\n"
                                         "¿Qué te gustaría ordenar hoy?"}
    ]
    st.experimental_rerun()
