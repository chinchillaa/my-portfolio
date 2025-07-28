from typing import Any, Dict, Optional


class ChatbotException(Exception):
    """チャットボットの基本例外クラス"""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class RateLimitException(ChatbotException):
    """レート制限例外"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class GeminiAPIException(ChatbotException):
    """Gemini API関連の例外"""
    def __init__(self, message: str = "Gemini API error"):
        super().__init__(message, status_code=503)


class ValidationException(ChatbotException):
    """バリデーション例外"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)


class AuthenticationException(ChatbotException):
    """認証例外"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)