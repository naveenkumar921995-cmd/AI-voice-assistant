import streamlit as st
from groq import Groq
import speech_recognition as sr
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎤",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #00FFD1;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #D3D3D3;
    margin-bottom: 30px;
}

.user-box {
    background-color: #1F2937;
    padding: 15px;
    border-radius: 15px;
    margin-top: 20px;
    color: white;
}

.ai-box {
    background-color: #111827;
    padding: 15px;
    border-radius: 15px;
    margin-top: 20px;
    border: 1px solid #00FFD1;
    color: white;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #00FFD1, #00C9FF);
    color: black;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #00C9FF, #00FFD1);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="title">🎤 AI Voice Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by Groq + Speech Recognition</div>',
    unsafe_allow_html=True
)

# -----------------------------
# API KEY
# -----------------------------
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# SPEECH RECOGNITION
# -----------------------------
recognizer = sr.Recognizer()

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🎙️ Start Listening"):

    with st.spinner("Listening... Speak Now"):

        try:

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(source)

                audio = recognizer.listen(source)

                text = recognizer.recognize_google(audio)

                st.markdown(
                    f"""
                    <div class="user-box">
                    <h4>🧑 You Said:</h4>
                    <p>{text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # -----------------------------
                # GROQ RESPONSE
                # -----------------------------
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a smart AI assistant"
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.markdown(
                    f"""
                    <div class="ai-box">
                    <h4>🤖 AI Response:</h4>
                    <p>{answer}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except sr.UnknownValueError:
            st.error("Could not understand audio")

        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")

        except Exception as e:
            st.error(f"Error: {e}")
