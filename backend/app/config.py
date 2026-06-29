from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
        # Automatically loads from .env file without needing load_dotenv()
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    app_name: str = "Document Chatbot"
    openai_api_key: str = ""
    supabase_url: str = ""
    supabase_key: str = ""

settings = Settings()