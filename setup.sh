#!/bin/bash

echo "Setting up Mental Health Monitoring System..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

echo "Please edit .env with your Supabase credentials"
echo ""

# Run migrations
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Setup complete! Next steps:"
echo "1. Edit .env with your Supabase credentials"
echo "2. Run: python manage.py createsuperuser"
echo "3. Run: python manage.py runserver"
