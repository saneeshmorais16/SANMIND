## backend/services/audio.py
from typing import Tuple

def placeholder_predict(raw_bytes: bytes) -> Tuple[str, float]:
    """Temporary stub until we add transcription or a SER model."""
    # You can add simple heuristics by file size/duration later if you want.
    return "neutral", 0.4

