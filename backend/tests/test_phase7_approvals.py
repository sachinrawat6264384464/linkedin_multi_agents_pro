import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.services.approval_service import ApprovalService


def test_approval_service_checksum_validation():
    """Verify approval service validates matching checksums and rejects drifted hashes."""
    checksum_valid = "a1b2c3d4e5f60000111122223333444455556666777788889999aaaabbbbcccc"
    checksum_drifted = "ffffffffffff0000111122223333444455556666777788889999aaaabbbbcccc"

    ticket = ApprovalService.request_approval(
        task_id="task-test-7",
        content_version_id="ver-test-7",
        version_checksum=checksum_valid,
        approval_type="FINAL_PUBLISH",
        title="Zero Trust Verification Test"
    )

    # Before signing -> False
    assert ApprovalService.is_publishing_authorized(checksum_valid) is False

    # Sign ticket
    ApprovalService.sign_approval(ticket["id"], status="APPROVED", reviewer_notes="Approved by Lead Architect")

    # After signing valid checksum -> True
    assert ApprovalService.is_publishing_authorized(checksum_valid) is True

    # Drifted checksum -> False (Security check prevents modified drafts from publishing)
    assert ApprovalService.is_publishing_authorized(checksum_drifted) is False


@pytest.mark.asyncio
async def test_pending_approvals_api_endpoint():
    """Verify pending approvals list endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/approvals/pending")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "version_checksum" in data[0]


@pytest.mark.asyncio
async def test_sign_approval_api_endpoint():
    """Verify signing an approval ticket through REST API."""
    ticket = ApprovalService.request_approval(
        task_id="task-api-test",
        content_version_id="ver-api-test",
        version_checksum="checksum_api_12345",
        approval_type="FINAL_PUBLISH"
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"/api/v1/approvals/{ticket['id']}/sign",
            json={"decision": "APPROVED", "reviewer_notes": "Ready for LinkedIn broadcast"}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert result["ticket"]["status"] == "APPROVED"
        assert result["ticket"]["reviewer_notes"] == "Ready for LinkedIn broadcast"
