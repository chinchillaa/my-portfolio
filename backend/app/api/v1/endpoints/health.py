from fastapi import APIRouter, Depends
from app.config import settings
from app.models import HealthCheck
import redis
from typing import Optional

router = APIRouter()


async def check_redis_connection() -> bool:
    """Redis接続をチェック"""
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        return True
    except Exception:
        return False


@router.get("", response_model=HealthCheck)
async def health_check():
    """
    ヘルスチェックエンドポイント
    
    サービスの状態を確認します。
    """
    # Redis接続チェック
    redis_healthy = await check_redis_connection()
    
    return HealthCheck(
        status="healthy" if redis_healthy else "degraded",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT
    )


@router.get("/ready")
async def readiness_check():
    """
    準備状態チェックエンドポイント
    
    すべての依存サービスが利用可能かチェックします。
    """
    redis_healthy = await check_redis_connection()
    
    # Gemini APIキーの存在確認
    gemini_configured = bool(settings.GEMINI_API_KEY)
    
    all_healthy = redis_healthy and gemini_configured
    
    return {
        "ready": all_healthy,
        "checks": {
            "redis": redis_healthy,
            "gemini_api": gemini_configured
        }
    }