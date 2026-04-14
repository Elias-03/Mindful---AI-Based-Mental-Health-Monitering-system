"""
Quick test script for the chatbot API
Run this after starting the server to test the chatbot
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Test the API key
api_key = os.getenv('GOOGLE_AI_API_KEY')
print(f"API Key loaded: {api_key[:20]}..." if api_key else "API Key not found!")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # Test message
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Hello! Can you help me with stress?"
        )
        print("\n✅ Chatbot is working!")
        print(f"\nTest Response:\n{response.text}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
else:
    print("\n❌ Please add GOOGLE_AI_API_KEY to your .env file")
