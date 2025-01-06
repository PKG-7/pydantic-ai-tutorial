from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class AgentRentRequest(BaseModel):
    text: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Какая температура в помещении unit_1?"
            }
        }

class AgentRentResponse(BaseModel):
    response: str

@router.post("/agent-rent", response_model=AgentRentResponse)
async def agent_rent(request: AgentRentRequest):
    """Эндпоинт для работы с агентом по аренде помещений"""
    try:
        # TODO: Здесь будет логика работы с агентом
        response = f"Получен запрос к агенту по аренде: {request.text}"
        return AgentRentResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 