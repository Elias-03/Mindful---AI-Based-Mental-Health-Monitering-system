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
