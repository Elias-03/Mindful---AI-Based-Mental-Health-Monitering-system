import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
api_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("Checking available models...\n")

try:
    with httpx.Client(timeout=10.0) as client:
        response = client.get(api_url)
        
        if response.status_code == 200:
            result = response.json()
            models = result.get('models', [])
            
            print("Available models for generateContent:\n")
            for model in models:
                if 'generateContent' in model.get('supportedGenerationMethods', []):
                    print(f"✓ {model['name']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
except Exception as e:
    print(f"Error: {e}")
