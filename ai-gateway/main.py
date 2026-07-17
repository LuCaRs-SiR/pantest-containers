import os
import logging
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Gateway")
logger = logging.getLogger("ai-gateway")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")


class Prompt(BaseModel):
    model: str = DEFAULT_MODEL
    prompt: str
    stream: bool = False


@app.on_event("startup")
def warmup_default_model() -> None:
    try:
        requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": DEFAULT_MODEL,
                "prompt": "Warmup",
                "stream": False,
                "keep_alive": "24h",
            },
            timeout=180,
        ).raise_for_status()
        logger.info("Default model warmed up: %s", DEFAULT_MODEL)
    except requests.RequestException as exc:
        logger.warning("Warmup failed for %s: %s", DEFAULT_MODEL, exc)


@app.get("/health")
def health():
    return {"status": "ok", "model": DEFAULT_MODEL}


@app.post("/api/generate")
def generate(payload: Prompt):
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload.model_dump(),
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))
