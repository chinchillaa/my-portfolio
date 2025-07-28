import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config import settings


class SecurityService:
    """セキュリティ関連のサービス"""
    
    ALGORITHM = "HS256"
    
    @staticmethod
    def generate_session_id() -> str:
        """セッションIDを生成"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_csrf_token() -> str:
        """CSRFトークンを生成"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_ip(ip_address: str) -> str:
        """IPアドレスをハッシュ化（プライバシー保護）"""
        return hashlib.sha256(f"{ip_address}{settings.SECRET_KEY}".encode()).hexdigest()
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """アクセストークンを作成"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=SecurityService.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """トークンを検証"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[SecurityService.ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """入力をサニタイズ"""
        # 基本的なサニタイゼーション
        dangerous_patterns = ['<script', '</script>', 'javascript:', 'onerror=']
        text_lower = text.lower()
        
        for pattern in dangerous_patterns:
            if pattern in text_lower:
                text = text.replace(pattern, '')
                text = text.replace(pattern.upper(), '')
        
        return text.strip()