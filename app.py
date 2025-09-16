from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import health, predict_text, predict_voice

app = FastAPI(title="SanMind API", version="0.1.0")

# CORS for local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(predict_text.router, prefix="/predict", tags=["predict"])
app.include_router(predict_voice.router, prefix="/predict", tags=["predict"])
