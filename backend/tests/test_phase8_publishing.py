import pytest
import hashlib
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.linkedin_service import linkedin_service, PublishSecurityError


@pytest.mark.asyncio
async def test_oauth_authorization_url_generation():
    """Verify LinkedIn OAuth 2.0 URL is properly structured."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/publishing/oauth/login")
        assert response.status_code == 200
        data = response.json()
        assert "authorization_url" in data
        assert "https://www.linkedin.com/oauth/v2/authorization" in data["authorization_url"]
        assert "response_type=code" in data["authorization_url"]
        assert "scope=" in data["authorization_url"]


@pytest.mark.asyncio
async def test_zero_trust_rejection_unapproved_content():
    """Verify that unapproved content is rejected with 403 Forbidden."""
    content = "Breaking: Distributed Consensus in Multi-Agent Systems"
    content_hash = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/publishing/publish",
            json={
                "content": content,
                "approval_status": "PENDING",  # Not APPROVED
                "approval_checksum": content_hash,
            }
        )
        assert response.status_code == 403
        assert "Zero-trust security violation" in response.json()["detail"]


@pytest.mark.asyncio
async def test_zero_trust_rejection_checksum_mismatch():
    """Verify that approved status with altered content is rejected immediately."""
    original_content = "Original verified content text."
    altered_content = "Altered malicious content text injection!"
    original_hash = hashlib.sha256(original_content.strip().encode("utf-8")).hexdigest()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/publishing/publish",
            json={
                "content": altered_content,
                "approval_status": "APPROVED",
                "approval_checksum": original_hash,  # Hash of original, content is altered
            }
        )
        assert response.status_code == 403
        assert "checksum drift detected" in response.json()["detail"]


@pytest.mark.asyncio
async def test_successful_publish_and_history():
    """Verify that cryptographically matching approved content publishes successfully."""
    content = "Architecting resilient systems requires automated state machine checkpoints."
    content_hash = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Publish
        response = await client.post(
            "/api/v1/publishing/publish",
            json={
                "content": content,
                "approval_status": "APPROVED",
                "approval_checksum": content_hash,
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "linkedin_urn" in data
        assert data["publishing_status"] in ("PUBLISHED", "STAGED_MANUAL")
        assert "post_url" in data

        # Verify history includes the record
        hist_resp = await client.get("/api/v1/publishing/history")
        assert hist_resp.status_code == 200
        history = hist_resp.json()
        assert len(history) >= 1


@pytest.mark.asyncio
async def test_manual_copy_formatter_endpoint():
    """Verify formatting helper generates accurate clipboard payloads."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "title": "System Resilience",
            "hook": "Why do microservices fail at 2 AM?",
            "body": "Because cascading timeouts overwhelm connection pools without circuit breakers.",
            "cta": "How does your team handle cascading retries?",
            "hashtags": ["Architecture", "DevOps"],
            "media_urls": ["https://res.cloudinary.com/demo/image/upload/diag.png"]
        }
        response = await client.post("/api/v1/publishing/manual-copy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ready_for_web_paste"] is True
        assert data["is_within_limit"] is True
        assert "#Architecture" in data["formatted_text"]
        assert data["media_count"] == 1

