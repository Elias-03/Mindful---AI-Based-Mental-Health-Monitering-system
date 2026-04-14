#!/usr/bin/env python
"""Test Hugging Face AI Chatbot"""
import httpx
import json

def test_huggingface_api(message):
    """Test Hugging Face Inference API"""
    try:
        print(f"\n🤖 Testing Hugging Face AI with message: '{message}'")
        print("=" * 60)
        
        # Using Microsoft's DialoGPT - free and no API key needed
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
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
        
        print("\n📡 Sending request to Hugging Face...")
        
        with httpx.Client(timeout=15.0) as client:
            response = client.post(api_url, json=payload)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ Success! Raw response:")
                print(json.dumps(result, indent=2))
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    print(f"\n💬 Generated Text:")
                    print(generated_text)
                    
                    # Extract only the assistant's response
                    if 'Assistant:' in generated_text:
                        ai_response = generated_text.split('Assistant:')[-1].strip()
                        print(f"\n🎯 Extracted AI Response:")
                        print(f"'{ai_response}'")
                        return ai_response
                    else:
                        print("\n⚠️ Could not find 'Assistant:' in response")
                        return generated_text
                else:
                    print("\n❌ Unexpected response format")
                    return None
            elif response.status_code == 503:
                print("\n⏳ Model is loading... This can take 20-30 seconds on first request")
                print("Try again in a moment!")
                return None
            else:
                print(f"\n❌ Error: {response.status_code}")
                print(response.text)
                return None
                
    except httpx.TimeoutException:
        print("\n⏱️ Request timed out. The model might be loading.")
        return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

def test_fallback_response(message):
    """Test the fallback response system"""
    print(f"\n🔄 Testing Fallback System with message: '{message}'")
    print("=" * 60)
    
    msg = message.lower()
    
    responses = {
        'anxious': [
            "I hear you. Anxiety can feel overwhelming. Try the 4-7-8 breathing: in for 4, hold for 7, out for 8. You've got this. 💙"
        ],
        'sad': [
            "I'm sorry you're feeling down. It's okay to not be okay. What's one small thing that brought you joy today? 🌟"
        ],
        'happy': [
            "That's wonderful! What made today special? Soak in this feeling - you deserve it! ✨"
        ]
    }
    
    for keyword, response_list in responses.items():
        if keyword in msg:
            response = response_list[0]
            print(f"\n✅ Matched keyword: '{keyword}'")
            print(f"💬 Response: {response}")
            return response
    
    default = "I'm here to listen. Tell me more about what's on your mind. Sometimes just expressing it helps. 💙"
    print(f"\n✅ Using default response")
    print(f"💬 Response: {default}")
    return default

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 HUGGING FACE AI CHATBOT TEST")
    print("=" * 60)
    
    # Test messages
    test_messages = [
        "I'm feeling anxious today",
        "I'm really happy!",
        "Tell me something supportive"
    ]
    
    for message in test_messages:
        # Test Hugging Face
        hf_response = test_huggingface_api(message)
        
        if not hf_response:
            print("\n🔄 Hugging Face failed, testing fallback...")
            fallback_response = test_fallback_response(message)
        
        print("\n" + "-" * 60 + "\n")
        input("Press Enter to test next message...")
    
    print("\n✅ All tests complete!")
    print("\n💡 Note: If you see 503 errors, the model is loading.")
    print("   Wait 20-30 seconds and try again.")
    print("\n🎯 The chatbot will automatically use fallback if Hugging Face fails!")
