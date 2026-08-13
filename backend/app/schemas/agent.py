from enum import Enum

from pydantic import BaseModel, Field, model_validator


class AgentType(str, Enum):
    CEO = "ceo"
    EMPLOYEE = "employee"


class AgentRole(str, Enum):
    ENGINEERING = "engineering"
    RESEARCH = "research"
    AUTOMATION = "automation"
    ANALYSIS = "analysis"
    GENERAL = "general"


class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Agent(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    agent_type: AgentType = AgentType.EMPLOYEE
    status: AgentStatus | None = None
    capabilities: list[str] = Field(default_factory=list)
    reports_to: str | None = None
    description: str | None = None

    @model_validator(mode="after")
    def set_default_status(self):
        if self.status is None:
            self.status = (
                AgentStatus.ACTIVE
                if self.agent_type == AgentType.CEO
                else AgentStatus.INACTIVE
            )

        return self