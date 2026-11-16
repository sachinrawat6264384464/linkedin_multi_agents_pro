from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.mcp.registry import mcp_registry
from app.mcp.schemas import (
    MCPServerSchema,
    MCPToolSchema,
    MCPToolExecutionRequest,
    MCPToolExecutionResponse
)

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol (MCP)"])


@router.get("/servers", response_model=List[MCPServerSchema])
async def list_mcp_servers():
    """Retrieve all registered MCP servers and connection states."""
    return mcp_registry.list_servers()


@router.get("/tools", response_model=List[MCPToolSchema])
async def list_mcp_tools():
    """Discover all registered MCP tools and their typed input schemas."""
    return mcp_registry.list_tools()


@router.post("/execute", response_model=MCPToolExecutionResponse)
async def execute_mcp_tool(request: MCPToolExecutionRequest):
    """
    Execute an approved MCP tool under least-privilege agent authorization.
    Rejects unauthorized agents automatically.
    """
    response = await mcp_registry.execute_tool(
        agent_id=request.agent_id,
        tool_id=request.tool_id,
        parameters=request.parameters
    )
    if not response.success and "PERMISSION_DENIED" in (response.error or ""):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=response.error
        )
    return response

