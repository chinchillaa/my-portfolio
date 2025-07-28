from fastapi import APIRouter, Request, Header, Depends
from typing import Optional
import logging
from app.models import ChatRequest, ChatResponse, ErrorResponse
from app.services import GeminiService, RateLimiter
from app.core import SecurityService, ValidationException, RateLimitException
from app.api.v1.dependencies import get_client_ip, validate_csrf_token

logger = logging.getLogger(__name__)
router = APIRouter()

# サービスのインスタンス化
gemini_service = GeminiService()
rate_limiter = RateLimiter()
security_service = SecurityService()


@router.post("", response_model=ChatResponse, responses={
    400: {"model": ErrorResponse, "description": "Bad Request"},
    429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
    503: {"model": ErrorResponse, "description": "Service Unavailable"}
})
async def chat(
    request: Request,
    chat_request: ChatRequest,
    client_ip: str = Depends(get_client_ip),
    x_session_id: Optional[str] = Header(None),
    x_csrf_token: Optional[str] = Header(None)
):
    """
    チャットエンドポイント
    
    ユーザーのメッセージに対してAIアシスタントが応答します。
    """
    try:
        # 入力のサニタイズ
        sanitized_message = security_service.sanitize_input(chat_request.message)
        
        # コンテンツの安全性チェック
        safety_check = await gemini_service.check_content_safety(sanitized_message)
        if not safety_check["is_safe"]:
            raise ValidationException("Unsafe content detected")
        
        # IPアドレスのハッシュ化（プライバシー保護）
        hashed_ip = security_service.hash_ip(client_ip)
        
        # レート制限チェック
        await rate_limiter.check_rate_limit(hashed_ip)
        
        # セッションIDの生成または検証
        session_id = x_session_id or security_service.generate_session_id()
        
        # 受信メッセージをログに記録
        logger.info(f"[Chat Request] Session: {session_id[:8]}..., Message: {sanitized_message}")
        
        # Gemini APIで応答を生成
        response_text = await gemini_service.generate_response(
            message=sanitized_message,
            context=chat_request.context
        )
        
        # 応答メッセージをログに記録
        logger.info(f"[Chat Response] Session: {session_id[:8]}..., Response: {response_text[:100]}...")
        
        # レスポンスの作成
        return ChatResponse(
            message=response_text,
            session_id=session_id,
            status="success"
        )
        
    except RateLimitException as e:
        logger.warning(f"Rate limit exceeded for IP: {hashed_ip}, Session: {x_session_id}")
        raise e
    except ValidationException as e:
        logger.warning(f"Validation error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        raise


@router.get("/quota")
async def get_quota(
    request: Request,
    client_ip: str = Depends(get_client_ip)
):
    """
    レート制限の残りクォータを取得
    
    現在のIPアドレスに対する残りリクエスト数を返します。
    """
    hashed_ip = security_service.hash_ip(client_ip)
    quota = await rate_limiter.get_remaining_quota(hashed_ip)
    
    return {
        "quota": quota,
        "status": "success"
    }