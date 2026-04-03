@echo off
echo Starting Mental Health Monitoring System...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Start Django server
python manage.py runserver

pause
