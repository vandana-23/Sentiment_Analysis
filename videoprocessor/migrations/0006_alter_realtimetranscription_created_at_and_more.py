# Generated by Django 5.1.5 on 2025-02-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoprocessor', '0005_realtimetranscription_abusive_words_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtimetranscription',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='realtimetranscription',
            name='overall_sentiment',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
