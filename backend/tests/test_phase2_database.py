import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.db.models import Task, ContentDraft, ContentVersion, Approval, MCPServer, MCPTool


@pytest.mark.asyncio
async def test_database_health_endpoint():
    """Verify database health API endpoint returns structured connectivity metadata."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/database/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "ssl_mode" in data
        assert data["read_back_verification_active"] is True


@pytest.mark.asyncio
async def test_database_statistics_endpoint():
    """Verify table statistics endpoint returns real or zeroed row counts."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/database/statistics")
        assert response.status_code == 200
        stats = response.json()
        assert "tasks" in stats
        assert "content_versions" in stats
        assert "published_posts" in stats


def test_content_version_checksum_calculation():
    """Verify SHA-256 content checksum produces deterministic cryptographic fingerprints."""
    hook = "Why 90% of AI agent systems fail in production."
    body = "Most teams treat LLM outputs as final without deterministic read-back verification."
    cta = "How do you enforce durability in your agent workflows?"

    checksum1 = ContentVersion.calculate_checksum(hook, body, cta)
    checksum2 = ContentVersion.calculate_checksum(hook, body, cta)
    assert checksum1 == checksum2
    assert len(checksum1) == 64

    # Non-whitespace modification must produce a different checksum
    checksum_altered = ContentVersion.calculate_checksum(hook + " An update.", body, cta)
    assert checksum_altered != checksum1


def test_task_model_initialization():
    """Verify Task entity initialization."""
    task = Task(
        title="Deep Dive into Model Context Protocol",
        topic="MCP Architecture",
        category="AI Engineering",
        target_audience="Software Architects",
        status="PENDING"
    )
    assert task.title == "Deep Dive into Model Context Protocol"
    assert task.status == "PENDING"
    assert task.category == "AI Engineering"
