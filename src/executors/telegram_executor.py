from typing import Dict, Any
from .base import ExecutorInterface
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramExecutor(ExecutorInterface):
    """Executor для работы с Telegram"""
    
    def __init__(self):
        self.bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        self.default_chat_id = os.getenv("TELEGRAM_DEFAULT_CHAT_ID")
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет сообщение в Telegram
        
        Args:
            params: {
                "message": str - текст сообщения,
                "chat_id": Optional[int] - ID чата (если не указан, используется default_chat_id)
            }
            
        Returns:
            {"success": bool, "message": str}
        """
        try:
            message = params.get("message")
            chat_id = params.get("chat_id", self.default_chat_id)
            
            if not message:
                return {"success": False, "message": "Message is required"}
                
            if not chat_id:
                return {"success": False, "message": "Chat ID is required"}
            
            await self.bot.send_message(chat_id=chat_id, text=message)
            return {"success": True, "message": "Message sent successfully"}
            
        except Exception as e:
            return {"success": False, "message": f"Error sending message: {str(e)}"} 