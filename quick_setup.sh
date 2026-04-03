#!/bin/bash

echo "========================================"
echo "Mental Health Monitoring System Setup"
echo "========================================"
echo ""

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Checking environment file..."
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please edit .env with your Supabase credentials"
fi

echo "[5/5] Running migrations..."
python manage.py migrate

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Supabase credentials"
echo "2. Run: python create_user.py (to create test user)"
echo "3. Run: python manage.py runserver"
echo "4. Visit: http://127.0.0.1:8000/login/"
echo ""
