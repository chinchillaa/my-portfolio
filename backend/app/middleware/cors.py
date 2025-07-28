from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    CORS設定を行う
    
    Args:
        app: FastAPIアプリケーションインスタンス
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Session-ID",
            "X-CSRF-Token",
            "X-Requested-With"
        ],
        expose_headers=[
            "X-Session-ID",
            "X-CSRF-Token",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset"
        ]
    )