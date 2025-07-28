from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.api.v1 import api_router
from app.core.exceptions import ChatbotException
from app.middleware import setup_middleware

# ログ設定
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時の処理
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield
    # 終了時の処理
    logger.info("Shutting down application")


# FastAPIアプリケーションの作成
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# ミドルウェアの設定
setup_middleware(app)

# CORS設定
# ALLOWED_ORIGINSが確実にリストであることを保証
allowed_origins = settings.ALLOWED_ORIGINS
if isinstance(allowed_origins, str):
    allowed_origins = [allowed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Session-ID", "X-CSRF-Token"]
)

# 信頼できるホストの設定
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.railway.app", "chinchillaa.github.io"]
    )


# エラーハンドラー
@app.exception_handler(ChatbotException)
async def chatbot_exception_handler(request: Request, exc: ChatbotException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "detail": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else None
        }
    )


# APIルーターの登録
app.include_router(api_router, prefix=settings.API_V1_STR)


# ルートエンドポイント
@app.get("/")
async def root():
    return {
        "message": "Portfolio Chatbot API",
        "version": settings.VERSION,
        "status": "running"
    }