from app.schemas.agent import Agent, AgentRole
from app.services.agent_registry import AgentRegistry


class AgentService:
    def __init__(self, registry: AgentRegistry | None = None):
        self.registry = registry or AgentRegistry()

    def create_agent(self, agent: Agent) -> Agent:
        return self.registry.register(agent)

    def get_agent(self, agent_id: str) -> Agent | None:
        return self.registry.get(agent_id)

    def list_agents(self) -> list[Agent]:
        return self.registry.list_all()

    def find_by_role(self, role: AgentRole) -> list[Agent]:
        return self.registry.find_by_role(role)

    def remove_agent(self, agent_id: str) -> bool:
        return self.registry.remove(agent_id)