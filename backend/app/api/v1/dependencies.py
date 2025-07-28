from fastapi import Request, HTTPException, Header
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> str:
    """
    クライアントのIPアドレスを取得
    
    プロキシ経由の場合も考慮してIPアドレスを取得します。
    """
    # X-Forwarded-Forヘッダーをチェック（プロキシ経由の場合）
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # 最初のIPアドレスを取得
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        # 直接接続の場合
        client_ip = request.client.host
    
    return client_ip


async def validate_csrf_token(
    x_csrf_token: Optional[str] = Header(None),
    x_requested_with: Optional[str] = Header(None)
) -> bool:
    """
    CSRFトークンを検証
    
    POSTリクエストに対してCSRF保護を提供します。
    """
    # 現在は簡易実装。本番環境では適切なCSRF保護を実装
    if x_requested_with != "XMLHttpRequest":
        logger.warning("Missing X-Requested-With header")
        # 現在は警告のみ（開発中のため）
    
    return True