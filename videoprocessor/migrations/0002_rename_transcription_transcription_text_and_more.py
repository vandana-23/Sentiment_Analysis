# Generated by Django 5.1.5 on 2025-01-27 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoprocessor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transcription',
            old_name='transcription',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='video',
            name='transcription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_transcription', to='videoprocessor.transcription'),
        ),
        migrations.AlterField(
            model_name='transcription',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcriptions', to='videoprocessor.video'),
        ),
        migrations.CreateModel(
            name='SentimentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_sentiment', models.CharField(max_length=10)),
                ('sentiment_score', models.FloatField()),
                ('abusive_words', models.TextField(blank=True)),
                ('bad_words', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transcription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videoprocessor.transcription')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videoprocessor.video')),
            ],
        ),
        migrations.DeleteModel(
            name='Sentiment_analysis',
        ),
    ]
