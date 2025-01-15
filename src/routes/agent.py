from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.executors.telegram_executor import TelegramExecutor

router = APIRouter(prefix="/agent", tags=["agent"])

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    intent: str
    params: Dict[str, Any]
    response: str

class TelegramRequest(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Тестовое сообщение от Rentier бота! 🏠"
            }
        }

class TelegramResponse(BaseModel):
    success: bool
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Message sent successfully"
            }
        }

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Основной эндпоинт для общения с агентом
    """
    # Простой пример определения намерения
    message = request.message.lower()
    
    # Если сообщение содержит "отправь" или "отправить" и "телеграм",
    # считаем что это запрос на отправку сообщения в Telegram
    if ("отправь" in message or "отправить" in message) and "телеграм" in message:
        return {
            "intent": "send_telegram",
            "params": {"message": message},
            "response": "Хорошо, отправляю сообщение в Telegram"
        }
    
    # По умолчанию считаем, что это просто чат
    return {
        "intent": "chat",
        "params": {},
        "response": "Извините, я пока умею только отправлять сообщения в Telegram"
    }

@router.post("/execute")
async def execute(intent: str, params: Dict[str, Any]):
    """
    Выполняет действие в зависимости от намерения
    """
    if intent == "send_telegram":
        executor = TelegramExecutor()
        result = await executor.execute(params)
        return result
    
    raise HTTPException(status_code=400, detail=f"Unknown intent: {intent}")

@router.post("/telegram/send", response_model=TelegramResponse, tags=["telegram"])
async def send_telegram(request: TelegramRequest):
    """
    Отправляет сообщение в Telegram.
    
    Требует наличия пер��менных окружения:
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_DEFAULT_CHAT_ID
    
    Пример запроса:
    ```json
    {
        "message": "Тестовое сообщение от Rentier бота! 🏠"
    }
    ```
    """
    executor = TelegramExecutor()
    result = await executor.execute({
        "message": request.message
    })
    return result 