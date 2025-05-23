from fastapi import APIRouter
from pydantic import BaseModel
from utils.hybrid_ai import hybrid_predict
from utils.rule_logic import rule_based_decision

router = APIRouter()

class StockInput(BaseModel):
    current_price: float
    entry_price: float
    rsi: float
    macd: float
    price_change: float
    sentiment_score: float
    pe_ratio: float
    sentiment: str

@router.post("/predict")
def get_decision(stock: StockInput):
    ml_decision = hybrid_predict(stock.dict())
    rule_decision = rule_based_decision(stock.current_price, stock.entry_price, stock.sentiment)

    if ml_decision == rule_decision:
        final = ml_decision
    elif ml_decision == "BUY" and rule_decision == "HOLD":
        final = "BUY"
    elif ml_decision == "SELL" and rule_decision == "HOLD":
        final = "SELL"
    else:
        final = "HOLD"

    return {
        "ml_decision": ml_decision,
        "rule_decision": rule_decision,
        "final_decision": final
    }