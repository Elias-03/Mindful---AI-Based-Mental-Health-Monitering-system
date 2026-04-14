import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv('GOOGLE_AI_API_KEY')
client = genai.Client(api_key=api_key)

print("Available models:")
for model in client.models.list():
    print(f"- {model.name}")
