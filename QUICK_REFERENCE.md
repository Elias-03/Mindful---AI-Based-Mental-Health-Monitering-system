# ⚡ Quick Reference Guide

## 🎯 For You (Project Owner)

### To Share the Project:
1. Zip the entire folder (including `.env` and optionally `venv/`)
2. Share via Google Drive, email, etc.
3. Done!

### To Add New Users:
```bash
.\ADD_USER.bat
```
Or use the register page: http://127.0.0.1:8000/register/

---

## 👥 For Recipients (Your Team)

### First Time Setup:

**If venv folder is included:**
```bash
.\START.bat
```

**If venv folder is NOT included:**
```bash
.\quick_setup.bat
```
Then:
```bash
.\START.bat
```

### Every Time After:
```bash
.\START.bat
```

### Login:
- URL: http://127.0.0.1:8000/login/
- Username: `testuser`
- Password: `test123`
- Or create your own account at `/register/`

---

## 🛠️ Useful Commands

### Start Server:
```bash
.\START.bat
```

### Add New User:
```bash
.\ADD_USER.bat
```

### Stop Server:
Press `CTRL+C` in the terminal

### Check Database:
```bash
python check_supabase_tables.py
```

---

## 📁 What's Included

- ✅ All source code
- ✅ Apple-inspired UI templates
- ✅ `.env` file (Supabase credentials)
- ✅ Database already configured
- ✅ User accounts ready to use
- ✅ AI model (downloads on first use)

---

## 🎨 Features

- Dashboard with mood charts
- Journal entries with AI analysis
- Profile management with photo upload
- Password change
- History timeline
- Alert system

---

## ⚠️ Notes

- Everyone shares the same Supabase database
- Each user sees only their own mood logs
- AI model downloads ~500MB on first journal entry
- Profile pictures stored in Supabase Storage
- No configuration needed - just run!

---

## 🆘 Troubleshooting

**"quick_setup.bat not recognized"**
→ Use: `.\quick_setup.bat`

**"START.bat not recognized"**
→ Use: `.\START.bat`

**"Python not found"**
→ Install Python 3.8+ from python.org

**"venv\Scripts\activate not found"**
→ Run `.\quick_setup.bat` first
