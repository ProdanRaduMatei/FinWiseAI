import requests
import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
sentiment_analyzer = pipeline("sentiment-analysis")

def fetch_stock_price(ticker):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    return response.get("c", 0)  # current price

def fetch_news_sentiment(ticker):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-05-01&to=2025-05-23&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    headlines = [article["headline"] for article in response if "headline" in article][:5]
    if not headlines:
        return "NEUTRAL"
    results = sentiment_analyzer(headlines)
    pos = sum(1 for r in results if r["label"] == "POSITIVE")
    neg = sum(1 for r in results if r["label"] == "NEGATIVE")
    return "POSITIVE" if pos >= neg else "NEGATIVE"

def get_recommendation_for_position(ticker, entry_price):
    current_price = fetch_stock_price(ticker)
    sentiment = fetch_news_sentiment(ticker)

    if current_price > entry_price * 1.1 and sentiment == "POSITIVE":
        return "SELL"
    elif current_price < entry_price * 0.95 or sentiment == "NEGATIVE":
        return "BUY"
    else:
        return "HOLD"