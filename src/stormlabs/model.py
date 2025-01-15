from typing import Literal
from pydantic_ai.models.ollama import OllamaModel

ModelSize = Literal['small', 'large', 'reasoning']

# llama3.1:8b                46e0c10c039e    4.9 GB    
# qwq:32b                    46407beda5c0    19 GB     
# qwen2.5-coder:7b           2b0496514337    4.7 GB   
# qwen2.5-coder:32b          4bd6cbf2d094    19 GB     
# nomic-embed-text:latest    0a109f422b47    274 MB    
# qwen2.5-coder:latest       2b0496514337    4.7 GB   

MODEL_MAP = {
    'small': {
        'name': 'llama3.1:8b',
        'url': 'http://192.168.1.31:11434/v1'
    },
    'large': {
        'name': 'qwen2.5-coder:32b',
        'url': 'http://192.168.1.31:11434/v1'
    },
    'reasoning': {
        'name': 'qwq:32b',
        'url': 'http://192.168.1.31:11434/v1'
    }
}

def stormlabs_model(size: ModelSize) -> OllamaModel:
    config = MODEL_MAP[size]
    return OllamaModel(
        model_name=config['name'],
        base_url=config['url']
    ) 