"""
Пример использования агента с инструментами.
"""

from typing import Dict
from pydantic_ai import Agent, RunContext, Tool, ModelRetry
from connection import model
from dependencies import CustomerDetails
from structured_response import ResponseModel

shipping_info_db: Dict[str, str] = {
    "#12345": "Shipped on 2024-12-01",
    "#67890": "Out for delivery",
}

def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
    """Получить информацию о доставке клиента."""
    return shipping_info_db[ctx.deps.orders[0].order_id]

agent = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses. "
        "Use tools to look up relevant information."
        "Always great the customer and provide a helpful response."
    ),
    tools=[Tool(get_shipping_info, takes_ctx=True)],
)

@agent.tool_plain()
def get_shipping_status(order_id: str) -> str:
    """Получить статус доставки по ID заказа."""
    shipping_status = shipping_info_db.get(order_id)
    if shipping_status is None:
        raise ModelRetry(
            f"No shipping information found for order ID {order_id}. "
            "Make sure the order ID starts with a #: e.g, #624743 "
            "Self-correct this if needed and try again."
        )
    return shipping_info_db[order_id]

if __name__ == "__main__":
    customer = CustomerDetails(
        customer_id="1",
        name="John Doe",
        email="john.doe@example.com",
    )
    
    response = agent.run_sync(
        user_prompt="What's the status of my last order #12345?", 
        deps=customer
    )
    print(response.data.model_dump_json(indent=2)) 