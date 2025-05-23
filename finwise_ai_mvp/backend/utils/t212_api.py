import requests
import os
from dotenv import load_dotenv

load_dotenv()

T212_API_KEY = os.getenv("T212_API_KEY")
BASE_URL = "https://demo.trading212.com/api/v0"

def get_headers():
    return {
        "Authorization": T212_API_KEY,         # should be "Bearer abcd123..."
        "User-Agent": "FinWiseAI/1.0"
    }

def fetch_open_positions():
    url = f"{BASE_URL}/equity/portfolio"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()