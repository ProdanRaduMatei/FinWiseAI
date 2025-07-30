from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import functools

# Load FinBERT model and tokenizer globally (cached in memory)
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
model.eval()

# Labels: 0 = neutral, 1 = positive, 2 = negative (FinBERT's ordering)
label_map = {0: "neutral", 1: "positive", 2: "negative"}

@functools.lru_cache(maxsize=256)
def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of a single text string using FinBERT with caching."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)[0]

    sentiment_scores = {label_map[i]: float(scores[i]) for i in range(len(scores))}
    sentiment_label = max(sentiment_scores, key=sentiment_scores.get)
    return {"label": sentiment_label, "scores": sentiment_scores}

def batch_analyze_sentiment(texts: list[str]) -> list[dict]:
    """Analyze multiple texts and return list of results."""
    results = []
    for text in texts:
        results.append(analyze_sentiment(text))
    return results