"""Schemas for AI memory operations."""

from datetime import datetime

from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    owner_id: str = Field(min_length=1, max_length=128)
    memory_type: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1)


class MemoryResponse(BaseModel):
    id: int
    owner_id: str
    memory_type: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }