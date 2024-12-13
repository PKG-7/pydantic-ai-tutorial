"""
Модуль настройки подключения к LLM моделям.
"""

import nest_asyncio
from pydantic_ai.models.ollama import OllamaModel

nest_asyncio.apply()

# Инициализация модели Ollama
ollama_model = OllamaModel(
    model_name='qwen2.5:32b',
    # model_name='qwen2.5-coder:7b',
    # model_name='llama3.2-vision',
    # model_name='llama3.3:70b-instruct-q2_K',
    base_url='http://192.168.1.31:11434/v1'
)

model = ollama_model