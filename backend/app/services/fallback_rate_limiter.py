"""
インメモリレート制限の実装
Redisがダウンした場合のフォールバック機構
"""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import threading
import logging

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """
    インメモリでのレート制限実装
    Redisが利用できない場合のフォールバック
    """
    
    def __init__(self, rate_limit_per_minute: int = 5, rate_limit_per_hour: int = 50):
        """
        初期化
        
        Args:
            rate_limit_per_minute: 分あたりのリクエスト制限（デフォルトはより厳しい制限）
            rate_limit_per_hour: 時間あたりのリクエスト制限
        """
        # より厳しい制限を設定（Redisダウン時はより慎重に）
        self.rate_limit_per_minute = rate_limit_per_minute
        self.rate_limit_per_hour = rate_limit_per_hour
        
        # リクエスト履歴を保存
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        
        # スレッドセーフティのためのロック
        self.lock = threading.Lock()
        
        # 最後のクリーンアップ時刻
        self.last_cleanup = datetime.utcnow()
        
        logger.warning(
            f"Using in-memory rate limiter with reduced limits: "
            f"{rate_limit_per_minute}/min, {rate_limit_per_hour}/hour"
        )
    
    def _cleanup_old_requests(self, identifier: str, now: datetime):
        """古いリクエスト記録を削除"""
        cutoff_time = now - timedelta(hours=1, minutes=5)  # 1時間5分以上前のデータを削除
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff_time
        ]
    
    def _periodic_cleanup(self):
        """定期的な全体クリーンアップ"""
        now = datetime.utcnow()
        if now - self.last_cleanup > timedelta(minutes=10):
            with self.lock:
                cutoff_time = now - timedelta(hours=2)
                # 古いエントリを削除
                identifiers_to_remove = []
                for identifier, requests in self.requests.items():
                    self.requests[identifier] = [
                        req_time for req_time in requests
                        if req_time > cutoff_time
                    ]
                    # 空のリストは削除
                    if not self.requests[identifier]:
                        identifiers_to_remove.append(identifier)
                
                for identifier in identifiers_to_remove:
                    del self.requests[identifier]
                
                self.last_cleanup = now
                logger.info(f"Cleaned up rate limiter memory. Active identifiers: {len(self.requests)}")
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, str]:
        """
        レート制限をチェック
        
        Args:
            identifier: ユーザー識別子
            
        Returns:
            (制限内かどうか, エラーメッセージ)
        """
        with self.lock:
            now = datetime.utcnow()
            
            # 古いリクエストをクリーンアップ
            self._cleanup_old_requests(identifier, now)
            
            # 定期的な全体クリーンアップ
            self._periodic_cleanup()
            
            # 時間枠の計算
            one_minute_ago = now - timedelta(minutes=1)
            one_hour_ago = now - timedelta(hours=1)
            
            # 各時間枠でのリクエスト数をカウント
            minute_requests = [
                req for req in self.requests[identifier]
                if req > one_minute_ago
            ]
            hour_requests = [
                req for req in self.requests[identifier]
                if req > one_hour_ago
            ]
            
            # 分単位の制限チェック
            if len(minute_requests) >= self.rate_limit_per_minute:
                return False, (
                    f"Rate limit exceeded: {self.rate_limit_per_minute} requests per minute "
                    "(Redis unavailable - stricter limits apply)"
                )
            
            # 時間単位の制限チェック
            if len(hour_requests) >= self.rate_limit_per_hour:
                return False, (
                    f"Rate limit exceeded: {self.rate_limit_per_hour} requests per hour "
                    "(Redis unavailable - stricter limits apply)"
                )
            
            # リクエストを記録
            self.requests[identifier].append(now)
            
            return True, ""
    
    def get_remaining_quota(self, identifier: str) -> dict:
        """
        残りのクォータを取得
        
        Args:
            identifier: ユーザー識別子
            
        Returns:
            残りのリクエスト数
        """
        with self.lock:
            now = datetime.utcnow()
            
            # 古いリクエストをクリーンアップ
            self._cleanup_old_requests(identifier, now)
            
            # 時間枠の計算
            one_minute_ago = now - timedelta(minutes=1)
            one_hour_ago = now - timedelta(hours=1)
            
            # 各時間枠でのリクエスト数をカウント
            minute_count = len([
                req for req in self.requests[identifier]
                if req > one_minute_ago
            ])
            hour_count = len([
                req for req in self.requests[identifier]
                if req > one_hour_ago
            ])
            
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
                "fallback_mode": True,
                "message": "Redis unavailable - using stricter in-memory limits"
            }
    
    def get_status(self) -> dict:
        """
        レート制限システムのステータスを取得
        
        Returns:
            ステータス情報
        """
        with self.lock:
            return {
                "type": "in-memory",
                "active_identifiers": len(self.requests),
                "total_requests": sum(len(reqs) for reqs in self.requests.values()),
                "rate_limits": {
                    "per_minute": self.rate_limit_per_minute,
                    "per_hour": self.rate_limit_per_hour
                },
                "last_cleanup": self.last_cleanup.isoformat()
            }