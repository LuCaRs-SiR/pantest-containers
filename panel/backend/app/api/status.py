import requests
from fastapi import APIRouter
from app.config import AI_GATEWAY_URL, TOOL_CONTAINERS
from app.services import containers_status

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("")
def status():
    try:
        response = requests.get(f"{AI_GATEWAY_URL}/health", timeout=5)
        ai_status = response.json()
    except Exception as exc:
        ai_status = {"error": str(exc)}
    return {
        "ai_gateway": ai_status,
        "backend": "ok",
        "containers": containers_status(TOOL_CONTAINERS),
    }
