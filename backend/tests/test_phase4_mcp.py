import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.mcp.registry import mcp_registry
from app.mcp.permission_manager import MCPPermissionManager


@pytest.mark.asyncio
async def test_mcp_servers_discovery():
    """Verify all 7 MCP servers are registered and discoverable."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/mcp/servers")
        assert response.status_code == 200
        servers = response.json()
        assert len(servers) >= 7
        server_ids = {s["id"] for s in servers}
        assert "research_server" in server_ids
        assert "content_server" in server_ids
        assert "media_server" in server_ids
        assert "database_server" in server_ids
        assert "linkedin_server" in server_ids


@pytest.mark.asyncio
async def test_mcp_tools_discovery():
    """Verify MCP tools expose typed input parameter schemas."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/mcp/tools")
        assert response.status_code == 200
        tools = response.json()
        assert len(tools) >= 7
        tool_ids = {t["id"] for t in tools}
        assert "research:search_web" in tool_ids
        assert "database:verify_record" in tool_ids


@pytest.mark.asyncio
async def test_mcp_authorized_tool_execution():
    """Verify an authorized agent can successfully execute a permitted MCP tool."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/mcp/execute",
            json={
                "agent_id": "research",
                "tool_id": "research:search_web",
                "parameters": {"query": "LangGraph state checkpointing"}
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool_id"] == "research:search_web"
        assert "sources" in data["data"]


@pytest.mark.asyncio
async def test_mcp_permission_denial_enforcement():
    """Verify an agent attempting to invoke an unauthorized tool is strictly blocked with 403."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Writer agent attempting to run web search (which only research agent is permitted to call)
        response = await client.post(
            "/api/v1/mcp/execute",
            json={
                "agent_id": "writer",
                "tool_id": "research:search_web",
                "parameters": {"query": "bypass"}
            }
        )
        assert response.status_code == 403
        assert "PERMISSION_DENIED" in response.json()["detail"]
