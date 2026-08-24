from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.agent_service import AgentService
from app.services.agent_memory_service import AgentMemoryService
from app.schemas.agent_memory import AgentMemory, AgentMemoryCreate


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/agents/{agent_id}/memories",
    response_model=AgentMemory,
    summary="Create Agent Memory",
    description="Stores persistent memory for an AI agent.",
    tags=["Agent Memory"],
)
def create_agent_memory(
    agent_id: str,
    memory: AgentMemoryCreate,
    db: Session = Depends(get_db),
):
    agent_service = AgentService(db)

    if agent_service.get_agent(agent_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found.",
        )

    memory_service = AgentMemoryService(db)

    return memory_service.create_memory(
        agent_id=agent_id,
        memory=memory,
    )


@router.get(
    "/agents/{agent_id}/memories",
    response_model=list[AgentMemory],
    summary="List Agent Memories",
    description="Returns persistent memories belonging to an AI agent.",
    tags=["Agent Memory"],
)
def list_agent_memories(
    agent_id: str,
    db: Session = Depends(get_db),
):
    agent_service = AgentService(db)

    if agent_service.get_agent(agent_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found.",
        )

    memory_service = AgentMemoryService(db)

    return memory_service.list_memories(agent_id)