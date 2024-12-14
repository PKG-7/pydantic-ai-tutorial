"""
Пример использования агента с зависимостями и контекстом.
"""

from typing import List, Optional
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from connection import model
from utils.markdown import to_markdown
from structured_response import ResponseModel

class Order(BaseModel):
    """Структура для деталей заказа."""
    order_id: str
    status: str
    items: List[str]

class CustomerDetails(BaseModel):
    """Структура для данных клиента."""
    customer_id: str
    name: str
    email: str
    orders: Optional[List[Order]] = None

agent5 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses. "
        "Always great the customer and provide a helpful response."
    ),
)

@agent5.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"

if __name__ == "__main__":
    customer = CustomerDetails(
        customer_id="1",
        name="John Doe",
        email="john.doe@example.com",
        orders=[
            Order(order_id="12345", status="shipped", items=["Blue Jeans", "T-Shirt"]),
        ],
    )

    response = agent5.run_sync(user_prompt="What did I order?", deps=customer)
    print(response.data.model_dump_json(indent=2)) 