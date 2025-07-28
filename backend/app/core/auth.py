"""
認証関連のユーティリティとミドルウェア
"""
import secrets
from typing import Optional
from fastapi import HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# HTTPBearer認証スキーム
security = HTTPBearer(auto_error=False)


class APIKeyAuth:
    """APIキー認証クラス"""
    
    def __init__(self):
        self.api_key = settings.API_KEY
        
    async def verify_api_key(
        self,
        x_api_key: Optional[str] = Header(None),
        authorization: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> bool:
        """
        APIキーを検証する
        
        Args:
            x_api_key: X-API-Keyヘッダーの値
            authorization: Authorizationヘッダーの値（Bearer token）
            
        Returns:
            bool: 認証成功時True
            
        Raises:
            HTTPException: 認証失敗時
        """
        # X-API-Keyヘッダーをチェック
        if x_api_key:
            if secrets.compare_digest(x_api_key, self.api_key):
                return True
            else:
                logger.warning("Invalid API key in X-API-Key header")
                raise HTTPException(
                    status_code=403,
                    detail="Invalid API Key"
                )
        
        # Authorizationヘッダー（Bearer token）をチェック
        if authorization and authorization.scheme == "Bearer":
            if secrets.compare_digest(authorization.credentials, self.api_key):
                return True
            else:
                logger.warning("Invalid API key in Authorization header")
                raise HTTPException(
                    status_code=403,
                    detail="Invalid API Key"
                )
        
        # どちらのヘッダーも提供されていない場合
        logger.warning("No API key provided in request")
        raise HTTPException(
            status_code=401,
            detail="API Key required. Please provide X-API-Key header or Authorization: Bearer token"
        )


# シングルトンインスタンス
api_key_auth = APIKeyAuth()


def require_api_key(authenticated: bool = Depends(api_key_auth.verify_api_key)) -> bool:
    """
    APIキー認証を要求する依存関係
    
    使用例:
        @router.get("/protected", dependencies=[Depends(require_api_key)])
        async def protected_endpoint():
            return {"message": "This endpoint is protected"}
    """
    return authenticated