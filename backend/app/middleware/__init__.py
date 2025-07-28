from fastapi import FastAPI
from .cors import setup_cors
from .security import SecurityMiddleware
from .rate_limit import RateLimitMiddleware
import logging

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """
    すべてのミドルウェアを設定
    
    Args:
        app: FastAPIアプリケーションインスタンス
    """
    # セキュリティヘッダー
    app.add_middleware(SecurityMiddleware)
    
    # レート制限
    app.add_middleware(RateLimitMiddleware)
    
    logger.info("All middleware configured successfully")