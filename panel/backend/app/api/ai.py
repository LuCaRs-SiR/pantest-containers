from fastapi import APIRouter
from app.schemas import Prompt
from app.services import proxy_ai

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("")
def ai_chat(payload: Prompt):
    return proxy_ai(payload.model_dump())
