"""
Агент с инструментами для расширенного функционала.
"""

from typing import Dict
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool, ModelRetry
from ..stormlabs.model import stormlabs_model

# База данных с информацией о доставке
shipping_info_db: Dict[str, str] = {
    "#12345": "Отправлено 2024-01-15",
    "#67890": "В пути",
}

class OrderDetails(BaseModel):
    """Структура для деталей заказа."""
    order_id: str
    customer_name: str
    email: str = Field(description="Email клиента")

class ResponseModel(BaseModel):
    """Структурированный ответ с метаданными."""
    response: str
    needs_escalation: bool
    follow_up_required: bool
    sentiment: str = Field(description="Анализ настроения клиента")

def get_shipping_status(order_id: str) -> str:
    """Получить статус доставки по ID заказа."""
    if not order_id.startswith('#'):
        order_id = f"#{order_id}"
        
    shipping_status = shipping_info_db.get(order_id)
    if shipping_status is None:
        raise ModelRetry(
            f"Информация о заказе {order_id} не найдена. "
            "ID заказа должен начинаться с #. "
            "Например: #624743"
        )
    return shipping_status

# Создаем агента с инструментами
AgentWithTools = Agent(
    model=stormlabs_model('small'),
    result_type=ResponseModel,
    deps_type=OrderDetails,
    retries=3,
    system_prompt=(
        "Ты умный агент поддержки клиентов. "
        "Внимательно анализируй запросы и используй инструменты для поиска информации. "
        "Всегда отвечай на русском языке и будь вежлив."
        "Если кода нет - ответь, что нет такого кода"
    ),
)

@AgentWithTools.tool_plain()
def check_shipping(order_id: str) -> str:
    """Проверить статус доставки заказа."""
    return get_shipping_status(order_id)

@AgentWithTools.system_prompt
async def add_customer_details(ctx: RunContext[OrderDetails]) -> str:
    return f"Детали клиента: Имя={ctx.deps.customer_name}, Email={ctx.deps.email}, Заказ={ctx.deps.order_id}" 