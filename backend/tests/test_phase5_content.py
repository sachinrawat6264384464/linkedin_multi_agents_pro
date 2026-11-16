import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.services.content_service import ContentService


@pytest.mark.asyncio
async def test_research_search_endpoint():
    """Verify research search returns structured articles."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/research/search?query=Model+Context+Protocol")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 1
        assert "results" in data
        assert "url" in data["results"][0]


@pytest.mark.asyncio
async def test_research_sources_endpoint():
    """Verify research sources list."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/research/sources")
        assert response.status_code == 200
        sources = response.json()
        assert len(sources) >= 2


@pytest.mark.asyncio
async def test_content_variations_generator():
    """Verify AI content variation generator produces multiple styles."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/content/generate",
            json={
                "topic": "Deterministic Durability in Multi-Agent Workflows",
                "category": "AI Engineering"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 2
        assert "variations" in data
        for var in data["variations"]:
            assert "hook" in var
            assert "main_body" in var
            assert "checksum" in var


@pytest.mark.asyncio
async def test_content_draft_save_and_checksum():
    """Verify draft saving with SHA-256 calculation."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        hook = "Why 90% of AI agent architectures fail."
        body = "Because they do not implement deterministic read-back verification."
        cta = "How do you test persistence in your agents?"

        expected_checksum = ContentService.calculate_checksum(hook, body, cta)

        response = await client.post(
            "/api/v1/content/drafts",
            json={
                "title": "Agent Failure Modes",
                "topic": "AI Engineering",
                "category": "AI Engineering",
                "hook": hook,
                "main_body": body,
                "cta": cta,
                "hashtags": ["#AI", "#Engineering"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "saved"
        assert data["checksum"] == expected_checksum
