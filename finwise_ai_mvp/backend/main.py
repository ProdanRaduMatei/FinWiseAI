
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from ai.sentiment import analyze_sentiment
from db.database import init_db, add_stock, get_portfolio
from utils import get_price, get_news, get_ai_suggestion

app = FastAPI()
init_db()

class StockRequest(BaseModel):
    email: str
    ticker: str

class PortfolioRequest(BaseModel):
    email: str

@app.post("/add_stock")
def add_stock_to_portfolio(req: StockRequest):
    return add_stock(req.email, req.ticker.upper())

@app.post("/get_portfolio")
def get_user_portfolio(req: PortfolioRequest):
    return get_portfolio(req.email)

@app.post("/analyze")
def analyze_portfolio(req: PortfolioRequest):
    portfolio = get_portfolio(req.email)
    insights = []
    for stock in portfolio:
        ticker = stock['ticker']
        price = get_price(ticker)
        headlines = get_news(ticker)
        sentiment = analyze_sentiment(headlines)
        suggestion = get_ai_suggestion(price, sentiment)
        insights.append({
            "ticker": ticker,
            "price": price,
            "sentiment": sentiment,
            "suggestion": suggestion
        })
    return insights
