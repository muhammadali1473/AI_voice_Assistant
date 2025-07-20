import streamlit as st
import os
from groq import Groq
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import time


load_dotenv()


def inject_css():
    st.markdown("""
    <style>
    /* Black background with dark theme */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Dark chat bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,255,255,0.3);
        padding: 12px;
        margin: 8px 0;
        border: 1px solid rgba(0,255,255,0.2);
    }
    
    /* User message style */
    [data-testid="stChatMessage"].user {
        background: rgba(30,30,30,0.8);
        border-left: 5px solid #00ffff;
        color: white;
    }
    
    /* Assistant message style */
    [data-testid="stChatMessage"].assistant {
        background: rgba(45,45,45,0.8);
        border-left: 5px solid #00ffaa;
        color: white;
    }
    
    /* Dark buttons with neon effect */
    .stButton>button {
        border-radius: 25px;
        box-shadow: 0 0 10px rgba(0,255,255,0.5);
        transition: all 0.3s;
        background: rgba(0,0,0,0.7);
        color: white;
        border: 1px solid #00ffff;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(0,255,255,0.8);
        background: rgba(0,100,100,0.5);
    }
    
    /* Text input with neon effect */
    .stTextInput>div>div>input {
        background: rgba(30,30,30,0.8);
        color: white;
        border: 1px solid #00ffff;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,255,255,0.3);
    }
    
    /* Checkbox style */
    .stCheckbox>label {
        color: white !important;
    }
    
    /* Siri-like pulse animation */
    @keyframes pulse {
        0% { 
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.7);
        }
        70% {
            transform: scale(1.05);
            box-shadow: 0 0 0 15px rgba(0, 255, 255, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(0, 255, 255, 0);
        }
    }
    .siri-pulse {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: radial-gradient(circle, #00ffff, #0077ff);
        display: flex;
        justify-content: center;
        align-items: center;
        animation: pulse 2s infinite;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(0,255,255,0.5);
    }
    .siri-icon {
        font-size: 40px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize components
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
recognizer = sr.Recognizer()

# Streamlit UI setup with futuristic theme
inject_css()
st.title("🌀 Muhammad Ali's AI Assistant")
st.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
    <span style="font-size: 24px; color: #00ffff;">✨</span>
    <span style="color: #00ffff;">Ready to assist you</span>
</div>
""", unsafe_allow_html=True)

# Initialize text-to-speech engine
def init_tts():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('voice', 'english')  # More natural voice
        return engine
    except:
        return None

# Session state for conversation and auto-mode
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'auto_mode' not in st.session_state:
    st.session_state.auto_mode = True
if 'listening' not in st.session_state:
    st.session_state.listening = False
if 'running' not in st.session_state:
    st.session_state.running = True

# Voice input function with auto-detection
def get_voice_input():
    st.session_state.listening = True
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            st.session_state.listening = False
            return query
        except Exception as e:
            st.session_state.listening = False
            return None

# Get Groq response with natural name integration
def get_groq_response(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Text-to-speech function
def speak(text):
    engine = init_tts()
    if engine:
        engine.say(text)
        engine.runAndWait()

# Main chat interface
chat_container = st.container()

# Auto-listening logic
if st.session_state.auto_mode and st.session_state.running:
    # Show Siri-like animation when listening
    if st.session_state.listening:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div class="siri-pulse">
                <span class="siri-icon">🌀</span>
            </div>
            <p style="color: #00ffff; margin-top: 10px;">Listening...</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Auto-detect voice input
    query = get_voice_input()
    if query:
        st.session_state.user_input = query
        if st.session_state.user_input:
            with st.spinner("🌀 Processing..."):
                response = get_groq_response(st.session_state.user_input)
                st.session_state.conversation.append(("You", st.session_state.user_input))
                st.session_state.conversation.append(("Assistant", response))
                speak(response)  # Auto-speak response
                time.sleep(0.5)
                st.rerun()

# Display conversation history with 3D effect
with chat_container:
    for speaker, text in st.session_state.conversation:
        if speaker == "You":
            st.chat_message("user").markdown(f"""
            <div style="
                padding: 12px;
                border-radius: 15px;
                background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
                box-shadow: 5px 5px 10px rgba(0,0,0,0.3),
                            -5px -5px 10px rgba(255,255,255,0.05);
                border-left: 4px solid #00ffff;
            ">
                <strong>You:</strong> {text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.chat_message("assistant").markdown(f"""
            <div style="
                padding: 12px;
                border-radius: 15px;
                background: linear-gradient(145deg, #2d2d2d, #383838);
                box-shadow: 5px 5px 10px rgba(0,0,0,0.3),
                            -5px -5px 10px rgba(255,255,255,0.05);
                border-left: 4px solid #00ffaa;
            ">
                <strong>Assistant:</strong> {text}
            </div>
            """, unsafe_allow_html=True)

# Settings sidebar with futuristic design
with st.sidebar:
    st.markdown("""
    <div style="
        padding: 15px;
        border-radius: 15px;
        background: linear-gradient(145deg, #1a1a1a, #252525);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5),
                   -5px -5px 15px rgba(255,255,255,0.05);
        margin-bottom: 20px;
        border: 1px solid rgba(0,255,255,0.2);
    ">
        <h2 style="color: #00ffff; text-align: center;">⚙️ Settings</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.auto_mode = st.checkbox("Auto Voice Mode", value=True)
    voice_enabled = st.checkbox("Enable Voice Responses", value=True)
    
    if st.button("Clear History", key="clear_btn"):
        st.session_state.conversation = []
        st.rerun()
    
    if st.button("Restart Session", key="restart_btn"):
        st.session_state.running = True
        st.rerun()
    
    st.markdown("""
    <div style="
        padding: 15px;
        border-radius: 15px;
        background: linear-gradient(145deg, #1a1a1a, #252525);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5),
                   -5px -5px 15px rgba(255,255,255,0.05);
        margin-top: 20px;
        border: 1px solid rgba(0,255,255,0.2);
    ">
        <h3 style="color: #00ffff;">💾 Conversation History</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for i, (speaker, text) in enumerate(st.session_state.conversation[-5:]):  # Show last 5 messages
        if speaker == "You":
            st.markdown(f"""
            <div style="
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                background: rgba(30,30,30,0.7);
                border-left: 3px solid #00ffff;
            ">
                🎤 <strong>You:</strong> {text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                background: rgba(45,45,45,0.7);
                border-left: 3px solid #00ffaa;
            ">
                🔊 <strong>Assistant:</strong> {text}
            </div>
            """, unsafe_allow_html=True)

# Manual input fallback
if not st.session_state.auto_mode or not st.session_state.running:
    user_input = st.text_input("Type your message:", key="manual_input")
    if st.button("Send", key="send_btn") and user_input:
        with st.spinner("🌀 Processing..."):
            response = get_groq_response(user_input)
            st.session_state.conversation.append(("You", user_input))
            st.session_state.conversation.append(("Assistant", response))
            if voice_enabled:
                speak(response)
            st.rerun()