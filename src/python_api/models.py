from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    """Class representing a todo item"""
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None


class Todo(BaseModel):
    """Class representing a todo item with an ID and creation timestamp"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
