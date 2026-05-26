import streamlit as st
from groq import Groq
import speech_recognition as sr
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: white;
}

/* Main Header */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 700;
    color: #00FFD1;
    margin-top: 10px;
}

.sub-title {
    text-align: center;
    color: #CBD5E1;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Chat Cards */
.user-message {
    background: #1E293B;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    border-left: 5px solid #00FFD1;
}

.bot-message {
    background: #111827;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
    border-left: 5px solid #38BDF8;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, #00FFD1, #00C9FF);
    color: black;
    font-size: 18px;
    font-weight: 600;
}

.stButton > button:hover {
    color: white;
    transform: scale(1.01);
    transition: 0.3s;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* Input Box */
.stTextInput input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# API CONFIG
# ---------------------------------------------------
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.title("⚙️ Assistant Settings")

    model = st.selectbox(
        "Choose Model",
        [
            "llama-3.3-70b-versatile",
            "llama3-8b-8192",
            "mixtral-8x7b-32768"
        ]
    )

    temperature = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.7
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown(
    '<div class="main-title">🎤 AI Voice Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Groq Powered Smart Assistant</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SPEECH RECOGNITION
# ---------------------------------------------------
recognizer = sr.Recognizer()

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2 = st.tabs(["💬 Chat", "🎙️ Voice"])

# ---------------------------------------------------
# CHAT TAB
# ---------------------------------------------------
with tab1:

    user_input = st.chat_input("Type your message here...")

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # Display User Message
        st.markdown(
            f"""
            <div class="user-message">
            <b>🧑 You:</b><br>{user_input}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Generate AI Response
        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature
            )

            answer = response.choices[0].message.content

        # Store Assistant Message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Streaming Effect
        placeholder = st.empty()

        streamed_text = ""

        for char in answer:
            streamed_text += char
            placeholder.markdown(
                f"""
                <div class="bot-message">
                <b>🤖 AI:</b><br>{streamed_text}
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.005)

# ---------------------------------------------------
# VOICE TAB
# ---------------------------------------------------
with tab2:

    st.info("Use voice input below")

    if st.button("🎙️ Start Listening"):

        try:

            with sr.Microphone() as source:

                with st.spinner("Listening..."):

                    recognizer.adjust_for_ambient_noise(source)

                    audio = recognizer.listen(source)

                    voice_text = recognizer.recognize_google(audio)

                st.success(f"You said: {voice_text}")

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": voice_text
                    }
                )

                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature
                )

                answer = response.choices[0].message.content

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                st.markdown(
                    f"""
                    <div class="bot-message">
                    <b>🤖 AI:</b><br>{answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except sr.UnknownValueError:
            st.error("Could not understand audio")

        except sr.RequestError as e:
            st.error(f"Speech Recognition Error: {e}")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------
st.divider()

st.subheader("📜 Conversation History")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
            <b>🧑 You:</b><br>{msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-message">
            <b>🤖 AI:</b><br>{msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )
