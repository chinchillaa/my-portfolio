from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.services import RateLimiter
from app.core import SecurityService, RateLimitException
from app.api.v1.dependencies import get_client_ip
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """レート制限を適用するミドルウェア"""
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limiter = RateLimiter()
        self.security_service = SecurityService()
    
    async def dispatch(self, request: Request, call_next):
        # ヘルスチェックエンドポイントはレート制限から除外
        if request.url.path in ["/health", "/api/v1/health", "/"]:
            return await call_next(request)
        
        try:
            # クライアントIPを取得
            client_ip = get_client_ip(request)
            hashed_ip = self.security_service.hash_ip(client_ip)
            
            # レート制限チェック
            await self.rate_limiter.check_rate_limit(hashed_ip)
            
            # クォータ情報を取得
            quota = await self.rate_limiter.get_remaining_quota(hashed_ip)
            
            # リクエストを処理
            response = await call_next(request)
            
            # レート制限ヘッダーを追加
            response.headers["X-RateLimit-Limit"] = str(quota["minute"]["limit"])
            response.headers["X-RateLimit-Remaining"] = str(quota["minute"]["remaining"])
            response.headers["X-RateLimit-Reset"] = quota["minute"]["reset_at"]
            
            return response
            
        except RateLimitException as e:
            logger.warning(f"Rate limit exceeded for IP: {hashed_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "detail": str(e)
                },
                headers={
                    "Retry-After": "60"
                }
            )
        except Exception as e:
            logger.error(f"Rate limit middleware error: {str(e)}")
            # エラーの場合はリクエストを通す（可用性を優先）
            return await call_next(request)