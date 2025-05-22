def get_price(ticker):
    return 123.45  # Replace with real API later

def get_news(ticker):
    return [
        f"{ticker} earnings beat expectations",
        f"{ticker} shows strong quarterly growth"
    ]

def get_ai_suggestion(price, sentiment):
    if sentiment > 0.5:
        return "Buy"
    elif sentiment < -0.3:
        return "Sell"
    else:
        return "Hold"
