from fastapi import APIRouter

from app.schemas import AssistantTaskRequest
from app.services import execute_assistant_task

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("/run")
def run_assistant(payload: AssistantTaskRequest):
    return execute_assistant_task(
        task=payload.task,
        target=payload.target,
        domain=payload.domain,
    )
