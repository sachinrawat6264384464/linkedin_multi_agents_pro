from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MCPToolSchema(BaseModel):
    id: str
    server_id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    is_dangerous: bool = False


class MCPServerSchema(BaseModel):
    id: str
    name: str
    description: str
    status: str = "CONNECTED"
    tools: List[MCPToolSchema] = []


class MCPToolExecutionRequest(BaseModel):
    agent_id: str
    tool_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class MCPToolExecutionResponse(BaseModel):
    tool_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: int = 0

