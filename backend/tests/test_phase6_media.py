import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.services.media_service import MediaService


def test_mermaid_syntax_generation():
    """Verify Mermaid architecture syntax contains required AgentOS nodes."""
    syntax = MediaService.generate_mermaid_diagram("Autonomous Agent Orchestration")
    assert "flowchart TD" in syntax
    assert "LangGraph Master" in syntax
    assert "Neon PostgreSQL" in syntax
    assert "Cloudinary Asset Pipeline" in syntax


def test_pdf_carousel_generation():
    """Verify in-memory compilation of LinkedIn PDF carousel."""
    slides = [
        {"title": "01: Durable State", "points": ["Rule 1: Never trust in-memory state alone", "Rule 2: Persist state checkpoints"]},
        {"title": "02: Cloudinary Upload", "points": ["Stream directly without ephemeral disk", "Set resource_type='raw' for PDFs"]}
    ]
    pdf_bytes = MediaService.generate_pdf_carousel_bytes(slides)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF-")  # Valid PDF binary signature


@pytest.mark.asyncio
async def test_diagram_endpoint():
    """Verify /api/v1/media/diagram endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/media/diagram",
            json={"topic": "Agent State Recovery", "flow_type": "architecture"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["media_type"] == "DIAGRAM"
        assert "flowchart" in data["syntax"]
        assert "cloudinary_url" in data


@pytest.mark.asyncio
async def test_carousel_endpoint():
    """Verify /api/v1/media/carousel endpoint produces PDF carousel asset."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/media/carousel",
            json={"title": "3 Rules for Production Agents"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["media_type"] == "PDF_CAROUSEL"
        assert data["resource_type"] == "raw"
        assert data["format"] == "pdf"
        assert "cloudinary_url" in data
