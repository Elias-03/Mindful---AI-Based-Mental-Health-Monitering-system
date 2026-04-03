import httpx
from django.conf import settings

class SupabaseClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.url = settings.SUPABASE_URL
            cls._instance.key = settings.SUPABASE_KEY
            cls._instance.headers = {
                'apikey': cls._instance.key,
                'Authorization': f'Bearer {cls._instance.key}',
                'Content-Type': 'application/json'
            }
        return cls._instance
    
    def save_mood_log(self, data):
        if not self.url or not self.key:
            return None
        try:
            with httpx.Client() as client:
                response = client.post(
                    f'{self.url}/rest/v1/mood_logs',
                    json=data,
                    headers=self.headers
                )
                return response.json()
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    
    def get_user_logs(self, user_id, limit=30):
        if not self.url or not self.key:
            return []
        try:
            with httpx.Client() as client:
                response = client.get(
                    f'{self.url}/rest/v1/mood_logs',
                    params={'user_id': f'eq.{user_id}', 'order': 'timestamp.desc', 'limit': limit},
                    headers=self.headers
                )
                return response.json()
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
