from django.contrib import admin
from .models import VideoTranscriptionAnalysis, RealTimeTranscription  

@admin.register(VideoTranscriptionAnalysis)
class VideoTranscriptionAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'video_name', 
        'transcription_text', 
        'overall_sentiment', 
        'sentiment_score', 
        'abusive_words', 
        'bad_words', 
        'created_at'
    )
    search_fields = ('video_name', 'transcription_text', 'overall_sentiment', 'sentiment_score', 'abusive_words', 'bad_words')
    list_filter = ('overall_sentiment', 'created_at')

@admin.register(RealTimeTranscription)
class RealTimeTranscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'transcription_text', 
        'created_at',
        'overall_sentiment', 
        'sentiment_score', 
        'abusive_words', 
        'bad_words',
    )
    search_fields = ('transcription_text', 'overall_sentiment', 'sentiment_score', 'abusive_words', 'bad_words')
    list_filter = ('created_at', 'overall_sentiment')

