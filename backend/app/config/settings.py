from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "shopverse_db")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Google OAuth
    google_client_id: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    google_redirect_uri: Optional[str] = os.getenv("GOOGLE_REDIRECT_URI")
    
    # Frontend URL
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # API
    api_v1_str: str = os.getenv("API_V1_STR", "/api/v1")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
