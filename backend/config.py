import os
import json
from functools import lru_cache
from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Pydantic settings manager for loading application configs from .env file and environment.
    """
    APP_NAME: str = "AI Solution Architect API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # CORS Origins (accepts JSON array string or list)
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]

    # Security & Auth
    SECRET_KEY: str = "change_this_to_a_secure_32_byte_hex_string_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Database URLs
    DATABASE_URL: str = "sqlite:///./ai_architect.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./ai_architect.db"

    # Gemini AI API Settings
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API Key")
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Storage & PDF Settings
    PDF_OUTPUT_DIR: str = "./reports/storage"

    # Pydantic v2 specific settings config
    @classmethod
    def get_env_path(cls) -> str:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, "..", ".env"))

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_cors_origins_list(self) -> List[str]:
        """
        Parses CORS_ORIGINS list safely if provided as a JSON string.
        """
        if isinstance(self.CORS_ORIGINS, str):
            try:
                return json.loads(self.CORS_ORIGINS)
            except Exception:
                return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached Settings instance to prevent redundant file I/O operations.
    """
    return Settings()
