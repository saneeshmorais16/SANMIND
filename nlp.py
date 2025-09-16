# backend/services/nlp.py
from typing import Tuple

# ---- Fallback heuristic (always available) ----
EMOTION_KEYWORDS = {
    "joy": ["happy", "glad", "excited", "joy", "delighted"],
    "sadness": ["sad", "down", "depressed", "unhappy", "tears"],
    "anger": ["angry", "mad", "furious", "rage", "annoyed"],
    "fear": ["afraid", "scared", "fear", "terrified", "anxious"],
    "stress": ["stressed", "overwhelmed", "pressure", "burnout", "tired"],
}

def _heuristic_emotion(text: str) -> Tuple[str, float]:
    t = (text or "").lower()
    best_emotion = "neutral"
    best_score = 0
    for emo, words in EMOTION_KEYWORDS.items():
        score = sum(w in t for w in words)
        if score > best_score:
            best_score = score
            best_emotion = emo
    conf = min(0.9, 0.5 + 0.1 * best_score) if best_score > 0 else 0.5
    return best_emotion, conf

# ---- Try to load a real transformer model ----
_PIPELINE = None
_LABEL_MAP = {
    # Map common emotion labels to our set (adjust as you like)
    "joy": "joy",
    "happiness": "joy",
    "sadness": "sadness",
    "anger": "anger",
    "fear": "fear",
    "anxiety": "fear",
    "surprise": "joy",      # simple mapping
    "disgust": "anger",     # simple mapping
    "neutral": "neutral",
}

def _load_pipeline():
    global _PIPELINE
    if _PIPELINE is not None:
        return _PIPELINE
    try:
        from transformers import pipeline
        # Popular small model for emotions (English)
        # Alternatives: "SamLowe/roberta-base-go_emotions"
        model_id = "j-hartmann/emotion-english-distilroberta-base"
        _PIPELINE = pipeline("text-classification", model=model_id, top_k=None)
    except Exception:
        _PIPELINE = None
    return _PIPELINE

def _normalize_label(label: str) -> str:
    lab = (label or "").lower()
    # direct match
    if lab in _LABEL_MAP:
        return _LABEL_MAP[lab]
    # basic fallbacks
    if "joy" in lab or "happy" in lab or "content" in lab:
        return "joy"
    if "sad" in lab or "sorrow" in lab:
        return "sadness"
    if "anger" in lab or "annoy" in lab or "irrit" in lab or "mad" in lab or "rage" in lab:
        return "anger"
    if "fear" in lab or "anx" in lab or "worr" in lab or "stress" in lab:
        return "fear"
    if "neutral" in lab:
        return "neutral"
    return "neutral"

def heuristic_emotion(text: str) -> Tuple[str, float]:
    """
    Public entry used by the router.
    Tries transformer pipeline first; if unavailable/failed, uses heuristic.
    Returns (emotion, confidence[0..1]).
    """
    pipe = _load_pipeline()
    if pipe is None:
        return _heuristic_emotion(text)

    try:
        outs = pipe(text, truncation=True)
        # outs can be a list of dicts OR list-of-list depending on top_k
        # We’ll pick the top label by score.
        if isinstance(outs, list) and len(outs) > 0:
            candidates = outs[0] if isinstance(outs[0], list) else outs
            # Find best candidate
            best = max(candidates, key=lambda d: d.get("score", 0.0))
            emotion = _normalize_label(best.get("label", "neutral"))
            conf = float(best.get("score", 0.6))
            # keep confidence in [0.5, 0.99] range for UI niceness
            conf = max(0.5, min(0.99, conf))
            return emotion, conf
    except Exception:
        pass

    # fallback if anything goes wrong
    return _heuristic_emotion(text)
