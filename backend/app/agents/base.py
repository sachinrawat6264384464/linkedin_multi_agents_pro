from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.integrations.ollama.client import ollama_client
from app.core.logging import logger


class AgentResult(BaseModel):
    agent_id: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    duration_ms: int = 0


class BaseAgent(ABC):
    """
    Standardized base agent contract for all 8 LinkedIn AgentOS agents.
    Every agent operates with:
    - Scoped system prompt
    - Strict input/output validation
    - Execution logging and error isolation
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        description: str,
        system_prompt: str,
        model_name: str = "qwen2.5:7b-instruct"
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.description = description
        self.system_prompt = system_prompt
        self.model_name = model_name

    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> AgentResult:
        """Execute the agent's task given current LangGraph state."""
        pass

    async def run_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        format_json: bool = True
    ) -> str:
        """Execute completion via shared Ollama client."""
        return await ollama_client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            model=self.model_name,
            temperature=temperature,
            format_json=format_json
        )

