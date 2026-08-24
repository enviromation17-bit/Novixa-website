from datetime import datetime

from pydantic import BaseModel, Field


class AgentMemoryCreate(BaseModel):
    memory_type: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1)
    memory_metadata: dict = Field(default_factory=dict)
    importance: float = Field(default=0.5, ge=0.0, le=1.0)


class AgentMemory(BaseModel):
    id: int
    agent_id: str
    memory_type: str
    content: str
    memory_metadata: dict
    importance: float
    created_at: datetime