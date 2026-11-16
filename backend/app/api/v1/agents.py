from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.agents import list_agents, get_agent

router = APIRouter(prefix="/agents", tags=["AI Agents"])


class AgentSummary(BaseModel):
    id: str
    name: str
    role: str
    description: str
    model_name: str
    system_prompt: str


class UpdateAgentPromptRequest(BaseModel):
    system_prompt: str
    model_name: Optional[str] = None


@router.get("", response_model=List[AgentSummary])
async def get_all_agents():
    """Retrieve all 8 active specialist agents and their operational status."""
    agents_map = list_agents()
    return [
        AgentSummary(
            id=agent.agent_id,
            name=agent.name,
            role=agent.role,
            description=agent.description,
            model_name=agent.model_name,
            system_prompt=agent.system_prompt
        )
        for agent in agents_map.values()
    ]


@router.get("/{agent_id}", response_model=AgentSummary)
async def get_agent_by_id(agent_id: str):
    """Retrieve specific agent profile and current prompt configuration."""
    try:
        agent = get_agent(agent_id)
        return AgentSummary(
            id=agent.agent_id,
            name=agent.name,
            role=agent.role,
            description=agent.description,
            model_name=agent.model_name,
            system_prompt=agent.system_prompt
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' does not exist"
        )


@router.put("/{agent_id}/config")
async def update_agent_config(agent_id: str, request: UpdateAgentPromptRequest):
    """Update agent's system prompt or model selection."""
    try:
        agent = get_agent(agent_id)
        agent.system_prompt = request.system_prompt
        if request.model_name:
            agent.model_name = request.model_name
        return {"status": "updated", "agent_id": agent_id, "model": agent.model_name}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' does not exist"
        )
