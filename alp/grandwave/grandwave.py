import streamlit as st
import cv2
import numpy as np
import pyttsx3
import json
import speech_recognition as sr
from PIL import Image
from streamlit_lottie import st_lottie
import requests

# Set up the page
st.set_page_config(page_title="Grand Wave App", page_icon="🌍", layout="wide")

# Function to load the local Lottie animation file
def load_local_lottie(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading animation: {e}")
        return None

# Load Lottie animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Load animations
# Load the local animation
animation_path = r"C:\Users\MULAMBA JORAM\Desktop\grandwave\animation1.json"
theme_animation = load_local_lottie(animation_path)


voice_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_iw1v2vqi.json")
video_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_kxsd2ytq.json")

# Header Section
st.markdown("""
    <style>
        .header-title {
            font-size: 36px;
            color: #d88c3c;
            text-align: center;
            font-weight: bold;
        }
        .sub-header {
            font-size: 18px;
            color: #4b3832;
            margin-top: -10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Add main animation banner
if theme_animation:
    st_lottie(theme_animation, height=200, key="theme")
else:
    st.warning("⚠️ Unable to load theme animation.")

st.markdown('<div class="header-title">Grand Wave App</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">"Beyond Boundaries: Bridging Communication Gaps in East Africa"</div>', unsafe_allow_html=True)



# Introduction Section
with st.container():
    st.markdown("""
        <style>
            .info-box {
                padding: 10px;
                background-color: #fff7e6;
                border-radius: 10px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                font-size: 18px;
                line-height: 1.6;
            }
        </style>
        <div class="info-box">
            Welcome to Grand Wave App, an innovative platform designed to:
            - Translate sign language into clear and audible speech.
            - Convert spoken local East African languages into English and vice versa.
        </div>
    """, unsafe_allow_html=True)

# Language Selection
with st.container():
    st.subheader("🌐 Select Your Preferred Language")
    local_languages = ["Luganda", "Acholi", "Rutooro", "English"]
    selected_language = st.selectbox("Choose your language:", local_languages)

# Feature Selection
st.markdown("---")
st.subheader("🎙️ Select a Recording Mode")

record_option = st.radio(
    "How would you like to record?",
    options=["Sign Language (Video)", "Voice Recording (Audio)"],
    index=0
)

# Voice Recording Section
if record_option == "Voice Recording (Audio)":
    st.markdown("---")
    st.subheader("🎤 Voice Recording")
    if voice_animation:
        st_lottie(voice_animation, height=150, key="voice")
    st.write("Use your microphone to capture and translate speech into a local language.")

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

# Sign Language Recording Section
if record_option == "Sign Language (Video)":
    st.markdown("---")
    st.subheader("📹 Sign Language Detection")
    if video_animation:
        st_lottie(video_animation, height=150, key="video")
    st.write("Turn on your camera to detect and translate sign language into speech.")
    
    run_video = st.checkbox("📸 Enable Camera")

    if run_video:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Camera not accessible.")
                break

            # Simulate detection and translation
            detected_translation = "Hello"
            st.success(f"🖐️ Detected Sign: {detected_translation}")

            # Display live video feed
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            st.image(img, caption="Live Camera Feed", use_column_width=True)

            if not st.checkbox("📸 Enable Camera", value=True):
                cap.release()
                break

        cap.release()

# Footer Section
st.markdown("---")
st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #4b3832;">
        Designed with ❤️ for the African Community. Powered by AI.
    </div>
""", unsafe_allow_html=True)
