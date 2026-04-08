#!/usr/bin/env python
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

print("Testing Supabase Storage Upload...")
print("=" * 60)

# Create a test file
test_content = b"Test image content"
file_path = "profiles/test/test.txt"

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'text/plain'
}

print(f"Uploading to: {SUPABASE_URL}/storage/v1/object/mhms/{file_path}")

try:
    with httpx.Client() as client:
        # Try upload
        response = client.post(
            f'{SUPABASE_URL}/storage/v1/object/mhms/{file_path}',
            content=test_content,
            headers=headers,
            timeout=30.0
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 201]:
            public_url = f'{SUPABASE_URL}/storage/v1/object/public/mhms/{file_path}'
            print(f"\n✅ Upload successful!")
            print(f"Public URL: {public_url}")
            
            # Test if file is accessible
            test_response = client.get(public_url)
            if test_response.status_code == 200:
                print("✅ File is publicly accessible!")
            else:
                print(f"⚠️ File uploaded but not accessible: {test_response.status_code}")
                print("Make sure the 'mhms' bucket is set to PUBLIC in Supabase Storage settings")
        else:
            print(f"❌ Upload failed")
            print("\nTroubleshooting:")
            print("1. Check if 'mhms' bucket exists in Supabase Storage")
            print("2. Make sure bucket is set to PUBLIC")
            print("3. Verify your SUPABASE_KEY has storage permissions")
            
except Exception as e:
    print(f"❌ Error: {e}")
