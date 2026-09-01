from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    """
    Centralized configuration manager for SecureVision AI.
    Loads settings from environment variables with safe defaults.
    """
    
    # Application Config
    PROJECT_NAME: str = "SecureVision AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "supersecretkey" # Override in production via .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./securevision.db"
    
    # External APIs
    GEMINI_API_KEY: str = ""
    
    # AI Engine Config
    ISOLATION_FOREST_CONTAMINATION: float = 0.05
    LSTM_SEQUENCE_LENGTH: int = 7
    LSTM_HIDDEN_SIZE: int = 64
    
    # Secure Cookie Settings
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"
    ENABLE_DEMO_LOGIN: bool = True
    DEMO_USER_EMAIL: str = "demo-account@securevision.ai"

    @model_validator(mode="after")
    def validate_security_settings(self):
        if self.ENVIRONMENT.lower() == "production":
            if self.SECRET_KEY == "supersecretkey" or len(self.SECRET_KEY) < 32:
                raise ValueError("A unique SECRET_KEY of at least 32 characters is required in production")
            if not self.COOKIE_SECURE:
                raise ValueError("COOKIE_SECURE must be enabled in production")
            if self.ENABLE_DEMO_LOGIN:
                raise ValueError("ENABLE_DEMO_LOGIN must be disabled in production")
        if self.COOKIE_SAMESITE not in {"lax", "strict", "none"}:
            raise ValueError("COOKIE_SAMESITE must be lax, strict, or none")
        return self
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
