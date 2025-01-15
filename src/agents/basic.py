"""
Простой бот с базовым функционалом ответов на вопросы.
"""

from pydantic_ai import Agent
from ..stormlabs.model import stormlabs_model

# Создаем простого агента
AgentBasic = Agent(
    model=stormlabs_model('small'),
    system_prompt="Ты полезный помощник. Отвечай на русском языке. не больше 30 слов",
)

