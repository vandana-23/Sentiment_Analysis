#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

logger = logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_to_text.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.error("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?")
        raise exc

    if len(sys.argv) > 1 and sys.argv[1] == "run_sentiment_analysis":
        logger.info("Running custom sentiment analysis task...")
        from video_to_text.videoprocessor.sentiment_analysis import run_analysis
        run_analysis()
        sys.exit(0)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
