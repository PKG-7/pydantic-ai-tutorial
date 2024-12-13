"""
Пример использования структурированных ответов.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from connection import model

class ResponseModel(BaseModel):
    """Структурированный ответ с метаданными."""
    response: str
    needs_escalation: bool
    follow_up_required: bool
    is_offensive: bool
    sentiment: str = Field(description="Customer sentiment analysis")

agent2 = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent. You always answer in Russian."
        "Analyze queries carefully and provide structured responses."
    ),
)

if __name__ == "__main__":
    response = agent2.run_sync("я твой рот ебал")
    print(response.data.model_dump_json(indent=2)) 