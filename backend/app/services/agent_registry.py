from app.schemas.agent import Agent, AgentRole


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> Agent:
        self._agents[agent.id] = agent
        return agent

    def get(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    def list_all(self) -> list[Agent]:
        return list(self._agents.values())

    def find_by_role(self, role: AgentRole) -> list[Agent]:
        return [
            agent
            for agent in self._agents.values()
            if agent.role == role
        ]

    def remove(self, agent_id: str) -> bool:
        if agent_id not in self._agents:
            return False

        del self._agents[agent_id]
        return True