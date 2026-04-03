# Create User in Supabase

You have two options to create users in Supabase:

## Option 1: Via Supabase Dashboard (Easiest)

1. Go to your Supabase dashboard
2. Click **Authentication** in the sidebar
3. Click **Users** tab
4. Click **Add User** button
5. Enter:
   - Email: `test@example.com`
   - Password: `test123`
   - Auto Confirm User: ✅ (check this)
6. Click **Create User**

## Option 2: Via SQL (Create auth user directly)

Go to **SQL Editor** and run:

```sql
-- Insert a test user into Supabase auth
INSERT INTO auth.users (
    instance_id,
    id,
    aud,
    role,
    email,
    encrypted_password,
    email_confirmed_at,
    created_at,
    updated_at,
    confirmation_token,
    raw_app_meta_data,
    raw_user_meta_data
) VALUES (
    '00000000-0000-0000-0000-000000000000',
    gen_random_uuid(),
    'authenticated',
    'authenticated',
    'test@example.com',
    crypt('test123', gen_salt('bf')),
    NOW(),
    NOW(),
    NOW(),
    '',
    '{"provider":"email","providers":["email"]}',
    '{}'
);
```

## Option 3: Enable Email Signup

In Supabase Dashboard:
1. Go to **Authentication** → **Providers**
2. Enable **Email** provider
3. Disable email confirmation (for testing)
4. Users can then register via your app's register page

After creating the user, you can login with that email/password.
