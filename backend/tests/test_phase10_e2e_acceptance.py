import pytest
import hashlib
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.graph.builder import build_workflow_graph
from app.services.approval_service import ApprovalService
from app.services.linkedin_service import linkedin_service
from app.monitoring.watchdog import watchdog


@pytest.mark.asyncio
async def test_e2e_full_agent_workflow_execution():
    """Execute end-to-end LangGraph state machine from research to approval hold."""
    graph = build_workflow_graph()

    initial_state = {
        "task_id": "task_e2e_001",
        "workflow_id": "wf_e2e_001",
        "topic": "Event-Driven Microservices with Kafka and Debezium",
        "category": "distributed-systems",
        "target_audience": "Senior Architects & Platform Engineers",
        "human_approved": False,
        "quality_loop_count": 0,
        "version_number": 1,
        "execution_history": []
    }

    config = {"configurable": {"thread_id": "thread_e2e_001"}}

    # Execute workflow DAG
    final_state = await graph.ainvoke(initial_state, config=config)

    # Assertions across the pipeline stages
    assert final_state.get("research_summary") is not None
    assert len(final_state.get("research_sources", [])) >= 1

    assert final_state.get("hook") is not None
    assert final_state.get("main_body") is not None
    assert final_state.get("cta") is not None

    assert final_state.get("quality_approved") is True
    assert final_state.get("quality_scorecard") is not None

    assert final_state.get("media_asset") is not None
    assert final_state.get("persisted") is True
    assert final_state.get("checksum") is not None

    # Zero-trust verification: Without human_approved=True, publishing does NOT execute
    assert final_state.get("published") is not True


@pytest.mark.asyncio
async def test_e2e_approval_to_publishing_cycle():
    """Verify human approval creation, cryptographic signing, and publishing execution."""
    content = "Event-driven architecture with outbox patterns guarantees exactly-once delivery."
    content_hash = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    # 1. Create approval ticket
    ticket = ApprovalService.request_approval(
        task_id="task_e2e_test",
        content_version_id="ver_e2e_test",
        version_checksum=content_hash,
        approval_type="FINAL_PUBLISH",
        title="Event Driven Architecture"
    )
    assert ticket["status"] == "PENDING"
    assert ticket["version_checksum"] == content_hash

    # 2. Human operator signs ticket
    signed = ApprovalService.sign_approval(
        approval_id=ticket["id"],
        status="APPROVED",
        reviewer_notes="Verified technical accuracy and diagrams."
    )
    assert signed["status"] == "APPROVED"
    assert ApprovalService.is_publishing_authorized(content_hash) is True

    # 3. Publish post with zero-trust validation
    pub_result = await linkedin_service.publish_post(
        content=content,
        approval_status=signed["status"],
        approval_checksum=signed["version_checksum"]
    )
    assert pub_result["publishing_status"] in ("PUBLISHED", "STAGED_MANUAL")
    assert "linkedin_urn" in pub_result


@pytest.mark.asyncio
async def test_e2e_system_health_and_watchdog_acceptance():
    """Verify sentinel watchdog reports nominal status and logs across all subsystems."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Check health endpoint
        health_resp = await client.get("/api/v1/health")
        assert health_resp.status_code == 200
        health = health_resp.json()
        assert health["status"] == "healthy"
        assert health["services"]["api"]["version"] == "1.0.0"

        # Check monitoring overview
        mon_resp = await client.get("/api/v1/monitoring/overview")
        assert mon_resp.status_code == 200
        overview = mon_resp.json()
        assert overview["total_agents"] == 8
        assert overview["active_agents"] == 8

        # Check database health & read-back verification status
        db_resp = await client.get("/api/v1/database/health")
        assert db_resp.status_code == 200
        db_audit = db_resp.json()
        assert db_audit["read_back_verification_active"] is True
