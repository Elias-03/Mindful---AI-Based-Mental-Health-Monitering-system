from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import MoodLog, Notification
from .emotion_analyzer import EmotionAnalyzer
from .supabase_client import SupabaseClient
import json
import io
import os
from django.conf import settings
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, toColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, PolyLine, Line, String, Group, Rect
from reportlab.graphics import renderPDF
from datetime import datetime

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
