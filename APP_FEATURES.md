# 🧠 Mindful - Mental Health Monitoring System

## 🎨 Apple-Inspired Design
- Clean, minimal interface with Inter font
- Glassmorphism effects on auth pages
- Smooth animations and transitions
- Gradient accents (purple to blue)
- Responsive layout for all devices

## 🔐 Authentication System
- **Login** (`/login/`) - Beautiful glassmorphic login card
- **Register** (`/register/`) - Create new accounts
- **Logout** (`/logout/`) - Confirmation page with smooth exit
- All stored in Supabase PostgreSQL

## 👤 User Profile Management
- **Profile Page** (`/profile/`) - View account stats and journey
- **Edit Profile** (`/profile/edit/`) - Update name, email, profile picture
- **Change Password** (`/profile/change-password/`) - Secure password updates
- **Avatar Upload** - Profile pictures stored in Supabase Storage (mhms bucket)
- **Auto-generated Avatars** - Fallback to UI Avatars API

## 📝 Journal Features
- **Dashboard** (`/`) - Mood overview with Chart.js visualizations
  - Stats cards showing total entries, weekly count, streak
  - Interactive mood trend chart
  - Recent entries list
  
- **New Entry** (`/new-entry/`) - Create journal entries
  - Large textarea with character counter
  - Writing tips card
  - AI emotion analysis on submit
  - Real-time sentiment scoring
  
- **History** (`/history/`) - Timeline view of all entries
  - Beautiful timeline with gradient connector
  - Emotion badges
  - Sentiment progress bars
  - Alert notifications for concerning patterns
  - Filter tabs (All Time, This Month, This Week)

## 🤖 AI Analysis
- **Model**: mental-roberta-base (MentalBERT family)
- **Fallback**: distilbert sentiment analysis
- **Features**:
  - Multi-emotion detection (joy, sadness, fear, anger, etc.)
  - Sentiment scoring (-1 to +1)
  - Alert system for negative patterns
  - Trained on mental health text data

## 🗄️ Database (Supabase PostgreSQL)
- **Users**: auth_user table
- **Profiles**: journal_userprofile table
- **Mood Logs**: journal_moodlog table
- **Storage**: mhms bucket for profile pictures
- **Security**: Row-level security enabled
- **Sync**: Real-time data sync across devices

## 🎯 Key Features
✅ Secure authentication with hashed passwords
✅ Profile customization with photo uploads
✅ AI-powered emotion detection
✅ Visual mood tracking with charts
✅ Timeline view of emotional journey
✅ Alert system for mental health concerns
✅ Privacy-focused design
✅ Cloud storage with Supabase
✅ Responsive Apple-inspired UI
✅ Real-time character counter
✅ Dropdown user menu
✅ Smooth page transitions

## 🚀 Quick Start
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/login/

Test account: `testuser` / `test123`
