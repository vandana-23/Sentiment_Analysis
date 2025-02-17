from django.db import models
from django.utils import timezone

class RealTimeTranscription(models.Model):
    """Stores real-time transcriptions."""
    session_id = models.CharField(max_length=255, null=True,blank=True)  
    transcription_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    overall_sentiment = models.CharField(max_length=50)
    sentiment_score = models.FloatField()
    abusive_words = models.TextField(blank=True, null=True)
    bad_words = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session {self.session_id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
class VideoTranscriptionAnalysis(models.Model):
    video_name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    transcription_text = models.TextField()
    overall_sentiment = models.CharField(max_length=50,default="Neutral")
    sentiment_score = models.FloatField(null=True, blank=True)
    abusive_words = models.TextField(blank=True, null=True)
    bad_words = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"{self.video_name} - {self.overall_sentiment}"
    