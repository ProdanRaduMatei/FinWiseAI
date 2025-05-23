import os
import requests
import yfinance as yf
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Setup FinBERT
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def get_current_price(ticker):
    ticker = clean_ticker(ticker)
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
        response = requests.get(url).json()
        return float(response.get("c", 0))
    except:
        return 0.0

def get_sentiment_score(ticker):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-05-01&to=2025-05-23&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    headlines = [article["headline"] for article in response if "headline" in article][:5]
    if not headlines:
        return 0.0  # neutral
    results = finbert(headlines)
    score = sum((1 if r["label"].lower() == "positive" else -1 if r["label"].lower() == "negative" else 0) for r in results)
    return score / len(results)

def clean_ticker(ticker):
    return ticker.split("_")[0]

def get_technical_indicators(ticker):
    ticker = clean_ticker(ticker)
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if len(data) < 15:
            return 50.0, 0.0  # default fallback
        delta = data["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean().iloc[-1]
        avg_loss = loss.rolling(window=14).mean().iloc[-1]
        rs = avg_gain / avg_loss if avg_loss != 0 else 1
        rsi = 100 - (100 / (1 + rs))
        data["EMA12"] = data["Close"].ewm(span=12, adjust=False).mean()
        data["EMA26"] = data["Close"].ewm(span=26, adjust=False).mean()
        macd = data["EMA12"].iloc[-1] - data["EMA26"].iloc[-1]
        return round(rsi, 2), round(macd, 2)
    except Exception as e:
        print(f"[!] Failed to fetch indicators for {ticker}: {e}")
        return 50.0, 0.0