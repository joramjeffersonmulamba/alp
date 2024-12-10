import streamlit as st
import speech_recognition as sr
from streamlit_lottie import st_lottie
import requests
import pyttsx3

# Page Config
st.set_page_config(page_title="Voice Recording", page_icon="🎙️", layout="wide")

# Load animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

voice_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_iw1v2vqi.json")

# Page Content
st.title("🎤 Voice Recording")
if voice_animation:
    st_lottie(voice_animation, height=150, key="voice")

st.markdown("""
    Use your microphone to capture and translate speech into a local language or English.
""")

recognizer = sr.Recognizer()
mic = sr.Microphone()

if st.button("🎙️ Start Recording"):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ Recognized Text: {text}")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        st.success("🔊 Translation played successfully!")
    except sr.UnknownValueError:
        st.error("❌ Unable to recognize speech. Please try again.")
    except sr.RequestError:
        st.error("❌ Connection error with the recognition service.")
