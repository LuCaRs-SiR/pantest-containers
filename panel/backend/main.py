import os
import requests
from fastapi import FastAPI

app = FastAPI(title="Pantest Panel Backend")

AI_GATEWAY_URL = os.getenv("AI_GATEWAY_URL", "http://ai-gateway:8000")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/status")
def status():
    try:
        r = requests.get(f"{AI_GATEWAY_URL}/health", timeout=5)
        ai_status = r.json()
    except Exception as exc:
        ai_status = {"error": str(exc)}
    return {"ai_gateway": ai_status}
