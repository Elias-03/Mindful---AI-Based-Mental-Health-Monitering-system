"""
Test the direct Google AI API without heavy libraries
"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
print(f"✓ API Key loaded: {api_key[:20]}...")

# Direct API call
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Hello! Can you help me with stress? Keep it brief."
        }]
    }],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 200
    }
}

print("\n🚀 Testing direct API call...")

try:
    with httpx.Client(timeout=10.0) as client:
        response = client.post(api_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
            print("\n✅ SUCCESS! AI Response:")
            print(f"\n{ai_response}\n")
        elif response.status_code == 429:
            print("\n⚠️  Rate limit hit. Wait 30-60 seconds and try again.")
        else:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            
except httpx.TimeoutException:
    print("\n⏱️  Request timed out. Check your connection.")
except Exception as e:
    print(f"\n❌ Error: {e}")
