from abc import ABC, abstractmethod
from typing import Dict, Any

class ExecutorInterface(ABC):
    """Базовый интерфейс для всех executor'ов"""
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет действие с заданными параметрами
        
        Args:
            params: Параметры для выполнения действия
            
        Returns:
            Результат выполнения действия
        """
        pass 