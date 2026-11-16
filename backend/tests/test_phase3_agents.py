import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.agents import list_agents, get_agent


@pytest.mark.asyncio
async def test_list_agents_endpoint():
    """Verify all 8 agents are registered and exposed via API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/agents")
        assert response.status_code == 200
        agents = response.json()
        assert len(agents) == 8
        agent_ids = {a["id"] for a in agents}
        expected_ids = {"master", "research", "writer", "designer", "quality", "publisher", "database", "monitoring"}
        assert agent_ids == expected_ids


@pytest.mark.asyncio
async def test_agent_prompt_update():
    """Verify agent system prompt can be updated dynamically."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.put(
            "/api/v1/agents/writer/config",
            json={"system_prompt": "Updated custom prompt for test verification."}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "updated"
        
        # Verify updated prompt is returned
        agent_res = await client.get("/api/v1/agents/writer")
        assert agent_res.json()["system_prompt"] == "Updated custom prompt for test verification."


@pytest.mark.asyncio
async def test_langgraph_workflow_run():
    """Verify execution of full LangGraph 8-node DAG."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/workflows/run",
            json={
                "topic": "Deterministic Read-Back Verification in Agent Pipelines",
                "category": "AI Engineering",
                "auto_approve": True
            }
        )
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "COMPLETED"
        assert result["quality_approved"] is True
        assert result["persisted"] is True
        assert result["published"] is True
        assert "hook" in result
        assert "main_body" in result
        assert result["checksum"] is not None
        assert result["execution_steps"] >= 7

