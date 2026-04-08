# 🚀 Deployment Guide - Share Your Project

## 📦 What to Share

Share everything EXCEPT:
- ❌ `venv/` folder (virtual environment)
- ❌ `.env` file (contains your passwords!)
- ❌ `db.sqlite3` (local database)
- ❌ `__pycache__/` folders
- ❌ Test files (`test_*.py`, `check_*.py`)

The `.gitignore` file is already configured to exclude these.

## 📋 Files to Include

✅ All Python code (`*.py`)
✅ Templates (`templates/`)
✅ Static files (`static/`)
✅ Requirements (`requirements.txt`)
✅ Config files (`.env.example`, `.gitignore`)
✅ Documentation (`README.md`, `*.md`)
✅ Django migrations (`*/migrations/`)

## 🎯 Setup Instructions for Others

Create a `SETUP_INSTRUCTIONS.md` file with these steps:

### 1. Clone/Download the Project
```bash
# Extract the project folder
cd mental-health-app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Supabase credentials:
# - SUPABASE_URL
# - SUPABASE_KEY  
# - SUPABASE_DB_URL
# - SECRET_KEY (generate new one)
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Admin User
```bash
python manage.py createsuperuser
```

### 8. Start Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/login/

## 🔐 Security Notes for Sharing

### If Sharing Publicly (GitHub, etc.):
1. **Never commit `.env`** - It's in .gitignore
2. **Generate new SECRET_KEY** for each deployment
3. **Each person needs their own Supabase project**
4. **Include `.env.example`** with placeholder values

### If Sharing Privately (Team):
1. **Option A**: Share the same Supabase credentials (everyone uses same database)
2. **Option B**: Each person creates their own Supabase project

## 📤 How to Package for Sharing

### Method 1: Git Repository (Recommended)
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### Method 2: ZIP File
1. Delete `venv/` folder
2. Delete `.env` file
3. Delete `db.sqlite3` if it exists
4. Zip the entire project folder
5. Share the ZIP file

## 🔄 Quick Setup Script

Create `quick_setup.sh` (Mac/Linux) or `quick_setup.bat` (Windows):

**Windows (quick_setup.bat):**
```batch
@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Setup complete! Edit .env file and run: python manage.py migrate
```

**Mac/Linux (quick_setup.sh):**
```bash
#!/bin/bash
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Setup complete! Edit .env file and run: python manage.py migrate"
```

## ⚠️ Important Reminders

1. **Each deployment needs its own SECRET_KEY**
2. **Never share your .env file**
3. **Supabase free tier limits**: 500MB database, 1GB storage
4. **AI model downloads ~500MB on first use**
5. **Include clear setup instructions**

## 📝 Checklist Before Sharing

- [ ] Remove `venv/` folder
- [ ] Remove `.env` file
- [ ] Check `.gitignore` is present
- [ ] Include `.env.example` with placeholders
- [ ] Update README.md with setup steps
- [ ] Test setup on a fresh machine
- [ ] Document Supabase setup requirements
- [ ] Include requirements.txt
- [ ] Add license file if needed
