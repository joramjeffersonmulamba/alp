import os
import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import time
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

# Streamlit page setup
st.set_page_config(page_title="Sign Language Detection", page_icon="🤟")

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
    # Draw landmarks (face, pose, hands)
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
st.title("Sign Language Detection")
st.write("This application uses MediaPipe to detect sign language gestures in real-time.")

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

                # Wait for 1 ms to check for the next frame or user interruption
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

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
        st.markdown(
            """
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
