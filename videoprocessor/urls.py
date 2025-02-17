from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('success/', views.success, name='success'),
    path('transcription_list/', views.transcription_list, name='transcription_list'),
    path('real_time_transcription/', views.real_time_transcription_view, name='real_time_transcription'),
    path('save_transcription/', views.save_transcription, name='save_transcription'),
    path('start_real_time_transcription/', views.start_real_time_transcription, name='start_real_time_transcription'),
]
