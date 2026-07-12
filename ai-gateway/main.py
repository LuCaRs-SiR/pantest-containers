import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Gateway")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


class Prompt(BaseModel):
    model: str = "llama2"
    prompt: str
    stream: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


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
