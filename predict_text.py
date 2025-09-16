from fastapi import APIRouter
from pydantic import BaseModel
from backend.services import nlp, crisis, suggestions

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/text")
def predict_text(req: TextRequest):
    text = req.text or ""
    crisis_flag, matched = crisis.detect_crisis(text)
    emotion, conf = nlp.heuristic_emotion(text)
    reply = suggestions.suggest(emotion, crisis_flag)
    return {
        "emotion": emotion,
        "confidence": conf,
        "crisis": crisis_flag,
        "crisis_terms": matched,
        "reply": reply
    }
