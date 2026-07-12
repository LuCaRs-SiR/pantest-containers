from .health import router as health_router
from .status import router as status_router
from .ai import router as ai_router
from .tools import router as tools_router

__all__ = ["health_router", "status_router", "ai_router", "tools_router"]
