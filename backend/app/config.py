# backend/app/config.py
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Single source of truth for environment variables.
    Fails fast on startup if required config is missing (no silent fallbacks).
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- App Settings ---
    APP_NAME: str = "Document Copilot"
    # Comma-separated list of allowed origins for CORS (e.g., "http://localhost:5173,http://localhost:3000")
    # ALLOWED_ORIGINS: str = "http://localhost:5173"
    ALLOWED_ORIGINS: str = "http://localhost:5173,https://your-frontend-url.vercel.app"

    # --- Supabase Settings ---
    SUPABASE_URL: str = Field(..., description="Supabase project URL")
    SUPABASE_ANON_KEY: str = Field(..., description="Supabase anonymous key")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(..., description="Supabase service role key")
    DATABASE_URL: PostgresDsn = Field(..., description="Direct Postgres connection string for SQLAlchemy/Alembic")

    # --- LLM Settings (Using Gemini instead of OpenAI) ---
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API key")
    GEMINI_EMBEDDING_MODEL: str = Field(...)
    GEMINI_EMBEDDING_DIMENSIONS: int = Field(...)

# Instantiating this will raise a ValidationError if any required fields are missing from .env
settings = Settings()