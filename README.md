# SanMind — Starter Kit

SanMind is a multimodal AI mental-health assistant (text + voice) with a FastAPI backend and a simple web frontend.

This starter includes:
- FastAPI backend with endpoints for text prediction, placeholder voice prediction, crisis detection, and suggestions
- Simple static frontend (HTML/CSS/JS) calling the backend
- Basic ethics & safety placeholders
- Requirements and run instructions

## Quickstart

### 1) Backend (FastAPI)
```bash
cd backend
python -m venv .venv
# activate:
#   Windows: .venv\Scripts\activate
#   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### 2) Frontend (static)
Open `frontend/index.html` directly in your browser, or serve it locally (e.g., VS Code Live Server).
Set `API_BASE` in `frontend/app.js` if backend runs on a different host/port.

### Notes
- Text prediction is a **stub** (keyword heuristic + neutral fallback). We'll replace with a DistilBERT model next.
- Voice prediction endpoint is a **placeholder** for future development.
- Crisis detection is rule-based with a small keyword list and semantic TODO.
- This project is NOT a medical device. It is **not** for diagnosis or crisis intervention.
