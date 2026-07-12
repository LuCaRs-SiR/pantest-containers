import requests
from fastapi import HTTPException
from app.config import AI_GATEWAY_URL


def proxy_ai(payload: dict) -> dict:
    try:
        response = requests.post(
            f"{AI_GATEWAY_URL}/api/generate",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc))
