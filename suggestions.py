from typing import Optional

TEMPLATES = {
    "neutral": "I'm here with you. Would you like to talk about what's on your mind today?",
    "joy": "That's lovely to hear. Savor the moment — what made you feel this way?",
    "sadness": "I'm sorry you're feeling low. A short walk, journaling, or talking to someone you trust might help.",
    "anger": "That sounds frustrating. Try a brief pause: slow breaths in for 4 seconds, out for 6.",
    "fear": "Feeling scared is valid. Ground yourself by naming 5 things you can see, 4 you can touch, 3 you can hear.",
    "stress": "Stress can pile up. Consider a 5-minute break, a glass of water, and listing your top 3 priorities.",
}

CRISIS_NOTICE = (
    "I’m concerned by what you shared. I can’t provide crisis support, "
    "but you’re not alone. If you’re in immediate danger, please contact emergency services. "
    "You can also reach out to local crisis helplines."
)

def suggest(emotion: str, crisis: bool) -> str:
    if crisis:
        return CRISIS_NOTICE
    return TEMPLATES.get(emotion, TEMPLATES["neutral"])
