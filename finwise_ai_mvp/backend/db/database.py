import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

PORTFOLIO_URL = f"{SUPABASE_URL}/rest/v1/portfolio"

def init_db():
    pass  # No need to manually create tables with Supabase hosted schema

def add_stock(email, ticker):
    payload = {"email": email, "ticker": ticker}
    res = requests.post(PORTFOLIO_URL, headers=HEADERS, json=payload)
    if res.status_code != 201:
        raise Exception(f"Failed to add stock: {res.text}")
    return {"status": "added", "ticker": ticker}

def get_portfolio(email):
    params = {"email": f"eq.{email}"}
    res = requests.get(PORTFOLIO_URL, headers=HEADERS, params=params)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch portfolio: {res.text}")
    return res.json()
