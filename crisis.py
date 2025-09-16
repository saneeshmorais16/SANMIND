from typing import Tuple, List

CRISIS_TERMS = [
    "suicide", "kill myself", "end it", "self harm", "hurt myself",
    "no reason to live", "die", "cut myself"
]

def detect_crisis(text: str) -> Tuple[bool, List[str]]:
    t = text.lower()
    matched = [k for k in CRISIS_TERMS if k in t]
    return (len(matched) > 0), matched
