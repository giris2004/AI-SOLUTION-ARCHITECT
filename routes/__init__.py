from routes.auth_routes import router as auth_router
from routes.project_routes import router as project_router
from routes.ai_routes import router as ai_router

__all__ = [
    "auth_router",
    "project_router",
    "ai_router",
]
