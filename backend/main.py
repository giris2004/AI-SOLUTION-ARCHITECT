import uvicorn
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from database.base import Base
from database.session import async_engine
from routes.auth_routes import router as auth_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup table creation and shutdown cleanup.
    """
    # Create DB tables if they don't exist
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup database connection pool on shutdown
    await async_engine.dispose()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Enterprise AI Solution Architect Platform REST API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routes
app.include_router(auth_router)

@app.get(
    "/api/health",
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="System health status check",
)
async def health_check():
    """
    Returns system operational status, timestamp, and environment configuration.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
