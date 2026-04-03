# Get Your Supabase Database Connection String

To connect Django directly to Supabase PostgreSQL:

## Step 1: Get Database Password

1. Go to your Supabase dashboard
2. Click **Settings** (gear icon)
3. Click **Database**
4. Scroll to **Connection string** section
5. Select **URI** tab
6. You'll see something like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xouvmjdemsjvphfrjqpq.supabase.co:5432/postgres
   ```

## Step 2: Get Your Password

The connection string shows `[YOUR-PASSWORD]` - you need to replace this with your actual database password.

**If you forgot your password:**
1. In the same Database settings page
2. Scroll to **Database password** section
3. Click **Reset database password**
4. Copy the new password (you won't see it again!)

## Step 3: Add to .env

Your complete connection string should look like:
```
SUPABASE_DB_URL=postgresql://postgres:your_actual_password_here@db.xouvmjdemsjvphfrjqpq.supabase.co:5432/postgres
```

Add this line to your `.env` file.

## Why This is Better:
- All data (users, sessions, mood logs) in one place
- Easy backups and exports
- Access from multiple devices/servers
- Supabase handles scaling and security
- No local database files to manage
