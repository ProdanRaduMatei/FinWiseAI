import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from finwiseai.ml_service.api.main import app

client = TestClient(app)


# Mock articles returned by fetch_stock_news
MOCK_ARTICLES = [
    {"title": "Apple launches new iPhone", "description": "Great reception from users"},
    {"title": "Apple faces lawsuit", "description": "Investors are concerned about potential losses"},
]


@pytest.fixture
def mock_news_fetcher():
    with patch("finwiseai.ml_service.api.routes.fetch_stock_news", return_value=MOCK_ARTICLES):
        yield


@pytest.fixture
def mock_finbert_sentiment():
    sentiments = [
        {"label": "positive", "score": 0.95},
        {"label": "negative", "score": 0.80},
    ]
    with patch("finwiseai.ml_service.api.routes.batch_analyze_sentiment", return_value=sentiments):
        yield


@pytest.fixture
def mock_vader_sentiment():
    scores = [
        {"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.8},
        {"neg": 0.6, "neu": 0.3, "pos": 0.1, "compound": -0.7},
    ]
    with patch("finwiseai.ml_service.api.routes.analyze_sentiment_vader", return_value=scores):
        yield


def test_finbert_sentiment_analysis(mock_news_fetcher, mock_finbert_sentiment):
    response = client.get("/ml/sentiment/finbert/AAPL")
    assert response.status_code == 200
    data = response.json()

    assert data["symbol"] == "AAPL"
    assert "summary" in data
    assert "articles" in data
    assert data["summary"]["positive"] == 1
    assert data["summary"]["negative"] == 1
    assert data["summary"]["neutral"] == 0
    assert len(data["articles"]) == 2


def test_vader_sentiment_analysis(mock_news_fetcher, mock_vader_sentiment):
    response = client.get("/ml/sentiment/vader/AAPL")
    assert response.status_code == 200
    data = response.json()

    assert data["symbol"] == "AAPL"
    assert "summary" in data
    assert "articles" in data
    assert data["summary"]["positive"] == 1
    assert data["summary"]["negative"] == 1
    assert data["summary"]["neutral"] == 0
    assert len(data["articles"]) == 2