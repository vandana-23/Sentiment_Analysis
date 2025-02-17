import cv2
import pyaudio
import speech_recognition as sr
import threading
import pyautogui
import requests

# Initialize the recognizer
recognizer = sr.Recognizer()
stop_flag = threading.Event()
transcription_text = ""

# Function to capture and transcribe audio
def capture_audio():
    global transcription_text
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while not stop_flag.is_set():
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                print("You said: " + transcription)
                transcription_text = transcription
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to save the transcription to the database
def save_to_database(transcription_text):
    url = 'http://127.0.0.1:8000/save_transcription/'  # Replace with your actual URL
    data = {'transcription_text': transcription_text}
    response = requests.post(url, data=data)
    print(response.status_code, response.content)

# Function to display video and overlay transcription like YouTube captions
def display_video():
    global transcription_text
    cap = cv2.VideoCapture(0)

    # Get the screen size using pyautogui
    screen_width, screen_height = pyautogui.size()

    # Set the window to full screen
    cv2.namedWindow('Video with Transcription', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Video with Transcription', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while not stop_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to fit the screen
        frame = cv2.resize(frame, (screen_width, screen_height))

        # Create a black bar at the bottom of the frame for captions
        bar_height = 50
        caption_bar = cv2.rectangle(frame, (0, screen_height - bar_height), (screen_width, screen_height), (0, 0, 0), -1)

        # Overlay transcription text centered on the black bar
        text_size = cv2.getTextSize(transcription_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = (screen_width - text_size[0]) // 2
        text_y = screen_height - 20

        cv2.putText(frame, transcription_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Video with Transcription', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_flag.set()
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save the transcription to the database
    save_to_database(transcription_text)

# Start the audio capture in a separate thread
audio_thread = threading.Thread(target=capture_audio)
audio_thread.daemon = True
audio_thread.start()

# Start the video capture in the main thread
display_video()

