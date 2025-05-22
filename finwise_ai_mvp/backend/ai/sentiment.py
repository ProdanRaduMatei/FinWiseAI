from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

from textblob import TextBlob

def analyze_sentiment(headlines):
    scores = []
    for text in headlines:
        score = TextBlob(text).sentiment.polarity
        scores.append(score)
    return sum(scores) / len(scores) if scores else 0
