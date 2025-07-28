from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """チャットメッセージのスキーマ"""
    content: str = Field(..., min_length=1, max_length=2000, description="メッセージ内容")
    role: str = Field(default="user", pattern="^(user|assistant)$", description="メッセージの送信者")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    @field_validator("content")
    def validate_content(cls, v):
        # 危険な文字列のサニタイズ
        v = v.strip()
        if not v:
            raise ValueError("メッセージは空にできません")
        return v


class ChatRequest(BaseModel):
    """チャットリクエストのスキーマ"""
    message: str = Field(..., min_length=1, max_length=2000, description="ユーザーからのメッセージ")
    session_id: Optional[str] = Field(None, max_length=100, description="セッションID")
    context: Optional[List[ChatMessage]] = Field(default_factory=list, description="会話履歴")


class ChatResponse(BaseModel):
    """チャットレスポンスのスキーマ"""
    message: str = Field(..., description="アシスタントからの返答")
    session_id: str = Field(..., description="セッションID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="success")


class HealthCheck(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str = Field(default="healthy")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    environment: str


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)