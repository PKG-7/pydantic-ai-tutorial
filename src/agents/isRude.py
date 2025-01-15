"""
Пример использования структурированных ответов.
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from ..stormlabs.model import stormlabs_model

class ResponseModel(BaseModel):
    """Структурированный ответ с метаданными."""
    # response: str
    # needs_escalation: bool
    # follow_up_required: bool
    is_offensive: bool
    sentiment: str = Field(description="Customer sentiment analysis")

AgentIsRude = Agent(
    model=stormlabs_model('large'),
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyze queries carefully and provide structured responses."
    ),
)
