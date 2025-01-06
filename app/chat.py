from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel

# Создаем роутер
router = APIRouter()

# Значения по умолчанию
DEFAULT_MODEL = 'qwen2.5-coder:32b'
DEFAULT_URL = 'http://192.168.1.31:11434/v1'
DEFAULT_MESSAGE = "Привет, как дела?"

# Инициализация модели
ollama_model = OllamaModel(
    model_name=DEFAULT_MODEL,
    base_url=DEFAULT_URL
)

# Создание агента
agent = Agent(
    model=ollama_model,
    system_prompt="You are a helpful assistant. Be concise."
)

class ChatRequest(BaseModel):
    """
    Запрос к чат-ассистенту
    """
    text: str
    model_name: Optional[str] = DEFAULT_MODEL
    base_url: Optional[str] = DEFAULT_URL
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": DEFAULT_MESSAGE,
                    "model_name": DEFAULT_MODEL,
                    "base_url": DEFAULT_URL
                }
            ]
        }
    }

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Отправить текстовый запрос AI ассистенту
    
    - **text**: Текст вашего вопроса или запроса к ассистенту
    - **model_name**: (опционально) Имя модели для использования
    - **base_url**: (опционально) URL сервера с моделью
    """
    try:
        # Создаем новую модель если параметры отличаются от дефолтных
        if request.model_name != DEFAULT_MODEL or request.base_url != DEFAULT_URL:
            model = OllamaModel(
                model_name=request.model_name,
                base_url=request.base_url
            )
            temp_agent = Agent(
                model=model,
                system_prompt="You are a helpful assistant. Be concise."
            )
            response = temp_agent.run_sync(request.text)
        else:
            response = agent.run_sync(request.text)
            
        return {"response": response.data}
    except Exception as e:
        return {"error": str(e)} 