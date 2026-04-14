from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import MoodLog, Notification
from .emotion_analyzer import EmotionAnalyzer
from .supabase_client import SupabaseClient
import json
import io
import os
import httpx
from django.conf import settings
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, toColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, PolyLine, Line, String, Group, Rect
from reportlab.graphics import renderPDF
from datetime import datetime, timedelta

analyzer = EmotionAnalyzer()
supabase = SupabaseClient()

@login_required
def dashboard(request):
    recent_logs = MoodLog.objects.filter(user=request.user).order_by('-timestamp')[:7]
    
    # Calculate stats
    total_entries = MoodLog.objects.filter(user=request.user).count()
    week_entries = MoodLog.objects.filter(
        user=request.user,
        timestamp__gte=datetime.now() - timedelta(days=7)
    ).count()
    
    return render(request, 'journal/dashboard_ultra.html', {
        'recent_logs': recent_logs,
        'total_entries': total_entries,
        'week_entries': week_entries,
    })

@login_required
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message.strip():
                return JsonResponse({'error': 'Please enter a message'}, status=400)
            
            # Try multiple AI services in order
            response_text = None
            ai_type = 'Mindful AI'
            
            # 1. Try Groq (Free, fast, no API key for basic use)
            try:
                groq_response = call_groq_api(user_message)
                if groq_response:
                    response_text = groq_response
                    ai_type = 'Groq AI'
            except:
                pass
            
            # 2. Try Hugging Face (Free, no API key needed)
            if not response_text:
                try:
                    hf_response = call_huggingface_api(user_message)
                    if hf_response:
                        response_text = hf_response
                        ai_type = 'Hugging Face'
                except:
                    pass
            
            # 3. Try Google Gemini (if configured)
            if not response_text and settings.GOOGLE_AI_API_KEY:
                try:
                    gemini_response = call_gemini_api(user_message, settings.GOOGLE_AI_API_KEY)
                    if gemini_response:
                        response_text = gemini_response
                        ai_type = 'Gemini AI'
                except:
                    pass
            
            # 4. Fallback to rule-based responses
            if not response_text:
                response_text = get_smart_fallback_response(user_message)
                ai_type = 'Mindful AI'
            
            return JsonResponse({
                'response': response_text,
                'ai_type': ai_type
            })
            
        except Exception as e:
            return JsonResponse({
                'response': get_smart_fallback_response(user_message if 'user_message' in locals() else ''),
                'ai_type': 'Mindful AI'
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def call_groq_api(message):
    """Call Groq API - Free and fast"""
    try:
        # Groq's free inference endpoint (no API key needed for basic use)
        api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Note: For production, you'd want to get a free API key from groq.com
        # But we'll use the fallback for now
        return None
    except:
        return None

def call_huggingface_api(message):
    """Call Hugging Face Inference API (Free tier available)"""
    try:
        # Using the new router endpoint
        api_url = "https://router.huggingface.co/models/microsoft/DialoGPT-medium"
        
        system_context = "You are a compassionate mental health companion. Provide supportive, empathetic responses in 2-3 sentences."
        
        payload = {
            "inputs": f"{system_context}\n\nUser: {message}\nAssistant:",
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        with httpx.Client(timeout=8.0) as client:
            response = client.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extract only the assistant's response
                    if 'Assistant:' in generated_text:
                        ai_response = generated_text.split('Assistant:')[-1].strip()
                        if ai_response and len(ai_response) > 10:
                            return ai_response[:300]  # Limit length
            return None
    except:
        return None

def call_gemini_api(message, api_key):
    """Call Google Gemini API"""
    try:
        system_prompt = """You are an advanced AI mental wellness companion. You provide empathetic, 
        supportive, and insightful responses. Keep responses concise (2-3 sentences), warm, and actionable. 
        If someone is in crisis, gently remind them to seek professional help. Never diagnose or replace 
        professional mental health care. Be conversational and human-like."""
        
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        with httpx.Client(timeout=10.0) as client:
            response = client.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                return ai_response.strip()
            return None
    except:
        return None

def get_smart_fallback_response(message):
    """Enhanced rule-based chatbot with context awareness and variety"""
    import random
    msg = message.lower()
    
    # Mental health keywords and responses with more variety
    responses = {
        'anxious': [
            "I hear you. Anxiety can feel overwhelming. Try the 4-7-8 breathing: breathe in for 4, hold for 7, breathe out for 8. You've got this. 💙",
            "Feeling anxious is tough. Ground yourself with the 5-4-3-2-1 technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
            "Anxiety is your body trying to protect you, but sometimes it's overactive. What's one small thing you can control right now? Start there. 🌟",
            "I understand. When anxiety hits, try progressive muscle relaxation - tense each muscle group for 5 seconds, then release. Start with your toes and work up.",
            "That sounds really hard. Remember: this feeling is temporary. You've survived 100% of your worst days so far. What helped you through before?"
        ],
        'anxiety': [
            "Anxiety can be paralyzing. Try this: place your hand on your heart, take a deep breath, and say 'I am safe right now.' Repeat 3 times. 💙",
            "I get it. Anxiety lies to us. Challenge the thought: Is this fear based on facts or feelings? What would you tell a friend feeling this way?",
            "When anxiety spirals, try the 'worry time' technique: set aside 15 minutes later to worry, then redirect your mind now. You're in control. 🌟",
            "Your anxiety is valid, but it doesn't define you. Try naming it - 'This is anxiety talking, not truth.' What's one thing that usually calms you?"
        ],
        'panic': [
            "You're having a panic attack. You're safe. This will pass. Focus on your breath: in through nose (4 counts), out through mouth (6 counts). I'm here. 💙",
            "Panic attacks are scary but not dangerous. You're safe. Try this: name 5 blue things you can see. This grounds you in the present moment.",
            "I know this feels terrifying. Splash cold water on your face or hold ice cubes. This activates your dive reflex and calms your nervous system. You're okay."
        ],
        'sad': [
            "I'm sorry you're feeling down. It's okay to not be okay sometimes. What's one small thing that brought you even a tiny bit of joy today? 🌟",
            "Sadness is valid and important. Be gentle with yourself today. Sometimes just getting through the day is enough, and that's perfectly okay. 💙",
            "Your feelings matter. When you're ready, try writing down 3 things you're grateful for - even tiny things. It can help shift perspective.",
            "I see you're hurting. Sadness is part of being human. What would you do to comfort a friend feeling this way? Can you offer yourself that same kindness?",
            "It's okay to feel sad. Try this: put on a song that matches your mood, then gradually shift to something more uplifting. Music can help process emotions. 🎵"
        ],
        'depressed': [
            "Depression is heavy, and I'm sorry you're carrying this weight. Please consider reaching out to a mental health professional - you deserve support. You're not alone. 💙",
            "What you're feeling is real and valid. Small steps count: can you do one tiny thing today? Drink water, open a window, text a friend. That's enough. 🌙",
            "Depression lies and tells you things will never get better. But you've felt better before, and you will again. Have you talked to a therapist? They can help.",
            "I'm concerned about you. Depression is treatable. Please reach out to a counselor or call 988 for support. You matter, and help is available. 💙"
        ],
        'stressed': [
            "Stress is real. Let's break it down: what's the ONE thing you can control right now? Start there. You don't have to do everything at once. 💪",
            "I get it - stress can be paralyzing. Try this: write down 3 things stressing you, then pick just ONE to focus on. Baby steps count. 🌟",
            "Stress often comes from trying to control everything. What's one thing you can let go of today? Give yourself permission to not be perfect.",
            "When stressed, try the 'brain dump': write everything down for 5 minutes without stopping. Getting it out of your head helps. Then prioritize. 📝",
            "Stress is your body's alarm system. Listen to it. What's it trying to tell you? Maybe you need rest, boundaries, or help? All are valid needs. 💙"
        ],
        'overwhelmed': [
            "Feeling overwhelmed means you care deeply. But you can't pour from an empty cup. What's one thing you can delegate or postpone? You matter too. 💙",
            "When everything feels like too much, focus on the next 5 minutes. Just the next 5. You can do anything for 5 minutes. Then reassess. 🌟",
            "Overwhelm is a sign you're doing too much. What would happen if you said 'no' to one thing today? Try it. Your wellbeing comes first.",
            "I hear you. Try this: close your eyes, take 3 deep breaths, then ask yourself 'What's the most important thing right now?' Do only that. 💪"
        ],
        'happy': [
            "That's wonderful! I love hearing this. What made today special? Soak in this feeling - you deserve it! ✨",
            "Your happiness is contagious! Keep riding this wave. Remember this moment when things get tough - you can get back here again. 🌟",
            "This is beautiful! Celebrate this win, no matter how small. Joy is precious - hold onto it. What are you most grateful for right now? 💙",
            "I'm so glad you're feeling good! Happiness is worth savoring. Take a mental snapshot of this moment - you earned this feeling. ✨",
            "Yes! This is amazing! Share this joy with someone - happiness multiplies when shared. Who can you tell about this? 🎉"
        ],
        'excited': [
            "Your excitement is amazing! What's got you feeling this way? I'd love to hear about it! Tell me more! ✨",
            "This energy is wonderful! Channel it into something creative or meaningful. You're radiating positivity! What's your next move? 🌟",
            "I can feel your excitement! This is the good stuff. What are you most looking forward to? Let's celebrate this feeling! 🎉"
        ],
        'tired': [
            "Rest isn't weakness - it's essential. If you can, take 10 minutes for yourself. Even a short break can help recharge. 🌙",
            "Exhaustion is your body's way of asking for care. Listen to it. What's one thing you can let go of today to create space for rest? 💙",
            "Being tired is valid. You don't have to earn rest - you deserve it simply because you exist. Can you give yourself permission to pause? 🌟",
            "Fatigue is real. Try this: set a timer for 15 minutes and do absolutely nothing. No phone, no tasks. Just breathe. You need this. 🌙",
            "Your body is talking to you. Tired means you need rest, not more coffee. What's one way you can be gentler with yourself today? 💙"
        ],
        'exhausted': [
            "Exhaustion is serious. You're running on empty. Please prioritize rest today - cancel something if you need to. Your health matters most. 🌙",
            "I'm worried about you. Chronic exhaustion can lead to burnout. Can you take a real break? Not just sleep, but actual rest and recovery? 💙",
            "You can't keep going like this. What would you need to feel rested? More sleep? Less responsibility? Help? All are valid. Ask for what you need. 🌟"
        ],
        'lonely': [
            "Loneliness is painful, and I'm sorry you're feeling this way. You're not alone in feeling alone - many people understand this. Can you reach out to one person today? 💙",
            "Feeling lonely doesn't mean you're unlovable - it means you're human and need connection. That's beautiful, actually. Who could you connect with, even briefly? 🌟",
            "Loneliness hurts. Try this: text someone 'thinking of you' or join an online community around your interests. Small connections count. You matter. 💙",
            "I hear you. Loneliness is different from being alone. What kind of connection are you craving? Sometimes naming it helps us find it. 🌟"
        ],
        'angry': [
            "Anger is a valid emotion - it's telling you something matters to you. Can you identify what's underneath the anger? Often it's hurt or fear. 💪",
            "It's okay to be angry. Try this: write down everything you're angry about, then tear it up or burn it (safely). Physical release can help. 🔥",
            "Anger is energy. Channel it: go for a run, punch a pillow, or write an angry letter (don't send it). Let it out safely. You're allowed to feel this. 💪",
            "I hear your anger. It's valid. But holding onto it hurts you most. What would help you release this? Movement? Talking? Creating? 🌟"
        ],
        'scared': [
            "Fear is your brain trying to protect you. But sometimes it overreacts. What's the worst that could realistically happen? And could you handle it? You're more resilient than you think. 💙",
            "Being scared is human. Courage isn't the absence of fear - it's acting despite it. What's one small brave thing you could do today? 🌟",
            "Fear can be paralyzing. Try this: imagine your fear as a small child. What would you say to comfort them? Now say that to yourself. 💙",
            "I understand you're scared. Fear often feels bigger than it is. Break it down: what specifically scares you? Sometimes naming it reduces its power. 🌟"
        ],
        'worried': [
            "Worry is your mind trying to prepare for the future. But most worries never happen. Try this: write down your worry, then write 3 possible positive outcomes. 💙",
            "I hear you're worried. Ask yourself: Is this something I can control? If yes, make a plan. If no, practice letting it go. Easier said than done, I know. 🌟",
            "Worry is exhausting. Try the 'worry time' technique: schedule 15 minutes to worry later, then redirect your mind now. You're in control. 💪"
        ],
        'help': [
            "I'm here to listen and support you. If you're in crisis, please reach out to a crisis helpline or mental health professional immediately. You deserve real help. 💙",
            "I care about your wellbeing. While I can offer support, please consider talking to a therapist or counselor for deeper help. You're worth it. 🌟",
            "Asking for help is brave. I'm here, but for serious concerns, please reach out to: Crisis Text Line (text HOME to 741741) or call 988. You matter. 💙"
        ],
        'suicide': [
            "I'm deeply concerned about you. Please reach out to a crisis helpline immediately: National Suicide Prevention Lifeline: 988 or 1-800-273-8255. Your life matters. 💙",
            "You matter more than you know. Please call 988 or text 'HELLO' to 741741 right now. There are people who want to help you through this. You're not alone. 🌟",
            "This is serious. Please get help NOW: Call 988, go to your nearest ER, or call 911. You deserve to live. This pain is temporary, but suicide is permanent. 💙"
        ],
        'crisis': [
            "This sounds serious. Please reach out for immediate help: Call 988 (Suicide & Crisis Lifeline) or text 'HELLO' to 741741. You deserve professional support right now. 💙",
            "I'm very concerned. Please don't face this alone. Call 988 or go to your nearest emergency room. You matter, and help is available right now. 🌟"
        ],
        'grateful': [
            "Gratitude is powerful! What are you grateful for? Savoring the good moments helps build resilience for tough times. Keep noticing the good. ✨",
            "I love this! Gratitude shifts our perspective. Try keeping a gratitude journal - write 3 things daily. It rewires your brain for positivity. 🌟"
        ],
        'hopeful': [
            "Hope is beautiful! Hold onto that feeling. Hope is what keeps us moving forward. What are you hopeful about? 🌟",
            "Yes! Hope is powerful. Even a tiny bit of hope can light the way forward. Keep nurturing that feeling. You're on the right path. ✨"
        ]
    }
    
    # Check for keywords with priority (crisis keywords first)
    crisis_keywords = ['suicide', 'kill myself', 'end it', 'crisis', 'die']
    for keyword in crisis_keywords:
        if keyword in msg:
            return random.choice(responses.get('suicide', responses['crisis']))
    
    # Check other keywords
    for keyword, response_list in responses.items():
        if keyword in msg:
            return random.choice(response_list)
    
    # Default supportive responses with more variety
    default_responses = [
        "I'm here to listen. Tell me more about what's on your mind. Sometimes just expressing it helps. 💙",
        "Thank you for sharing with me. Your feelings are valid. What would help you feel even 1% better right now? 🌟",
        "I appreciate you opening up. Remember: you're stronger than you think, and you don't have to face this alone. 💙",
        "That sounds challenging. What's one small step you could take today to care for yourself? You deserve kindness, especially from yourself. 🌟",
        "I hear you. It takes courage to express how you're feeling. What support do you need right now? 💙",
        "Your experience matters. While I'm here to listen, please consider reaching out to a mental health professional for deeper support. You're worth it. 🌟",
        "I'm listening. Sometimes we just need someone to hear us. What's weighing on you most right now? 💙",
        "Thank you for trusting me with this. How long have you been feeling this way? Understanding the timeline can help. 🌟",
        "I want to support you. What would be most helpful right now - advice, validation, or just someone to listen? 💙",
        "You're not alone in this. Many people struggle with similar feelings. What's one thing that usually helps you feel better? 🌟"
    ]
    
    return random.choice(default_responses)

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

@login_required
def download_report_pdf(request):
    logs = list(MoodLog.objects.filter(user=request.user)[:10])
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=toColor('#1d1d1f'),
        spaceAfter=15,
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=toColor('#86868b'),
        spaceAfter=20
    )
    
    # Header with Logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'fav.ico')
    if os.path.exists(logo_path):
        logo = Image(logo_path, 0.4*inch, 0.4*inch)
        logo.hAlign = 'LEFT'
        elements.append(logo)
    
    elements.append(Paragraph("Your Mental Wellness Snapshot", title_style))
    elements.append(Paragraph(f"Created for {request.user.get_full_name() or request.user.username} • {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    
    # Recent Performance Table
    elements.append(Paragraph("Your Recent Mood Overview", styles['Heading2']))
    elements.append(Spacer(1, 8))
    
    if logs:
        avg_sentiment = sum(log.sentiment_score for log in logs) / len(logs)
        moods = [log.dominant_emotion for log in logs]
        most_common_mood = max(set(moods), key=moods.count)
        
        # Human readable mood level
        mood_vibe = "Very High" if avg_sentiment > 0.6 else "High" if avg_sentiment > 0.2 else "Neutral" if avg_sentiment > -0.2 else "Low" if avg_sentiment > -0.6 else "Very Low"
        
        summary_data = [
            ["Item", "Detail"],
            ["Total Journal Notes", str(len(logs))],
            ["Overall Mood Vibe", f"{mood_vibe} ({avg_sentiment:.2f})"],
            ["Main Feeling Recently", most_common_mood.title()],
            ["Last Check-in Date", logs[0].timestamp.strftime('%B %d, %Y at %H:%M')],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), toColor('#0071e3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), toColor('#f5f5f7')),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Improved Mood Trend Graph
        elements.append(Paragraph("How Your Vibe Has Changed", styles['Heading2']))
        elements.append(Spacer(1, 8))
        
        graph_width = 10 * inch
        graph_height = 2.0 * inch
        d = Drawing(graph_width, graph_height)
        
        # Grid lines and background
        d.add(Rect(0, 0, graph_width, graph_height, fillColor=toColor('#fafafa'), strokeColor=toColor('#d2d2d7')))
        
        # Y-Axis Labels
        d.add(String(-50, graph_height - 10, "Very High", fontSize=8, fillColor=toColor('#0071e3')))
        d.add(Line(0, graph_height, graph_width, graph_height, strokeColor=toColor('#d2d2d7'), strokeDashArray=[1, 2]))
        
        d.add(String(-50, graph_height/2 - 4, "Neutral", fontSize=8, fillColor=toColor('#86868b')))
        d.add(Line(0, graph_height/2, graph_width, graph_height/2, strokeColor=toColor('#86868b'), strokeDashArray=[2, 2]))
        
        d.add(String(-50, 4, "Very Low", fontSize=8, fillColor=toColor('#ff3b30')))
        d.add(Line(0, 0, graph_width, 0, strokeColor=toColor('#d2d2d7'), strokeDashArray=[1, 2]))
        
        if len(logs) > 1:
            trend_logs = list(reversed(logs)) # Show all 10 for better trend
            points = []
            x_step = graph_width / (len(trend_logs) - 1) if len(trend_logs) > 1 else graph_width
            
            for i, log in enumerate(trend_logs):
                x = i * x_step
                y = (log.sentiment_score + 1) / 2 * graph_height
                points.extend([x, y])
                
                # Small data point
                d.add(Rect(x-1.5, y-1.5, 3, 3, fillColor=toColor('#0071e3'), strokeColor=None))
                
                # Date label for first and last point
                if i == 0 or i == len(trend_logs) - 1:
                    date_str = log.timestamp.strftime('%b %d')
                    d.add(String(x - 15, -15, date_str, fontSize=8, fillColor=toColor('#86868b')))
            
            d.add(PolyLine(points, strokeColor=toColor('#0071e3'), strokeWidth=1.5))
        
        # Adjust drawing position to leave room for labels
        g = Group(d)
        g.translate(60, 20) # Move right to make room for Y labels, up for X labels
        
        drawing_container = Drawing(graph_width + 80, graph_height + 40)
        drawing_container.add(g)
        elements.append(drawing_container)
        
        elements.append(Spacer(1, 15))
        
        # Detailed History (Limited to 10)
        elements.append(Paragraph("Your Last 10 Journal Notes", styles['Heading2']))
        elements.append(Spacer(1, 8))
        
        history_data = [["When", "Feeling", "Mood Level", "Your Summary"]]
        for log in logs:
            vibe_label = "High" if log.sentiment_score > 0.3 else "Neutral" if log.sentiment_score > -0.3 else "Low"
            history_data.append([
                log.timestamp.strftime('%b %d, %H:%M'),
                log.dominant_emotion.title(),
                vibe_label,
                Paragraph(log.entry_summary[:120] + ("..." if len(log.entry_summary) > 120 else ""), styles['Normal'])
            ])
            
        history_table = Table(history_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 6.3*inch])
        history_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), toColor('#1d1d1f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(history_table)
    else:
        elements.append(Paragraph("Start writing your journal to see your wellness snapshot!", styles['Normal']))
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="your_mindful_report_{datetime.now().strftime("%Y%m%d")}.pdf"'
    response.write(pdf)
    
    return response
