from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_avatar_url(self):
        if self.profile_picture_url:
            return self.profile_picture_url
        return f"https://ui-avatars.com/api/?name={self.user.username}&background=667eea&color=fff&size=200"

class MoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    entry_summary = models.TextField(blank=True)
    emotions_json = models.JSONField(default=dict)
    dominant_emotion = models.CharField(max_length=50)
    sentiment_score = models.FloatField()
    alert_level = models.CharField(max_length=20, default='none')
    alert_text = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def sentiment_percentage(self):
        # Maps -1 to 1 to 0% to 100%
        return int((self.sentiment_score + 1) * 50)

class NotificationManager(models.Manager):
    def unread(self):
        return self.filter(is_read=False)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('mood_alert', 'Mood Alert'),
        ('mood_positive', 'Positive Mood'),
        ('mood_neutral', 'Neutral Mood'),
        ('system', 'System Notification'),
        ('milestone', 'Milestone Reached'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    objects = NotificationManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"
