def rule_based_decision(current_price, entry_price, sentiment):
    price_diff = (current_price - entry_price) / entry_price
    if price_diff > 0.1 and sentiment == "POSITIVE":
        return "SELL"
    elif price_diff < -0.05 or sentiment == "NEGATIVE":
        return "BUY"
    return "HOLD"