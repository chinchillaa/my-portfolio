import google.generativeai as genai
from typing import List, Optional, Dict, Any
import logging
import os
from pathlib import Path
from app.config import settings
from app.core.exceptions import GeminiAPIException
from app.models import ChatMessage

logger = logging.getLogger(__name__)


class GeminiService:
    """Gemini API統合サービス"""
    
    def __init__(self):
        """サービスの初期化"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=1024,
        )
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        # システムプロンプトをファイルから読み込む
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """システムプロンプトをファイルから読み込む"""
        try:
            # プロンプトファイルのパスを構築
            base_dir = Path(__file__).resolve().parent.parent
            prompt_file = base_dir / "prompts" / "system_prompt.txt"
            
            # ファイルが存在しない場合のデフォルトプロンプト
            if not prompt_file.exists():
                logger.warning(f"System prompt file not found at {prompt_file}")
                return "あなたは親切なAIアシスタントです。"
            
            # ファイルから読み込み
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
                logger.info("System prompt loaded successfully")
                return prompt
                
        except Exception as e:
            logger.error(f"Error loading system prompt: {str(e)}")
            return "あなたは親切なAIアシスタントです。"
    
    async def generate_response(
        self,
        message: str,
        context: Optional[List[ChatMessage]] = None
    ) -> str:
        """
        メッセージに対する応答を生成
        
        Args:
            message: ユーザーからのメッセージ
            context: 会話履歴
            
        Returns:
            生成された応答テキスト
        """
        try:
            # 会話履歴を含むプロンプトを構築
            prompt_parts = [self.system_prompt]
            
            # コンテキストがある場合は追加
            if context:
                for msg in context[-5:]:  # 直近5件のみ使用
                    role_prefix = "ユーザー:" if msg.role == "user" else "アシスタント:"
                    prompt_parts.append(f"{role_prefix} {msg.content}")
            
            # 現在のメッセージを追加
            prompt_parts.append(f"ユーザー: {message}")
            prompt_parts.append("アシスタント:")
            
            full_prompt = "\n\n".join(prompt_parts)
            
            # Gemini APIで応答を生成
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # 応答のチェック
            if not response or not response.text:
                raise GeminiAPIException("Empty response from Gemini API")
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise GeminiAPIException(f"Failed to generate response: {str(e)}")
    
    async def check_content_safety(self, text: str) -> Dict[str, Any]:
        """
        コンテンツの安全性をチェック
        
        Args:
            text: チェックするテキスト
            
        Returns:
            安全性チェックの結果
        """
        try:
            # 簡易的な安全性チェック（実際のプロダクションではより高度な実装を推奨）
            dangerous_keywords = ['script', 'eval', 'exec', 'system', 'os.']
            
            is_safe = not any(keyword in text.lower() for keyword in dangerous_keywords)
            
            return {
                "is_safe": is_safe,
                "confidence": 0.9 if is_safe else 0.1,
                "reasons": [] if is_safe else ["Potentially dangerous content detected"]
            }
            
        except Exception as e:
            logger.error(f"Safety check error: {str(e)}")
            return {
                "is_safe": False,
                "confidence": 0.0,
                "reasons": ["Safety check failed"]
            }