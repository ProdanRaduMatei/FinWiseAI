from fastapi import APIRouter
from utils.t212_api import fetch_open_positions
from utils.finnhub_data import (
    get_current_price,
    get_sentiment_score,
    get_technical_indicators
)
from utils.hybrid_ai import hybrid_predict
from utils.rule_logic import rule_based_decision

router = APIRouter()

@router.get("/portfolio")
def get_portfolio_decisions():
    raw_positions = fetch_open_positions()
    results = []

    for pos in raw_positions:
        ticker = pos.get("ticker")
        entry_price = float(pos.get("averagePrice"))
        quantity = float(pos.get("quantity"))

        current_price = get_current_price(ticker)
        sentiment_score = get_sentiment_score(ticker)
        rsi, macd = get_technical_indicators(ticker)

        price_change = (current_price - entry_price) / entry_price
        sentiment = "POSITIVE" if sentiment_score > 0.2 else "NEGATIVE" if sentiment_score < -0.2 else "NEUTRAL"

        features = {
            "rsi": rsi,
            "macd": macd,
            "price_change": price_change,
            "sentiment_score": sentiment_score,
            "pe_ratio": 20  # default placeholder
        }

        ml_decision = hybrid_predict(features)
        rule_decision = rule_based_decision(current_price, entry_price, sentiment)

        if ml_decision == rule_decision:
            final = ml_decision
        elif ml_decision in ["BUY", "SELL"] and rule_decision == "HOLD":
            final = ml_decision
        else:
            final = "HOLD"

        results.append({
            "ticker": ticker,
            "avg_price": entry_price,
            "quantity": quantity,
            "current_price": current_price,
            "rsi": rsi,
            "macd": macd,
            "sentiment_score": sentiment_score,
            "ml_decision": ml_decision,
            "rule_decision": rule_decision,
            "final_decision": final
        })

    return results