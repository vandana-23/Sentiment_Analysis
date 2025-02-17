# Generated by Django 5.1.5 on 2025-01-25 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcription', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='videos/')),
                ('title', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sentiment_analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_sentiment', models.CharField(max_length=10)),
                ('sentiment_score', models.FloatField()),
                ('abusive_words', models.TextField(blank=True)),
                ('bad_words', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transcription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videoprocessor.transcription')),
            ],
        ),
        migrations.AddField(
            model_name='transcription',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videoprocessor.video'),
        ),
    ]
