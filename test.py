import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel

nest_asyncio.apply()

# Инициализация модели
ollama_model = OllamaModel(
    model_name='qwen2.5-coder:7b',
    base_url='http://192.168.1.31:11434/v1'
)

# Создание агента
agent = Agent(
    model=ollama_model,
    system_prompt="You are a helpful assistant. Be concise."
)

# Тест подключения
try:
    response = agent.run_sync("Привет, как дела?")
    print("Connection successful!")
    print("Response:", response.data)
except Exception as e:
    print(f"Connection error: {e}")