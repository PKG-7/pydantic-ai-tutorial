"""
Основной файл для запуска агента
"""

from src.agents.isRude import AgentIsRude
from src.agents.basic import AgentBasic
from src.agents.tools import AgentWithTools, OrderDetails

if __name__ == "__main__":
    # Тест AgentIsRude
    # response = AgentIsRude.run_sync('сосал?')
    # print('👿 AgentIsRude: ', response.data.model_dump_json(indent=2))
    
    # # Тест AgentBasic
    # response = AgentBasic.run_sync('Расстояние до луны') 
    # print('📊 AgentBasic: ', response.data)
    
    # Тест AgentWithTools
    customer = OrderDetails(
        order_id="12346",
        customer_name="Иван Хуев Сосалин",
        email="ivan@example.com"
    )
    
    response = AgentWithTools.run_sync(
        user_prompt="как меня зовут?",
        deps=customer
    )
    print('🛠 AgentWithTools: ', response.data.model_dump_json(indent=2))
    