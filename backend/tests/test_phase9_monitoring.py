import pytest
import time
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.monitoring.watchdog import watchdog


@pytest.mark.asyncio
async def test_watchdog_agent_registration_and_heartbeats():
    """Verify all 8 agents are registered and track latency correctly."""
    assert len(watchdog.agents) == 8
    assert "agent_0" in watchdog.agents
    assert "agent_7" in watchdog.agents

    # Test agent record_start and record_success
    agent = watchdog.agents["agent_2"]
    agent.record_start("task_test_101")
    assert agent.status == "RUNNING"
    assert agent.current_task_id == "task_test_101"

    agent.record_success(duration_ms=450.0)
    assert agent.status == "IDLE"
    assert agent.successful_runs >= 1
    assert agent.avg_latency_ms == 450.0


@pytest.mark.asyncio
async def test_stalled_task_detection_and_retry_queue():
    """Verify watchdog detects unresponsive tasks and enforces retry backoff."""
    agent = watchdog.agents["agent_1"]
    agent.record_start("task_stalled_999")
    # Simulate artificial delay beyond stalled threshold
    agent.task_start_time = time.time() - 200

    stalled = watchdog.scan_for_stalled_tasks()
    assert any(s["task_id"] == "task_stalled_999" for s in stalled)
    assert agent.status == "STALLED"

    # Schedule retry #1
    retry_1 = watchdog.schedule_retry("task_stalled_999", "agent_1", attempt=1)
    assert retry_1["status"] == "QUEUED"
    assert retry_1["backoff_seconds"] == 2

    # Schedule retry #4 (exceeds cap of 3)
    retry_4 = watchdog.schedule_retry("task_stalled_999", "agent_1", attempt=4)
    assert retry_4["status"] == "ABANDONED"


@pytest.mark.asyncio
async def test_system_overview_and_metrics_endpoints():
    """Verify monitoring overview and resource metrics endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        overview_resp = await client.get("/api/v1/monitoring/overview")
        assert overview_resp.status_code == 200
        overview = overview_resp.json()
        assert overview["total_agents"] == 8
        assert "health_score" in overview
        assert overview["memory_optimization_mode"] == "8GB_HOST_QUANTIZED_SINGLE_MODEL"

        metrics_resp = await client.get("/api/v1/monitoring/metrics")
        assert metrics_resp.status_code == 200
        metrics = metrics_resp.json()
        assert "avg_agent_latency_ms" in metrics
        assert metrics["database_pool"]["ssl_mode"] == "require (verified)"
        assert "Ollama Local" in metrics["model_execution"]["provider"]


@pytest.mark.asyncio
async def test_system_logs_buffer_and_filtering():
    """Verify log ring buffer captures and filters log levels correctly."""
    watchdog.log_event("INFO", "test_source", "General informational telemetry log.")
    watchdog.log_event("ERROR", "test_source", "Simulated critical execution fault.")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Filter ERROR
        err_resp = await client.get("/api/v1/monitoring/logs?level=ERROR")
        assert err_resp.status_code == 200
        error_logs = err_resp.json()
        assert all(entry["level"] == "ERROR" for entry in error_logs)
        assert any("Simulated critical execution fault." in entry["message"] for entry in error_logs)

        # Filter ALL
        all_resp = await client.get("/api/v1/monitoring/logs?level=ALL")
        assert all_resp.status_code == 200
        assert len(all_resp.json()) >= 2


@pytest.mark.asyncio
async def test_model_status_and_switch_endpoint():
    """Verify model status endpoint and hot model switching."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        status_resp = await client.get("/api/v1/monitoring/models/status")
        assert status_resp.status_code == 200
        status_data = status_resp.json()
        assert "active_model" in status_data
        assert len(status_data["supported_models"]) >= 2

        # Switch model
        switch_resp = await client.post(
            "/api/v1/monitoring/models/switch",
            json={
                "model_tag": "qwen2.5:7b-instruct",
                "context_window": 8192,
                "temperature": 0.5
            }
        )
        assert switch_resp.status_code == 200
        assert switch_resp.json()["new_model"] == "qwen2.5:7b-instruct"
