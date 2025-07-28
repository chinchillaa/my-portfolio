import redis
from datetime import datetime, timedelta
from typing import Optional
import logging
from app.config import settings
from app.core.exceptions import RateLimitException
from app.services.fallback_rate_limiter import InMemoryRateLimiter

logger = logging.getLogger(__name__)


class RateLimiter:
    """レート制限サービス（Redisとフォールバック機構付き）"""
    
    def __init__(self):
        """サービスの初期化"""
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            # Redis接続テスト
            self.redis_client.ping()
            self.redis_available = True
            logger.info("Redis connection established for rate limiting")
        except redis.RedisError as e:
            logger.error(f"Redis connection failed: {str(e)}")
            self.redis_available = False
            self.redis_client = None
        
        self.rate_limit_per_minute = settings.RATE_LIMIT_PER_MINUTE
        self.rate_limit_per_hour = settings.RATE_LIMIT_PER_HOUR
        
        # フォールバック用のインメモリレート制限（より厳しい制限）
        self.fallback_limiter = InMemoryRateLimiter(
            rate_limit_per_minute=max(5, self.rate_limit_per_minute // 2),  # 半分の制限
            rate_limit_per_hour=max(50, self.rate_limit_per_hour // 2)
        )
        
        # Redis復旧チェック用のカウンター
        self.redis_check_counter = 0
        self.redis_check_interval = 100  # 100リクエストごとにRedis復旧をチェック
    
    def _try_redis_recovery(self):
        """定期的にRedis復旧を試みる"""
        self.redis_check_counter += 1
        if self.redis_check_counter >= self.redis_check_interval:
            self.redis_check_counter = 0
            try:
                if self.redis_client:
                    self.redis_client.ping()
                    self.redis_available = True
                    logger.info("Redis connection recovered")
            except redis.RedisError:
                self.redis_available = False

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
        # Redisが利用可能か確認
        if self.redis_available and self.redis_client:
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
                self.redis_available = False
                # Redisエラーの場合はフォールバックに切り替え
        
        # Redisが利用不可の場合はフォールバックを使用
        if not self.redis_available:
            # 定期的にRedis復旧を試みる
            self._try_redis_recovery()
            
            # インメモリレート制限を使用
            allowed, error_message = self.fallback_limiter.check_rate_limit(identifier)
            if not allowed:
                logger.warning(f"Rate limit exceeded (fallback): {identifier}")
                raise RateLimitException(error_message)
            
            return True
        
        # デフォルトで拒否（セキュリティファースト）
        logger.error("No rate limiter available, rejecting request")
        raise RateLimitException("Rate limiting service unavailable")
    
    async def get_remaining_quota(self, identifier: str) -> dict:
        """
        残りのクォータを取得
        
        Args:
            identifier: ユーザー識別子
            
        Returns:
            残りのリクエスト数
        """
        # Redisが利用可能な場合
        if self.redis_available and self.redis_client:
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
                    },
                    "backend": "redis"
                }
                
            except redis.RedisError as e:
                logger.error(f"Redis error getting quota: {str(e)}")
                self.redis_available = False
        
        # Redisが利用不可の場合はフォールバックを使用
        return self.fallback_limiter.get_remaining_quota(identifier)