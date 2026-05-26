import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import whisper
import tempfile
import os

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎤"
)

st.title("🎤 AI Voice Assistant")

# ---------------------------------
# GROQ API
# ---------------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ---------------------------------
# LOAD WHISPER MODEL
# ---------------------------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

model = load_whisper()

# ---------------------------------
# RECORD AUDIO
# ---------------------------------
audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True
)

# ---------------------------------
# PROCESS AUDIO
# ---------------------------------
if audio:

    st.audio(audio["bytes"])

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as tmp_file:

        tmp_file.write(audio["bytes"])

        temp_audio_path = tmp_file.name

    # -----------------------------
    # SPEECH TO TEXT
    # -----------------------------
    with st.spinner("Transcribing audio..."):

        result = model.transcribe(temp_audio_path)

        user_text = result["text"]

    st.success(f"🧑 You said: {user_text}")

    # -----------------------------
    # AI RESPONSE
    # -----------------------------
    with st.spinner("Generating AI response..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart AI voice assistant"
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        answer = response.choices[0].message.content

    st.markdown("## 🤖 AI Response")

    st.write(answer)

    # -----------------------------
    # CLEANUP
    # -----------------------------
    os.remove(temp_audio_path)
