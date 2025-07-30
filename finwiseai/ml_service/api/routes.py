from fastapi import APIRouter, HTTPException
from finwiseai.ml_service.models.lstm_model import LSTMStockModel
import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
from finwiseai.ml_service.sentiment.finbert_sentiment import batch_analyze_sentiment
from finwiseai.ml_service.sentiment.news_fetcher import fetch_stock_news
from finwiseai.ml_service.sentiment.vader_sentiment import analyze_sentiment_vader

# Define router ONCE with prefix /ml
router = APIRouter(prefix="/ml", tags=["LSTM"])

@router.get("/predict")
def predict_next_close(csv_path: str = "sample_ohlcv_stock_data.csv"):
    if not os.path.exists("lstm_model.pth"):
        raise HTTPException(status_code=404, detail="Model not trained. Run training first.")

    df = pd.read_csv(csv_path)
    data = df[['Open', 'High', 'Low', 'Close', 'Volume']].values

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    last_seq = torch.tensor([scaled_data[-50:]], dtype=torch.float32)

    model = LSTMStockModel()
    model.load_state_dict(torch.load("lstm_model.pth"))
    model.eval()

    with torch.no_grad():
        pred = model(last_seq).item()

    close_index = 3  # 'Close'
    close_max = scaler.data_max_[close_index]
    close_min = scaler.data_min_[close_index]
    predicted_close = pred * (close_max - close_min) + close_min

    return {"predicted_close_price": round(predicted_close, 2)}

@router.get("/sentiment/finbert/{symbol}")
def sentiment_analysis(symbol: str):
    # Fetch news
    articles = fetch_stock_news(symbol)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this symbol")

    # Combine titles and descriptions for sentiment analysis
    texts = [f"{a['title']} {a['description'] or ''}" for a in articles]
    sentiments = batch_analyze_sentiment(tuple(texts))

    # Aggregate sentiment counts
    summary = {"positive": 0, "negative": 0, "neutral": 0}
    for s in sentiments:
        summary[s["label"]] += 1

    return {
        "symbol": symbol,
        "summary": summary,
        "articles": [
            {**article, "sentiment": sentiments[i]} for i, article in enumerate(articles)
        ],
    }


vader_router = APIRouter(prefix="/ml", tags=["VADER"])

@vader_router.get("/sentiment/vader/{symbol}")
def sentiment_analysis_vader(symbol: str):
    # Fetch news
    articles = fetch_stock_news(symbol)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this symbol")

    # Prepare text
    texts = [f"{a['title']} {a['description'] or ''}" for a in articles]

    # Analyze sentiment using VADER
    scores = analyze_sentiment_vader(texts)

    # Convert VADER scores to labels
    sentiments = []
    for s in scores:
        compound = s["compound"]
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        sentiments.append({"label": label})

    # Aggregate sentiment counts
    summary = {"positive": 0, "negative": 0, "neutral": 0}
    for s in sentiments:
        summary[s["label"]] += 1

    return {
        "symbol": symbol,
        "summary": summary,
        "articles": [
            {**article, "sentiment": sentiments[i]} for i, article in enumerate(articles)
        ],
    }