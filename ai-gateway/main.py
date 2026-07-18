import os
import time
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


def _call_ollama_generate(payload: dict, timeout: int = 120, retries: int = 2) -> dict:
    last_exc: requests.RequestException | None = None

    for attempt in range(1, retries + 2):
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=timeout,
            )

            if response.status_code >= 500:
                body = response.text[:400]
                raise requests.HTTPError(
                    f"upstream {response.status_code}: {body}", response=response
                )

            response.raise_for_status()
            return response.json()
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as exc:
            retriable = isinstance(exc, (requests.ConnectionError, requests.Timeout))
            if isinstance(exc, requests.HTTPError) and exc.response is not None:
                retriable = retriable or exc.response.status_code >= 500

            if retriable and attempt <= retries:
                logger.warning(
                    "Retrying Ollama request (%s/%s) after error: %s",
                    attempt,
                    retries,
                    exc,
                )
                time.sleep(0.5 * attempt)
                last_exc = exc
                continue

            raise
        except requests.RequestException as exc:
            last_exc = exc
            raise

    if last_exc:
        raise last_exc

    raise requests.RequestException("unknown upstream error")


@app.on_event("startup")
def warmup_default_model() -> None:
    try:
        _call_ollama_generate(
            {
                "model": DEFAULT_MODEL,
                "prompt": "Warmup",
                "stream": False,
                "keep_alive": "24h",
            },
            timeout=180,
            retries=2,
        )
        logger.info("Default model warmed up: %s", DEFAULT_MODEL)
    except requests.RequestException as exc:
        logger.warning("Warmup failed for %s: %s", DEFAULT_MODEL, exc)


@app.get("/health")
def health():
    return {"status": "ok", "model": DEFAULT_MODEL}


@app.post("/api/generate")
def generate(payload: Prompt):
    outgoing = payload.model_dump()
    outgoing.setdefault("keep_alive", "24h")

    try:
        return _call_ollama_generate(outgoing, timeout=180, retries=2)
    except requests.RequestException as exc:
        logger.error("/api/generate failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc))
