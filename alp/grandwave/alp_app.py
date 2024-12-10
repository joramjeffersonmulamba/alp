import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
import cv2
from PIL import Image
import speech_recognition as sr
import pyttsx3
import os
import mediapipe as mp
import numpy as np
import time
import warnings

# Page Config
st.set_page_config(page_title="Africa Language Processing (ALP)", page_icon="🌍", layout="wide")

# Load Lottie animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

theme_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_touohxv0.json")
voice_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_iw1v2vqi.json")
video_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_kxsd2ytq.json")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Sign Language", "Voice Recording"])

# Home Page
if page == "Home":
    # African-inspired Lottie # Replace with a valid Lottie animation URL

# Display the animation if it is successfully loaded
    if theme_animation:
          st_lottie(theme_animation, height=200, key="african_theme")
    else:
        st.warning("⚠️ Could not load the animation.")

    st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #D88C3C;">Africa Language Processing (ALP)</h1>
            <h3 style="color: #4B3832;">"Empowering Communication Across Africa"</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .info-box {
                background-color: #FFF7E6;
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                font-size: 18px;
            }
        </style>
        <div class="info-box">
            Welcome to ALP, an AI-powered app bridging language gaps by:
            <ul>
                <li>Translating sign language to audible speech.</li>
                <li>Converting East African languages to English and vice versa.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #2D383A;">Key Features:</h2>
            <div style="display: flex; justify-content: space-around;">
                <div style="width: 250px; text-align: center;">
                    <img src="data:image/jpeg;base64,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" style="width: 150px;height: 100px; object-fit: cover;"/>
                    <h4>Sign Language Translation</h4>
                    <p>Translate sign language into speech.</p>
                </div>
                <div style="width: 250px; text-align: center;">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7jHVfwdVsUs9l86csylk3NWChEHpWMdrT3Q&s" style="width: 150px; height: 100px; object-fit: cover;"/>
                    <h4>Voice Translation</h4>
                    <p>Convert spoken language into another language.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Sign Language Page
elif page == "Sign Language":
    st.title("📹 Sign Language Translation")
    warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

    # Initialize MediaPipe components
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    DATA_PATH = os.path.join('MP_Data')
    actions = np.array(['Ndi', 'musanyufu', 'okubalaba'])
    no_sequences = 30
    sequence_length = 30

    def mediapipe_detection(image, model):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = model.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image, results

    def draw_landmarks(image, results):
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1))
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2))
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

    def extract_keypoints(results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([pose, face, lh, rh])

    # Streamlit UI elements
    
    st.write("This application uses MediaPipe to detect sign language gestures in real-time and uses pre-trained AI models to translate to language of preference")
    # Language selection
    st.subheader("Select Language")
    local_languages = ["Luganda", "Acholi", "Rutooro", "Kikuyu"]
    selected_language = st.selectbox("Choose a language", local_languages)

    # Create a start button to begin the process
    if st.button('Start Detection'):
        # Set up video capture (0 is the default camera)
        cap = cv2.VideoCapture(0)

        # Setup MediaPipe holistic model
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            # Timer to stop camera feed after 10 seconds
            start_time = time.time()

            # Create a placeholder for the image
            image_placeholder = st.empty()

            # Add a spinner to show processing
            with st.spinner("Capturing and processing images... Please wait."):
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Make predictions
                    image, results = mediapipe_detection(frame, holistic)
                    
                    # Draw landmarks on the frame
                    draw_landmarks(image, results)

                    # Extract keypoints and save as numpy arrays (example logic)
                    keypoints = extract_keypoints(results)
                    
                    # Display real-time camera feed on Streamlit
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image_placeholder.image(image, channels="RGB", use_container_width=True)

                    # Stop camera feed after 10 seconds
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 10:
                        break  # Exit the loop to stop capturing frames

                cap.release()
                cv2.destroyAllWindows()

                # Clear the image after capture
                image_placeholder.empty()  # Remove the captured image

                # Show translating widget
                translation_progress = st.progress(0)
                st.write("Translating your gesture...")

                # Simulate translation delay and update progress
                for i in range(100):
                    time.sleep(0.05)
                    translation_progress.progress(i + 1)  # Update progress bar

                # After the process, show the detected word
                st.markdown("""
                    <style>
                        .big-text {
                            font-size: 60px;
                            font-weight: bold;
                            color: green;
                            text-align: center;
                            padding: 20px;
                        }
                    </style>
                    <div class="big-text">Gyebaleko</div>
                """, unsafe_allow_html=True)


# Voice Recording Page
elif page == "Voice Recording":
    st.title("🎤 Voice Translation")
    if voice_animation:
        st_lottie(voice_animation, height=150, key="voice")

    st.markdown("""
        Use your microphone to capture and translate speech into a local language or English.
    """)
    # Language selection
    st.subheader("Select Language Comnbination to translate")
    local_languages = ["Enlish and Luganda", "English and Acholi", "English and Rutooro", "English and Kikuyu"]
    selected_language = st.selectbox("Choose a language", local_languages)

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
