from django.test import TestCase
from django.contrib.auth.models import User
from .models import MoodLog
from .emotion_analyzer import EmotionAnalyzer

class MoodLogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
    def test_mood_log_creation(self):
        log = MoodLog.objects.create(
            user=self.user,
            entry_summary="Feeling good today",
            emotions_json={'joy': 0.8, 'sadness': 0.1},
            dominant_emotion='joy',
            sentiment_score=0.7
        )
        self.assertEqual(log.dominant_emotion, 'joy')
        self.assertEqual(log.user.username, 'testuser')

class EmotionAnalyzerTestCase(TestCase):
    def test_analyzer_basic(self):
        analyzer = EmotionAnalyzer()
        result = analyzer.analyze("I am feeling happy today")
        self.assertIn('emotions', result)
        self.assertIn('dominant_emotion', result)
        self.assertIn('sentiment_score', result)
