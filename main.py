"""
Основной файл для запуска агента
"""

from src.agents.isRude import AgentIsRude

# def analyze_text(text: str) -> None:
#     """Анализируем текст с помощью агента"""
#     response = AgentIsRude.run_sync(text)
#     print(f"Анализ текста: '{text}'")
#     print(response.data.model_dump_json(indent=2))

if __name__ == "__main__":
    response = AgentIsRude.run_sync('сосал?')
    print('👿 AgentIsRude: ', response.data.model_dump_json(indent=2))
    