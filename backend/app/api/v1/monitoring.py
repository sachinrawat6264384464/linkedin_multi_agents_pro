from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from app.monitoring.watchdog import watchdog
from app.core.config import settings

router = APIRouter(prefix="/monitoring", tags=["System Monitoring & Health Watchdog"])


class RetryRequest(BaseModel):
    task_id: str = Field(..., description="Stalled or failed task ID")
    agent_id: str = Field(..., description="Target agent to rerun")
    attempt: int = Field(1, description="Current retry attempt number")


class SwitchModelRequest(BaseModel):
    model_tag: str = Field(..., description="Ollama model tag to switch to, e.g. 'qwen2.5:7b-instruct'")
    context_window: int = Field(4096, description="Maximum context window tokens")
    temperature: float = Field(0.7, description="Generation temperature")


@router.get("/overview")
async def get_monitoring_overview() -> Dict[str, Any]:
    """Retrieve overall system health score, uptime, and high-level agent metrics."""
    return watchdog.get_system_overview()


@router.get("/agents")
async def get_agent_heartbeats() -> List[Dict[str, Any]]:
    """Retrieve live heartbeats, status, latencies, and invocation counts for all 8 agents."""
    return watchdog.get_agents_telemetry()


@router.get("/logs")
async def get_system_logs(
    level: Optional[str] = Query("ALL", description="Filter logs: ALL, INFO, WARN, ERROR"),
    limit: int = Query(100, ge=1, le=250, description="Maximum number of log entries to return")
) -> List[Dict[str, Any]]:
    """Retrieve fast in-memory ring-buffered system audit logs for the live console."""
    return watchdog.get_logs(level=level, limit=limit)


@router.post("/scan-stalled")
async def scan_for_stalled_tasks() -> List[Dict[str, Any]]:
    """Force an immediate watchdog sweep for stalled or unresponsive tasks."""
    return watchdog.scan_for_stalled_tasks()


@router.post("/retry")
async def trigger_task_retry(payload: RetryRequest) -> Dict[str, Any]:
    """Manually or automatically schedule an exponential backoff retry for a task."""
    result = watchdog.schedule_retry(
        task_id=payload.task_id,
        agent_id=payload.agent_id,
        attempt=payload.attempt
    )
    return result


@router.get("/metrics")
async def get_system_metrics() -> Dict[str, Any]:
    """Retrieve resource telemetry, latencies, and Neon connection health."""
    overview = watchdog.get_system_overview()
    agents = watchdog.get_agents_telemetry()
    avg_latency = (
        sum(a["avg_latency_ms"] for a in agents) / len(agents) if agents else 0.0
    )

    return {
        "overview": overview,
        "avg_agent_latency_ms": round(avg_latency, 2),
        "database_engine": "Neon PostgreSQL (AsyncPG)",
        "database_pool": {
            "size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
            "timeout_seconds": settings.DB_POOL_TIMEOUT,
            "ssl_mode": "require (verified)"
        },
        "media_storage_engine": "Cloudinary (Direct Streaming)",
        "model_execution": {
            "provider": "Ollama Local",
            "active_model": settings.OLLAMA_MODEL,
            "base_url": settings.OLLAMA_BASE_URL,
            "ram_tier": "8GB RAM Constrained (Quantized Shared Context)"
        }
    }


@router.get("/models/status")
async def get_model_status() -> Dict[str, Any]:
    """Inspect active local Ollama model execution settings and RAM optimization status."""
    return {
        "active_model": settings.OLLAMA_MODEL,
        "base_url": settings.OLLAMA_BASE_URL,
        "timeout": settings.OLLAMA_TIMEOUT,
        "optimization_profile": "8GB RAM Efficient Single-Model Concurrency",
        "supported_models": [
            {"tag": "qwen2.5:7b-instruct", "recommended": True, "vram_mb": 4600},
            {"tag": "qwen2.5:3b-instruct", "recommended": False, "vram_mb": 2200},
            {"tag": "llama3.2:3b", "recommended": False, "vram_mb": 2400},
            {"tag": "mistral:7b-instruct", "recommended": False, "vram_mb": 4800}
        ]
    }


@router.post("/models/switch")
async def switch_model(payload: SwitchModelRequest) -> Dict[str, Any]:
    """Switch the active local Ollama model tag dynamically."""
    settings.OLLAMA_MODEL = payload.model_tag
    watchdog.log_event(
        "INFO",
        "model_manager",
        f"Active LLM switched to {payload.model_tag} (Context: {payload.context_window} tokens)."
    )
    return {
        "status": "switched",
        "new_model": settings.OLLAMA_MODEL,
        "context_window": payload.context_window,
        "temperature": payload.temperature
    }

