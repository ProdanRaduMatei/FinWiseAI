import sqlite3
from datetime import datetime

DB_FILE = "portfolio.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                      ticker TEXT,
                                                      entry_price REAL,
                                                      quantity INTEGER,
                                                      recommendation TEXT,
                                                      sentiment TEXT,
                                                      added_at TEXT
                )
                """)
    conn.commit()
    conn.close()

def add_stock_to_db(ticker, entry_price, quantity, recommendation, sentiment):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO stocks (ticker, entry_price, quantity, recommendation, sentiment, added_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (ticker, entry_price, quantity, recommendation, sentiment, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return {
        "ticker": ticker,
        "entry_price": entry_price,
        "quantity": quantity,
        "recommendation": recommendation,
        "sentiment": sentiment
    }

def get_portfolio():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT ticker, entry_price, quantity, recommendation, sentiment, added_at FROM stocks")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "ticker": r[0],
            "entry_price": r[1],
            "quantity": r[2],
            "recommendation": r[3],
            "sentiment": r[4],
            "added_at": r[5]
        }
        for r in rows
    ]

init_db()