import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
import bleach
from bleach.css_sanitizer import CSSSanitizer
import markdown
import re
import html
from app.config import settings


class SecurityService:
    """セキュリティ関連のサービス"""
    
    ALGORITHM = "HS256"
    
    @staticmethod
    def generate_session_id() -> str:
        """セッションIDを生成"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_csrf_token() -> str:
        """CSRFトークンを生成"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_ip(ip_address: str) -> str:
        """IPアドレスをハッシュ化（プライバシー保護）"""
        return hashlib.sha256(f"{ip_address}{settings.SECRET_KEY}".encode()).hexdigest()
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """アクセストークンを作成"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=SecurityService.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """トークンを検証"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[SecurityService.ALGORITHM])
            return payload
        except JWTError:
            return None
    
    # Bleach設定
    ALLOWED_TAGS = [
        'p', 'br', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'strong', 'em', 'u', 'i', 'b', 'code', 'pre', 'blockquote',
        'ul', 'ol', 'li', 'hr', 'a', 'img'
    ]
    
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'code': ['class'],  # シンタックスハイライト用
        '*': ['class', 'id']  # 基本的なスタイリング用
    }
    
    ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
    
    # CSS サニタイザーの設定
    CSS_SANITIZER = CSSSanitizer(
        allowed_css_properties=[
            'color', 'background-color', 'font-size', 'font-weight',
            'text-align', 'margin', 'padding', 'border', 'width', 'height'
        ]
    )
    
    @staticmethod
    def sanitize_input(text: str, allow_html: bool = False) -> str:
        """
        入力をサニタイズ（XSS対策強化版）
        
        Args:
            text: サニタイズするテキスト
            allow_html: HTMLタグを許可するかどうか
            
        Returns:
            サニタイズされたテキスト
        """
        if not text:
            return ""
        
        # 基本的なクリーニング
        text = text.strip()
        
        # 制御文字の除去
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        if allow_html:
            # HTMLを許可する場合はbleachでサニタイズ
            cleaned = bleach.clean(
                text,
                tags=SecurityService.ALLOWED_TAGS,
                attributes=SecurityService.ALLOWED_ATTRIBUTES,
                protocols=SecurityService.ALLOWED_PROTOCOLS,
                strip=True,
                css_sanitizer=SecurityService.CSS_SANITIZER
            )
            return cleaned
        else:
            # HTMLを許可しない場合は完全にエスケープ
            return html.escape(text)
    
    @staticmethod
    def sanitize_markdown(text: str) -> str:
        """
        Markdownテキストを安全にHTMLに変換
        
        Args:
            text: Markdownテキスト
            
        Returns:
            サニタイズされたHTML
        """
        if not text:
            return ""
        
        # まずMarkdownをHTMLに変換
        md = markdown.Markdown(
            extensions=['extra', 'codehilite', 'toc'],
            output_format='html'
        )
        html_content = md.convert(text)
        
        # 生成されたHTMLをサニタイズ
        return SecurityService.sanitize_input(html_content, allow_html=True)
    
    @staticmethod
    def remove_javascript_urls(text: str) -> str:
        """JavaScriptプロトコルURLを除去"""
        # javascript:, vbscript:, data: URLを検出して除去
        dangerous_protocols = re.compile(
            r'(javascript|vbscript|data):[^"\s]*',
            re.IGNORECASE
        )
        return dangerous_protocols.sub('', text)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """ファイル名をサニタイズ（パストラバーサル対策）"""
        # 危険な文字を除去
        filename = re.sub(r'[^\w\s.-]', '', filename)
        # パストラバーサルを防ぐ
        filename = filename.replace('..', '')
        filename = filename.replace('/', '')
        filename = filename.replace('\\', '')
        return filename.strip()
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """URLの妥当性を検証"""
        if not url:
            return False
        
        # 許可されたプロトコルのみ
        allowed_protocols = ['http://', 'https://', 'mailto:']
        if not any(url.startswith(proto) for proto in allowed_protocols):
            return False
        
        # JavaScriptプロトコルをブロック
        if 'javascript:' in url.lower() or 'vbscript:' in url.lower():
            return False
        
        return True
    
    @staticmethod
    def escape_for_json(text: str) -> str:
        """JSON出力用のエスケープ"""
        if not text:
            return ""
        
        # JSONで問題となる文字をエスケープ
        text = text.replace('\\', '\\\\')
        text = text.replace('"', '\\"')
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        text = text.replace('\t', '\\t')
        
        return text