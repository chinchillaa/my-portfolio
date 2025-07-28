import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field
import json


class Settings(BaseSettings):
    # API設定
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Portfolio Chatbot API"
    VERSION: str = "0.1.0"
    
    # Gemini API設定
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"
    
    # Redis設定
    REDIS_URL: str = "redis://localhost:6379"
    
    # セキュリティ設定
    SECRET_KEY: str
    API_KEY: str  # APIキー認証用
    ALLOWED_ORIGINS: Union[str, List[str]] = Field(default="https://chinchillaa.github.io")
    
    # レート制限
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    
    # 環境設定
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    @field_validator("ALLOWED_ORIGINS", mode='before')
    def parse_allowed_origins(cls, v):
        if v is None:
            return ["https://chinchillaa.github.io"]
        if isinstance(v, str):
            # 空文字列の場合はデフォルト値を返す
            if not v.strip():
                return ["https://chinchillaa.github.io"]
            # JSON配列かどうか確認
            if v.strip().startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # カンマ区切りの文字列として処理
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        if isinstance(v, list):
            return v
        return ["https://chinchillaa.github.io"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # 自動的なJSON解析を無効化
        json_parse_mode = None


settings = Settings()