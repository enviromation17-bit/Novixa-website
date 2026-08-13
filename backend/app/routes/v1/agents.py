from fastapi import APIRouter, HTTPException

from app.schemas.agent import Agent, AgentRole
from app.services.agent_service import AgentService


router = APIRouter()

agent_service = AgentService()


@router.post(
    "/agents",
    response_model=Agent,
    summary="Create Agent",
    description="Creates and registers an AI agent.",
    tags=["Agents"],
)
def create_agent(agent: Agent):
    existing = agent_service.get_agent(agent.id)

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Agent with this ID already exists.",
        )

    return agent_service.create_agent(agent)


@router.get(
    "/agents",
    response_model=list[Agent],
    summary="List Agents",
    description="Returns all registered AI agents.",
    tags=["Agents"],
)
def list_agents():
    return agent_service.list_agents()


@router.get(
    "/agents/{agent_id}",
    response_model=Agent,
    summary="Get Agent",
    description="Returns a registered AI agent by ID.",
    tags=["Agents"],
)
def get_agent(agent_id: str):
    agent = agent_service.get_agent(agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found.",
        )

    return agent


@router.get(
    "/agents/role/{role}",
    response_model=list[Agent],
    summary="Find Agents by Role",
    description="Returns agents matching a specific role.",
    tags=["Agents"],
)
def find_agents_by_role(role: AgentRole):
    return agent_service.find_by_role(role)


@router.delete(
    "/agents/{agent_id}",
    summary="Remove Agent",
    description="Removes a registered AI agent.",
    tags=["Agents"],
)
def remove_agent(agent_id: str):
    removed = agent_service.remove_agent(agent_id)

    if not removed:
        raise HTTPException(
            status_code=404,
            detail="Agent not found.",
        )

    return {
        "success": True,
        "message": "Agent removed successfully.",
    }