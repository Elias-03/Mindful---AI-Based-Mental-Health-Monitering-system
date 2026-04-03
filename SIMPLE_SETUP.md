# 🚀 Simple Setup - For Your Team

Since you're sharing the `.env` file (same Supabase database for everyone), setup is super simple!

## ✅ What You're Sharing

Everything including:
- ✅ All code
- ✅ `.env` file (with Supabase credentials)
- ✅ `venv/` folder (optional - can include or exclude)
- ✅ Migrations (database structure)

## 📦 For Recipients

### Option 1: With venv folder (Easiest)

If you include the `venv/` folder:

**Windows:**
```bash
venv\Scripts\activate
python manage.py runserver
```

**Mac/Linux:**
```bash
source venv/bin/activate
python manage.py runserver
```

That's it! Visit http://127.0.0.1:8000/login/

### Option 2: Without venv folder (Smaller download)

If you DON'T include `venv/`:

**Windows:**
```bash
.\quick_setup.bat
```

**Mac/Linux:**
```bash
chmod +x quick_setup.sh
./quick_setup.sh
```

Then:
```bash
python manage.py runserver
```

## 🎯 Why No Migrations Needed?

Since everyone uses the SAME Supabase database:
- Tables already exist (you created them)
- Users already exist (testuser is there)
- No need to run migrations again
- Just activate venv and run server!

## 👥 User Accounts

Everyone can:
- Login with: `testuser` / `test123`
- Or create new accounts via `/register/`
- All users share the same database
- Everyone sees their own mood logs (filtered by user_id)

## 📤 How to Share

**Easiest way:**
1. Zip the entire folder (including venv if you want)
2. Share via Google Drive, Dropbox, etc.
3. Recipients extract and run

**Smaller package:**
1. Delete `venv/` folder
2. Zip the folder
3. Recipients run `quick_setup.bat` to recreate venv

## ⚡ Super Quick Start

For someone who just received your project:

```bash
# PowerShell requires .\ prefix
.\quick_setup.bat

# Or if venv exists:
venv\Scripts\activate
python manage.py runserver
```

Done! No migrations, no database setup, no Supabase configuration needed!
