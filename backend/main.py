import logging
import uvicorn
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from database.base import Base
from database.session import async_engine
from routes.auth_routes import router as auth_router

# Setup logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_solution_architect")

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous lifespan manager handling database initialization and teardown cleanup.
    """
    logger.info("Initializing Database Tables Schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database Schema initialization completed.")
    
    yield
    
    logger.info("Disposing active database connection pool...")
    await async_engine.dispose()
    logger.info("Database engine connections terminated.")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Enterprise AI Solution Architect Platform REST API Engine",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS Cross-Origin settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Custom Exception Handling for standard JSON response formatting
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all global exception interceptor returning safe structured JSON error messages.
    """
    logger.error(f"Unhandled Exception occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected server error occurred. Please contact the administrator."
        },
    )

# Include Authentication Routes
app.include_router(auth_router)

@app.get(
    "/api/health",
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="System health status check",
)
async def health_check():
    """
    Returns system status, current environment, and timezone-aware UTC timestamps.
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
