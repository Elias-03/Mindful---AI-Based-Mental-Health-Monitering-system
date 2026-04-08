from transformers import pipeline
import torch

class EmotionAnalyzer:
    def __init__(self):
        self.model_name = "mental/mental-roberta-base"
        try:
            self.emotion_classifier = pipeline(
                "text-classification",
                model=self.model_name,
                top_k=None
            )
        except:
            self.emotion_classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
    
    def analyze(self, text):
        if not text or len(text.strip()) < 10:
            return {
                'emotions': {},
                'dominant_emotion': 'neutral',
                'sentiment_score': 0.0
            }
        
        results = self.emotion_classifier(text[:512])
        
        emotions = {}
        if isinstance(results[0], list):
            for item in results[0]:
                emotions[item['label']] = item['score']
        else:
            emotions[results[0]['label']] = results[0]['score']
        
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Robust sentiment calculation
        if 'POSITIVE' in emotions or 'NEGATIVE' in emotions:
            sentiment_score = emotions.get('POSITIVE', 0.0) - emotions.get('NEGATIVE', 0.0)
        else:
            # Map mental health emotions to sentiment
            positive_emotions = ['joy', 'love', 'surprise']
            negative_emotions = ['sadness', 'anger', 'fear', 'disgust', 'shame', 'guilt']
            
            pos_score = sum(emotions.get(e, 0.0) for e in positive_emotions)
            neg_score = sum(emotions.get(e, 0.0) for e in negative_emotions)
            sentiment_score = pos_score - neg_score
        
        return {
            'emotions': emotions,
            'dominant_emotion': dominant_emotion,
            'sentiment_score': sentiment_score
        }
