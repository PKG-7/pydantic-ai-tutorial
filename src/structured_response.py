"""
Пример агента со структурированным ответом.
"""

from pydantic import BaseModel
from pydantic_ai import Agent
from connection import model
from models.database_actions import StructuredResponse

class ResponseModel(BaseModel):
    """Базовая модель ответа для всех агентов."""
    response: str
    sentiment: str = "neutral"
    needs_escalation: bool = False
    follow_up_required: bool = False
    is_offensive: bool = False

# Создаем агента со структурированным ответом
agent2 = Agent(
    model=model,
    result_type=StructuredResponse,
    system_prompt="""Ты помощник, который может отвечать на вопросы и выполнять действия с базой данных.

Если пользователь просит изменить данные, ты должен:
1. Определить тип действия (create/update/delete)
2. Определить таблицу, с которой нужно работать
3. Определить ID записи
4. ��пределить значения для изменения

Примеры запросов и ответов:

Запрос: "Измени цену аренды для помещения с id unit_1 на 30000 рублей в месяц"
Ответ: {
    "action": "database",
    "response": "Я изменю цену аренды помещения unit_1 на 30000 рублей в месяц.",
    "database_command": {
        "action": "update",
        "table": "units",
        "id": "unit_1",
        "values": {
            "price_rent_month": 30000
        }
    }
}

Запрос: "Создай новое помещение unit_2 площадью 50 квадратных метров"
Ответ: {
    "action": "database",
    "response": "Я создам новое помещение unit_2 с площадью 50 квадратных метров.",
    "database_command": {
        "action": "create",
        "table": "units",
        "id": "unit_2",
        "values": {
            "square_meters": 50,
            "display_name": "Помещение 2"
        }
    }
}

Запрос: "Удали помещение с id unit_3"
Ответ: {
    "action": "database",
    "response": "Я удалю помещение unit_3 из базы данных.",
    "database_command": {
        "action": "delete",
        "table": "units",
        "id": "unit_3",
        "values": {}
    }
}

Запрос: "Привет, как дела?"
Ответ: {
    "action": "text",
    "response": "Здравствуйте! У меня все хорошо, спасибо что спросили. Как я могу вам помочь с управлением помещениями?",
    "database_command": null
}

Всегда отвечай на русском языке и следуй этому формату ответа."""
)

if __name__ == "__main__":
    # Тестовый запрос
    response = agent2.run_sync("Измени цену аренды для помещения с id unit_1 на 30000 рублей в месяц")
    print(response.data.model_dump_json(indent=2)) 