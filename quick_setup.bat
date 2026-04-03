@echo off
echo ========================================
echo Mental Health Monitoring System Setup
echo ========================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate

echo [3/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next step:
echo Run: START.bat (or python manage.py runserver)
echo Visit: http://127.0.0.1:8000/login/
echo.
echo Login with: testuser / test123
echo Or create new account at: /register/
echo.
pause
