# ─────────────────────────────────────────────────────────────
# app/predictor.py
# The BRAIN of the web app.
# Loads the trained model once when the server starts,
# then uses it to analyse any text sent by the user.
# ─────────────────────────────────────────────────────────────

import re
import joblib
import os
import numpy as np

# ── File paths (same as config.py) ────────────────────────────
MODEL_FILE      = os.path.join('model', 'saved', 'classifier.pkl')
VECTORIZER_FILE = os.path.join('model', 'saved', 'vectorizer.pkl')

# ── Load model once at import time ────────────────────────────
# Loading from disk is slow (~0.5s). We do it ONCE when the server
# starts, not on every request. This keeps responses fast.
try:
    _model      = joblib.load(MODEL_FILE)
    _vectorizer = joblib.load(VECTORIZER_FILE)
    print(f'✅ Model loaded from {MODEL_FILE}')
except FileNotFoundError:
    _model      = None
    _vectorizer = None
    print('⚠️  Model files not found. Run: python model/train.py first.')


# ── Stop words (same set used during training) ────────────────
_STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
    'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
    'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'shall',
    'this', 'that', 'these', 'those', 'it', 'its', 'as', 'not',
    'he', 'she', 'they', 'we', 'i', 'you', 'his', 'her', 'their',
    'our', 'my', 'your', 'said', 'also', 'just', 'about', 'up',
    'out', 'into', 'than', 'then', 'when', 'which', 'who', 'what',
    'all', 'more', 'no', 'so', 'if', 'after', 'before', 'over',
    'new', 'one', 'two', 'can', 'get', 'has', 'us', 'him', 'them'
}


def _clean(text: str) -> str:
    """Apply the same cleaning steps used during training."""
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\([^)]*\)\s*-\s*', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = [w for w in text.split() if w not in _STOP_WORDS]
    return ' '.join(words)


def predict(text: str) -> dict:
    """
    Analyse a piece of text and return a prediction.

    Parameters
    ----------
    text : str  — the raw article or message from the user

    Returns
    -------
    dict with keys:
      label      : "FAKE" or "REAL"
      confidence : float 0–100  (how sure the model is)
      fake_prob  : float 0–100  (probability it is FAKE)
      real_prob  : float 0–100  (probability it is REAL)
      error      : str or None  (set if something went wrong)
    """
    # Guard: model not loaded
    if _model is None or _vectorizer is None:
        return {
            'label': None, 'confidence': 0,
            'fake_prob': 0, 'real_prob': 0,
            'error': 'Model not loaded. Run python model/train.py first.'
        }

    # Guard: empty input
    text = text.strip() if text else ''
    if not text:
        return {
            'label': None, 'confidence': 0,
            'fake_prob': 0, 'real_prob': 0,
            'error': 'Please enter some text.'
        }

    # Guard: input too short to be meaningful
    if len(text.split()) < 5:
        return {
            'label': None, 'confidence': 0,
            'fake_prob': 0, 'real_prob': 0,
            'error': 'Text is too short. Please paste at least a sentence or two.'
        }

    # Clean → vectorize → predict
    clean   = _clean(text)
    vec     = _vectorizer.transform([clean])
    pred    = _model.predict(vec)[0]          # 0=REAL, 1=FAKE

    # PassiveAggressiveClassifier has no predict_proba (it's not a
    # probabilistic model) — it only gives decision_function, which is
    # the signed distance from the decision boundary: positive means
    # "leaning FAKE", negative means "leaning REAL", and bigger magnitude
    # means more confident. We squash that distance into a 0-1 range
    # with a sigmoid so we can still show a friendly confidence percentage.
    score     = _model.decision_function(vec)[0]
    fake_prob_raw = 1 / (1 + np.exp(-score))

    real_prob = round((1 - fake_prob_raw) * 100, 1)
    fake_prob = round(fake_prob_raw * 100, 1)
    label     = 'FAKE' if pred == 1 else 'REAL'
    confidence = fake_prob if pred == 1 else real_prob

    return {
        'label':      label,
        'confidence': round(confidence, 1),
        'fake_prob':  fake_prob,
        'real_prob':  real_prob,
        'error':      None
    }
