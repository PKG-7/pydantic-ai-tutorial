"""
Простой бот с базовым функционалом ответов на вопросы.
"""

from pydantic_ai import Agent
from src.connection import model

# Создаем простого агента
agent1 = Agent(
    model=model,
    system_prompt="Ты полезный помощник. Отвечай на русском языке.",
)

# Пример использования
if __name__ == "__main__":
    try:
        response = agent1.run_sync("Привет, как дела?")
        print("Connection successful!")
        print(response.data)
        
        response2 = agent1.run_sync(
            user_prompt="Какой был мой предыдущий вопрос?",
            message_history=response.new_messages(),
        )
        print(response2.data)
    except Exception as e:
        print(f"Connection error: {e}")