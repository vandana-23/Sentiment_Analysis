import threading
import uuid
import os
import cv2
import pyautogui
from moviepy.editor import VideoFileClip
from textblob import TextBlob
from nltk.tokenize import word_tokenize
import speech_recognition as sr
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from .models import VideoTranscriptionAnalysis, RealTimeTranscription

# Constants for abusive and bad words detection
ABUSIVE_WORDS = [
    'abuse', 'offensive', 'harass', 'threat', 'violence', 'bully', 
    'insult', 'disrespect', 'demean', 'assault', 'discriminate', 'humiliate',
    'intimidate', 'coerce', 'exploit', 'oppress', 'persecute', 'torment',
    'terrorize', 'abhor', 'degrade', 'dehumanize', 'belittle', 'mock'
]
BAD_WORDS = [
    'bad', 'idiot', 'hate', 'not happy', 'stupid', 'loser', 
    'worthless', 'failure', 'pathetic', 'ugly', 'fool', 'miserable',
    'dumb', 'ignorant', 'nasty', 'horrible', 'terrible', 'awful',
    'disgusting', 'gross', 'repulsive', 'vile', 'detestable', 'loathsome'
]

def home(request):
    """Render the home page."""
    return render(request, 'videoprocessor/home.html')

from django import forms

class VideoUploadForm(forms.Form):
    video = forms.FileField(label='Select a video file')

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(video_file.name, video_file)
        video_url = fs.url(filename)
        video_path = os.path.join(settings.MEDIA_ROOT, filename)

        print(f"Uploaded Video Path: {video_path}")  # Debugging

        try:
            audio_path = extract_audio(video_path)
            if not audio_path:
                raise ValueError("Audio extraction failed")

            transcription_text = transcribe_audio(audio_path)

            # Perform sentiment analysis
            overall_sentiment, sentiment_score, abusive_words, bad_words = analyze_sentiment(transcription_text)

            # Save to database
            obj = VideoTranscriptionAnalysis.objects.create(
                video_name=filename,
                video_file=video_file,
                transcription_text=transcription_text,
                overall_sentiment=overall_sentiment,
                sentiment_score=sentiment_score,
                abusive_words=", ".join(abusive_words),
                bad_words=", ".join(bad_words),
            )
            
            context = {
                'video_name': obj.video_name,
                'transcription': obj.transcription_text,
                'overall_sentiment': obj.overall_sentiment,
                'sentiment_score': obj.sentiment_score,
                'abusive_words': obj.abusive_words.split(", ") if obj.abusive_words else [],
                'bad_words': obj.bad_words.split(", ") if obj.bad_words else [],
                'video_url': video_url,
            }
            return render(request, 'videoprocessor/transcriptions.html', context)

        except Exception as e:
            print(f"Error occurred: {e}")  # Debugging
            return render(request, 'videoprocessor/error.html', {'error': str(e)})

    return render(request, 'videoprocessor/upload.html')

def extract_audio(video_path):
    """Extracts audio from video and saves it as a .wav file."""
    audio_path = video_path.replace(".mp4", ".wav")  

    if os.path.exists(audio_path):
        return audio_path  # If already converted, return the existing audio path
    
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        return audio_path
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
   
def transcribe_audio(audio_path):
    """Converts audio to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)  # Read the entire audio file
        transcription = recognizer.recognize_google(audio)  # Google API for speech recognition
        return transcription
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "API request failed."
    except Exception as e:
        return f"Error: {str(e)}"
    
def analyze_sentiment(transcription_text):
    """Performs sentiment analysis and detects abusive/bad words."""
    if not transcription_text:
        return "Neutral", 0, [], []

    blob = TextBlob(transcription_text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        overall_sentiment = "Positive"
    elif sentiment_score < 0:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    # Check for abusive and bad words
    words = word_tokenize(transcription_text.lower())
    abusive_words_found = [word for word in words if word in ABUSIVE_WORDS]
    bad_words_found = [word for word in words if word in BAD_WORDS]

    return overall_sentiment, sentiment_score, abusive_words_found, bad_words_found

def transcription_detail(request, video_id):
    """Displays details of a transcription."""
    video = get_object_or_404(VideoTranscriptionAnalysis, id=video_id)

    return render(request, 'videoprocessor/transcriptions.html', {
        'video_name': video.video_name,
        'transcription': video.transcription_text,
        'overall_sentiment': video.overall_sentiment,
        'sentiment_score': video.sentiment_score,
        'abusive_words': video.abusive_words.split(', ') if video.abusive_words else [],
        'bad_words': video.bad_words.split(', ') if video.bad_words else [],
    })


def video_list(request):
    """Displays a list of all videos."""
    videos = VideoTranscriptionAnalysis.objects.all()
    return render(request, 'videoprocessor/video_list.html', {'videos': videos})


def success(request):
    """Renders the success page."""
    return render(request, 'videoprocessor/success.html')

def save_transcription(request):
    """Saves transcription text to the database."""
    if request.method == 'POST':
        transcription_text = request.POST.get('transcription_text', '')

        if transcription_text.strip():  # Ensure it's not empty
            transcription = RealTimeTranscription(
                transcription_text=transcription_text,
                created_at=timezone.now()
            )
            transcription.save()
            return redirect('home')

    return render(request, 'videoprocessor/upload.html')

def start_real_time_transcription():
    """Start real-time speech recognition with abusive/bad word detection and display."""
    recognizer = sr.Recognizer()
    stop_flag = threading.Event()
    transcription_text = ""
    detected_abusive_text = ""
    detected_bad_text = ""

    session_id = str(uuid.uuid4())  # Generate a unique session ID

    def capture_audio():
        """Capture and process audio for transcription and abusive word detection."""
        nonlocal transcription_text, detected_abusive_text, detected_bad_text

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            while not stop_flag.is_set():
                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=60, phrase_time_limit=60)
                    transcription = recognizer.recognize_google(audio)
                    print("You said:", transcription)

                    # Tokenize words
                    words = word_tokenize(transcription.lower())

                    # Detect abusive & bad words
                    detected_abusive = [word for word in ABUSIVE_WORDS if word in words]
                    detected_bad = [word for word in BAD_WORDS if word in words]

                    # Store detected words
                    detected_abusive_text = ", ".join(detected_abusive) if detected_abusive else ""
                    detected_bad_text = ", ".join(detected_bad) if detected_bad else ""

                    # Perform sentiment analysis
                    sentiment_blob = TextBlob(transcription)
                    polarity = sentiment_blob.sentiment.polarity
                    overall_sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
                    sentiment_score = polarity

                    # Update displayed transcription
                    transcription_text = transcription  # Always store the full transcription

                    # Save to database
                    save_transcription_to_db(transcription, overall_sentiment, sentiment_score, detected_abusive, detected_bad, session_id)

                except sr.WaitTimeoutError:
                    print("No speech detected. Continuing to listen...")
                    continue
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Speech recognition service error: {e}")

    def save_transcription_to_db(text, sentiment, score, detected_abusive, detected_bad, session_id):
        """Save transcription with detected abusive/bad words to the database."""
        transcription = RealTimeTranscription(
            session_id=session_id,
            transcription_text=text,
            created_at=timezone.now(),
            overall_sentiment=sentiment,
            sentiment_score=score,
            abusive_words=', '.join(detected_abusive),
            bad_words=', '.join(detected_bad)
        )
        transcription.save()

    def display_video():
        """Capture video and overlay transcription text and detected words in real-time."""
        nonlocal transcription_text, detected_abusive_text, detected_bad_text
        cap = cv2.VideoCapture(0)

        screen_width, screen_height = pyautogui.size()
        cv2.namedWindow('Video with Transcription', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Video with Transcription', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while not stop_flag.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (screen_width, screen_height))

            # Draw a black bar at the bottom
            bar_height = 50
            cv2.rectangle(frame, (0, screen_height - bar_height), (screen_width, screen_height), (0, 0, 0), -1)

            # Prepare text to display
            text_to_display = transcription_text if transcription_text else "Listening..."
            abusive_text_to_display = f"Abusive Words: {detected_abusive_text}" if detected_abusive_text else ""
            bad_text_to_display = f"Bad Words: {detected_bad_text}" if detected_bad_text else ""

            # Display transcription
            text_size = cv2.getTextSize(text_to_display, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (screen_width - text_size[0]) // 2
            text_y = screen_height - 35
            cv2.putText(frame, text_to_display, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display abusive/bad words separately
            if detected_abusive_text:
                abusive_text_size = cv2.getTextSize(abusive_text_to_display, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                abusive_text_x = (screen_width - abusive_text_size[0]) // 2
                abusive_text_y = screen_height - 10
                cv2.putText(frame, abusive_text_to_display, (abusive_text_x, abusive_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            if detected_bad_text:
                bad_text_size = cv2.getTextSize(bad_text_to_display, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                bad_text_x = (screen_width - bad_text_size[0]) // 2
                bad_text_y = screen_height - 10
                cv2.putText(frame, bad_text_to_display, (bad_text_x, bad_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow('Video with Transcription', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_flag.set()
                break

        cap.release()
        cv2.destroyAllWindows()

    # Start both threads
    audio_thread = threading.Thread(target=capture_audio, daemon=True)
    video_thread = threading.Thread(target=display_video, daemon=True)

    audio_thread.start()
    video_thread.start()

    # Wait for the video thread to complete
    video_thread.join()

    # Ensure audio thread stops properly
    stop_flag.set()
    audio_thread.join()


def real_time_transcription_view(request):
    """Start the real-time transcription and abusive word detection."""
    if request.method == 'GET':
        try:
            start_real_time_transcription()
            return render(request, 'videoprocessor/real_time_transcription.html')
        except Exception as e:
            return HttpResponse(f"Failed to start real-time transcription: {e}")

    return render(request, 'videoprocessor/upload.html')

def transcription_list(request):
    """Render the list of transcriptions."""
    transcriptions = RealTimeTranscription.objects.all()
    return render(request, 'videoprocessor/transcription_list.html', {'transcriptions': transcriptions})
