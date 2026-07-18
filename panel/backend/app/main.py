from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    health_router,
    status_router,
    ai_router,
    tools_router,
    assistant_router,
)

app = FastAPI(title="Pantest Panel Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(status_router)
app.include_router(ai_router)
app.include_router(tools_router)
app.include_router(assistant_router)
