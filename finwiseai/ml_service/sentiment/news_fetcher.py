import os
import requests
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()  # This loads the .env variables

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@lru_cache(maxsize=128)
def fetch_stock_news(symbol: str, page_size: int = 5):
    """Fetch latest stock-related news for a given symbol using NewsAPI."""

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("NewsAPI error:", response.text)
        return []

    articles = response.json().get("articles", [])
    return [
        {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt"),
        }
        for a in articles
    ]