from typing import Dict
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except Exception as e:
    raise RuntimeError('Please run: python -m nltk.downloader vader_lexicon') from e

_analyzer = None

def _get():
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer

def score(text: str) -> Dict[str, float]:
    if not text:
        return {'compound': 0.0, 'neg': 0.0, 'neu': 1.0, 'pos': 0.0}
    return _get().polarity_scores(text)
