@echo off
echo ========================================
echo Add New User
echo ========================================
echo.

call venv\Scripts\activate

set /p username="Enter username: "
set /p password="Enter password: "
set /p email="Enter email (optional): "

python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health.settings'); django.setup(); from django.contrib.auth.models import User; user = User.objects.create_user(username='%username%', password='%password%', email='%email%'); print(f'\n✅ User {user.username} created successfully!')"

echo.
echo User can now login at: http://127.0.0.1:8000/login/
echo Username: %username%
echo.
pause
