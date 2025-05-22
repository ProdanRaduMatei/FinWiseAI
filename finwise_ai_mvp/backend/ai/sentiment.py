from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(headlines):
    results = sentiment_pipeline(headlines)
    scores = [1 if r['label'] == 'positive' else -1 if r['label'] == 'negative' else 0 for r in results]
    return sum(scores) / len(scores) if scores else 0
