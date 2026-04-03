from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
import httpx
import os
from django.conf import settings

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'journal/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update basic info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            file = request.FILES['profile_picture']
            file_path = f"profiles/{request.user.id}/{file.name}"
            
            # Upload to Supabase Storage
            headers = {
                'apikey': settings.SUPABASE_KEY,
                'Authorization': f'Bearer {settings.SUPABASE_KEY}',
            }
            
            try:
                file_content = file.read()
                with httpx.Client() as client:
                    response = client.post(
                        f'{settings.SUPABASE_URL}/storage/v1/object/mhms/{file_path}',
                        content=file_content,
                        headers={**headers, 'Content-Type': file.content_type},
                        timeout=30.0
                    )
                    if response.status_code in [200, 201]:
                        profile.profile_picture_url = f'{settings.SUPABASE_URL}/storage/v1/object/public/mhms/{file_path}'
                        profile.save()
                        messages.success(request, 'Profile picture updated!')
                    else:
                        messages.error(request, f'Upload failed: {response.status_code} - {response.text}')
            except Exception as e:
                messages.error(request, f'Upload failed: {str(e)}')
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('journal:profile')
    
    return render(request, 'journal/edit_profile.html', {'profile': profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('journal:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'journal/change_password.html', {'form': form})
