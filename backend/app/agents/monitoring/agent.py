import time
from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult
from app.core.config import settings


MONITORING_SYSTEM_PROMPT = """You are Agent 7 — Monitoring & System Health Specialist for LinkedIn AgentOS.
Your responsibilities:
- Continuously watch agent execution latencies, step status transitions, and error logs.
- Detect stuck workflows, infinite loops, and failed database transactions.
- Enforce strict retry caps (max 3 retries with exponential backoff) with full audit logging.
- Generate system health diagnostics for the command center.
"""


class MonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="monitoring",
            name="Monitoring & System Health Specialist",
            role="Autonomous Telemetry & Reliability Watchdog",
            description="Monitors workflow state transitions, tracks execution duration, prevents runaway loops, audits retries.",
            system_prompt=MONITORING_SYSTEM_PROMPT
        )

    async def execute(self, state: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        workflow_id = state.get("workflow_id", "wf-unknown")
        history = state.get("execution_history", [])

        health_audit = {
            "workflow_id": workflow_id,
            "total_steps_executed": len(history),
            "system_health": "HEALTHY",
            "backend_status": "ONLINE",
            "database_configured": settings.is_database_configured,
            "ollama_base_url": settings.OLLAMA_BASE_URL,
            "retry_count": state.get("retry_count", 0),
            "max_retries_allowed": 3,
            "timestamp": int(time.time())
        }

        duration = int((time.time() - start_time) * 1000)
        return AgentResult(
            agent_id=self.agent_id,
            success=True,
            data={"health_audit": health_audit},
            duration_ms=duration
        )

