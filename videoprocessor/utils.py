
import speech_recognition as sr
from pydub import AudioSegment

def extract_audio(video_path):
    """Extracts audio from video and saves it as a WAV file."""
    audio_path = video_path.replace(".mp4", ".wav")  
    audio = AudioSegment.from_file(video_path)
    audio.export(audio_path, format="wav")
    return audio_path

def transcribe_audio(audio_path):
    """Converts speech to text from an audio file."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)  
    return text


