# Generated by Django 5.1.5 on 2025-01-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoprocessor', '0002_rename_transcription_transcription_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTranscriptionAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=255)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('transcription_text', models.TextField()),
                ('overall_sentiment', models.CharField(max_length=10)),
                ('sentiment_score', models.FloatField()),
                ('abusive_words', models.TextField(blank=True)),
                ('bad_words', models.TextField(blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='transcription',
            name='video',
        ),
        migrations.RemoveField(
            model_name='video',
            name='transcription',
        ),
        migrations.DeleteModel(
            name='SentimentAnalysis',
        ),
        migrations.DeleteModel(
            name='Transcription',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
