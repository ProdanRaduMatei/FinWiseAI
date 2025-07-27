from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(texts):
    """
    Analyze sentiment of given texts using VADER.
    Returns list of dicts: [{'label': 'positive/negative/neutral', 'score': float}]
    """
    results = []
    for text in texts:
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05:
            label = 'positive'
        elif compound <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        results.append({'label': label, 'score': compound})
    return results