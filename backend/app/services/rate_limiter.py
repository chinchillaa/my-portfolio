import redis
from datetime import datetime, timedelta
from typing import Optional
import logging
from app.config import settings
from app.core.exceptions import RateLimitException

logger = logging.getLogger(__name__)


class RateLimiter:
    """レート制限サービス"""
    
    def __init__(self):
        """サービスの初期化"""
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.rate_limit_per_minute = settings.RATE_LIMIT_PER_MINUTE
        self.rate_limit_per_hour = settings.RATE_LIMIT_PER_HOUR
    
    async def check_rate_limit(self, identifier: str) -> bool:
        """
        レート制限をチェック
        
        Args:
            identifier: ユーザー識別子（IPアドレスのハッシュなど）
            
        Returns:
            制限内であればTrue
            
        Raises:
            RateLimitException: レート制限を超えた場合
        """
        try:
            now = datetime.utcnow()
            
            # 分単位のチェック
            minute_key = f"rate_limit:minute:{identifier}:{now.strftime('%Y%m%d%H%M')}"
            minute_count = self.redis_client.incr(minute_key)
            if minute_count == 1:
                self.redis_client.expire(minute_key, 60)
            
            if minute_count > self.rate_limit_per_minute:
                raise RateLimitException(
                    f"Rate limit exceeded: {self.rate_limit_per_minute} requests per minute"
                )
            
            # 時間単位のチェック
            hour_key = f"rate_limit:hour:{identifier}:{now.strftime('%Y%m%d%H')}"
            hour_count = self.redis_client.incr(hour_key)
            if hour_count == 1:
                self.redis_client.expire(hour_key, 3600)
            
            if hour_count > self.rate_limit_per_hour:
                raise RateLimitException(
                    f"Rate limit exceeded: {self.rate_limit_per_hour} requests per hour"
                )
            
            return True
            
        except redis.RedisError as e:
            logger.error(f"Redis error in rate limiter: {str(e)}")
            # Redisエラーの場合はレート制限をスキップ（サービスの可用性を優先）
            return True
    
    async def get_remaining_quota(self, identifier: str) -> dict:
        """
        残りのクォータを取得
        
        Args:
            identifier: ユーザー識別子
            
        Returns:
            残りのリクエスト数
        """
        try:
            now = datetime.utcnow()
            
            # 現在のカウントを取得
            minute_key = f"rate_limit:minute:{identifier}:{now.strftime('%Y%m%d%H%M')}"
            hour_key = f"rate_limit:hour:{identifier}:{now.strftime('%Y%m%d%H')}"
            
            minute_count = int(self.redis_client.get(minute_key) or 0)
            hour_count = int(self.redis_client.get(hour_key) or 0)
            
            return {
                "minute": {
                    "limit": self.rate_limit_per_minute,
                    "remaining": max(0, self.rate_limit_per_minute - minute_count),
                    "reset_at": (now + timedelta(minutes=1)).isoformat()
                },
                "hour": {
                    "limit": self.rate_limit_per_hour,
                    "remaining": max(0, self.rate_limit_per_hour - hour_count),
                    "reset_at": (now + timedelta(hours=1)).isoformat()
                }
            }
            
        except redis.RedisError as e:
            logger.error(f"Redis error getting quota: {str(e)}")
            return {
                "minute": {"limit": self.rate_limit_per_minute, "remaining": -1},
                "hour": {"limit": self.rate_limit_per_hour, "remaining": -1}
            }