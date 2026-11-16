from typing import Dict
from app.agents.base import BaseAgent
from app.agents.master.agent import MasterOrchestrator
from app.agents.research.agent import ResearchAgent
from app.agents.writer.agent import ContentWriterAgent
from app.agents.designer.agent import VisualDesignerAgent
from app.agents.quality.agent import QualityAgent
from app.agents.publisher.agent import LinkedInPublisherAgent
from app.agents.database.agent import DatabaseAgent
from app.agents.monitoring.agent import MonitoringAgent

_AGENTS: Dict[str, BaseAgent] = {
    "master": MasterOrchestrator(),
    "research": ResearchAgent(),
    "writer": ContentWriterAgent(),
    "designer": VisualDesignerAgent(),
    "quality": QualityAgent(),
    "publisher": LinkedInPublisherAgent(),
    "database": DatabaseAgent(),
    "monitoring": MonitoringAgent(),
}


def get_agent(agent_id: str) -> BaseAgent:
    """Retrieve an agent instance by ID."""
    if agent_id not in _AGENTS:
        raise KeyError(f"Agent '{agent_id}' not found in registry. Available: {list(_AGENTS.keys())}")
    return _AGENTS[agent_id]


def list_agents() -> Dict[str, BaseAgent]:
    """Retrieve all 8 active agents."""
    return _AGENTS

