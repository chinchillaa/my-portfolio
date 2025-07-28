import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    # API設定
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Portfolio Chatbot API"
    VERSION: str = "0.1.0"
    
    # Gemini API設定
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"
    
    # Redis設定
    REDIS_URL: str = "redis://localhost:6379"
    
    # セキュリティ設定
    SECRET_KEY: str
    ALLOWED_ORIGINS: List[str] = ["https://chinchillaa.github.io"]
    
    # レート制限
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    
    # 環境設定
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    @field_validator("ALLOWED_ORIGINS", mode='before')
    def parse_allowed_origins(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            # 空文字列の場合は空リストを返す
            if not v.strip():
                return []
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()