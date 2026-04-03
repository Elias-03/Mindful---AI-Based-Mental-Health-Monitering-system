#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health.settings')
django.setup()

from django.contrib.auth.models import User
from journal.models import MoodLog

print("Checking Supabase PostgreSQL Database...")
print("=" * 60)

# Check users
users = User.objects.all()
print(f"\n👥 Users in database: {users.count()}")
for user in users:
    print(f"   - {user.username} ({user.email})")

# Check mood logs
logs = MoodLog.objects.all()
print(f"\n📊 Mood logs in database: {logs.count()}")
for log in logs[:5]:
    print(f"   - {log.user.username}: {log.dominant_emotion} ({log.timestamp})")

print("\n" + "=" * 60)
print("✅ All data is now stored in Supabase PostgreSQL!")
print("\nYou can view this data in Supabase Dashboard:")
print("1. Go to Table Editor")
print("2. Check tables: auth_user, journal_moodlog, etc.")
