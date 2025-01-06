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
DEFAULT_MESSAGE = "Какая температура в помещении unit_1?"

# Инициализация модели
ollama_model = OllamaModel(
    model_name=DEFAULT_MODEL,
    base_url=DEFAULT_URL
)

# Создание агента
agent = Agent(
    model=ollama_model,
    system_prompt="""You are a rental property management assistant. 
    You help manage properties, monitor temperature, control smart home features, and provide advice about snow removal.
    Be concise and professional. Always respond in Russian."""
)

class AgentRentRequest(BaseModel):
    """
    Запрос к агенту по аренде
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

@router.post("/agent-rent")
async def agent_rent(request: AgentRentRequest):
    """
    Отправить запрос агенту по аренде
    
    - **text**: Текст вашего вопроса или запроса к агенту
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
                system_prompt="""You are a rental property management assistant. 
                You help manage properties, monitor temperature, control smart home features, and provide advice about snow removal.
                Be concise and professional. Always respond in Russian."""
            )
            response = temp_agent.run_sync(request.text)
        else:
            response = agent.run_sync(request.text)
            
        return {"response": response.data}
    except Exception as e:
        return {"error": str(e)} 