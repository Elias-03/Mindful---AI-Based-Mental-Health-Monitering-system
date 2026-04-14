# AI Chatbot Setup Complete! 🤖

Your mental health journal now has an AI-powered chatbot on the main dashboard!

## What's Been Added

1. **Google AI Integration**: Using Google's Gemini 2.5 Flash model
2. **Chatbot Interface**: Clean, Apple-style chat interface on the dashboard
3. **Mental Health Context**: The bot is configured to provide compassionate mental wellness support
4. **Error Handling**: Graceful handling of API rate limits and errors

## How to Use

1. **Start the server**:
   ```bash
   START.bat
   ```
   Or manually:
   ```bash
   python manage.py runserver
   ```

2. **Visit the dashboard**: http://127.0.0.1:8000/

3. **Chat with the AI**: The chatbot is right at the top of your dashboard!

## Features

- Real-time chat interface
- Typing indicators
- Smooth animations
- Mental health-focused responses
- Compassionate and supportive AI assistant
- Automatic fallback between models
- Rate limit handling

## API Key & Quota

Your Google AI API key has been added to the `.env` file:
```
GOOGLE_AI_API_KEY=AIzaSyBA4Qkh9OXdrN9OThTzuaWzaaBqg0XOXmY
```

**Note**: The free tier has rate limits. If you see quota errors, wait a few minutes and try again. The chatbot will automatically handle these errors gracefully.

## Files Modified

- `journal/views.py` - Added chatbot API endpoint with error handling
- `journal/urls.py` - Added chatbot route
- `templates/journal/dashboard_apple.html` - Added chatbot UI
- `mental_health/settings.py` - Added API key configuration
- `.env` - Added Google AI API key
- `requirements.txt` - Added google-genai library

## Try It Out!

Ask the chatbot things like:
- "How are you feeling today?"
- "I'm feeling stressed about work"
- "Can you help me with anxiety?"
- "I need someone to talk to"
- "What are some coping strategies?"

The AI is configured to be supportive, empathetic, and helpful for mental wellness conversations.

## Troubleshooting

If you see "quota exceeded" errors:
- Wait 30-60 seconds and try again
- The free tier has limits on requests per minute
- Consider upgrading to a paid plan for higher limits

Enjoy your new AI companion! 💙

