import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Load environment settings
load_dotenv()

def get_database_url() -> str:
    """
    Retrieves and formats the database connection URL.
    Prefers ASYNC_DATABASE_URL or DATABASE_URL if configured.
    Falls back to SQLite for local development if PostgreSQL is unavailable.
    """
    url = os.getenv("ASYNC_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not url:
        return "sqlite+aiosqlite:///./ai_architect.db"
    
    # Ensure proper async driver for PostgreSQL
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    return url

DATABASE_URL = get_database_url()
is_sqlite = "sqlite" in DATABASE_URL

engine_args = {"echo": os.getenv("ENVIRONMENT") == "development"}
if is_sqlite:
    engine_args["connect_args"] = {"check_same_thread": False}

async_engine: AsyncEngine = create_async_engine(DATABASE_URL, **engine_args)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency yielding an asynchronous database session.
    Handles commit/rollback automatically.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
