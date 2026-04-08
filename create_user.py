#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health.settings')
django.setup()

from django.contrib.auth.models import User

username = 'testuser'
password = 'test123'
email = 'test@example.com'

if User.objects.filter(username=username).exists():
    print(f"✅ User '{username}' already exists")
else:
    User.objects.create_user(username=username, password=password, email=email)
    print(f"✅ Created test user: {username}")
    print(f"   Password: {password}")

print("\nYou can now login at: http://127.0.0.1:8000/login/")
print(f"Username: {username}")
print(f"Password: {password}")
