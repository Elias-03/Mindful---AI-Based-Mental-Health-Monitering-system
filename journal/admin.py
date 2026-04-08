from django.contrib import admin
from .models import MoodLog

@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'dominant_emotion', 'sentiment_score', 'alert_level']
    list_filter = ['dominant_emotion', 'alert_level', 'timestamp']
    search_fields = ['user__username', 'entry_summary']
