from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel

class DatabaseAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class DatabaseCommand(BaseModel):
    table: str
    id: str
    values: Dict[str, Any]
    action: DatabaseAction

class StructuredResponse(BaseModel):
    action: str = "text"  # "text" | "database"
    response: str
    database_command: Optional[DatabaseCommand] = None

    def is_database_action(self) -> bool:
        return self.action == "database" and self.database_command is not None 