from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MoodLog, Notification
from .emotion_analyzer import EmotionAnalyzer
from .supabase_client import SupabaseClient
import json

analyzer = EmotionAnalyzer()
supabase = SupabaseClient()

@login_required
def dashboard(request):
    recent_logs = MoodLog.objects.filter(user=request.user)[:7]
    return render(request, 'journal/dashboard_apple.html', {
        'recent_logs': recent_logs
    })

@login_required
def new_entry(request):
    if request.method == 'POST':
        entry_text = request.POST.get('entry_text', '')
        
        analysis = analyzer.analyze(entry_text)
        print(f"DEBUG: Analysis results: {analysis}") # Debug print
        
        alert_level = 'none'
        alert_text = ''
        if analysis['sentiment_score'] < -0.4: # Slightly more sensitive
            alert_level = 'warning'
            alert_text = 'Consider talking to a friend or professional.'
            print(f"DEBUG: Alert triggered: {alert_level}") # Debug print
        
        mood_log = MoodLog.objects.create(
            user=request.user,
            entry_summary=entry_text[:200],
            emotions_json=analysis['emotions'],
            dominant_emotion=analysis['dominant_emotion'],
            sentiment_score=analysis['sentiment_score'],
            alert_level=alert_level,
            alert_text=alert_text
        )

        if alert_level == 'warning':
            Notification.objects.create(
                user=request.user,
                title='Mood Alert Detected',
                message='Your recent journal entry shows a high level of distress. Remember to be kind to yourself and reach out for support if needed.',
                notification_type='mood_alert',
                link=f'/history/'
            )
        elif analysis['sentiment_score'] > 0.4:
            Notification.objects.create(
                user=request.user,
                title='Great Mood Captured!',
                message=f'It is wonderful to see you feeling {analysis["dominant_emotion"]}. Keep up this positive energy!',
                notification_type='mood_positive',
                link=f'/history/'
            )
        else:
            Notification.objects.create(
                user=request.user,
                title='Journal Entry Saved',
                message='Your thoughts have been safely recorded. Consistency is key to mental wellness!',
                notification_type='mood_neutral',
                link=f'/history/'
            )
        
        if supabase.url and supabase.key:
            supabase.save_mood_log({
                'user_id': str(request.user.id),
                'timestamp': mood_log.timestamp.isoformat(),
                'entry_summary': mood_log.entry_summary,
                'emotions_json': analysis['emotions'],
                'dominant_emotion': analysis['dominant_emotion'],
                'sentiment_score': analysis['sentiment_score'],
                'alert_level': alert_level,
                'alert_text': alert_text
            })
        
        return redirect('journal:dashboard')
    
    return render(request, 'journal/new_entry_apple.html')

@login_required
def history(request):
    logs = MoodLog.objects.filter(user=request.user)[:30]
    return render(request, 'journal/history_apple.html', {'logs': logs})

@login_required
def mood_data_api(request):
    logs = MoodLog.objects.filter(user=request.user)[:14]
    data = {
        'labels': [log.timestamp.strftime('%Y-%m-%d') for log in reversed(logs)],
        'sentiment': [log.sentiment_score for log in reversed(logs)],
        'emotions': [log.dominant_emotion for log in reversed(logs)]
    }
    return JsonResponse(data)

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'journal/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})
