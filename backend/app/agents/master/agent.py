import time
from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult


MASTER_SYSTEM_PROMPT = """You are Agent 0 — Master Orchestrator for LinkedIn AgentOS.
Your responsibilities:
- Receive high-level content tasks and decompose them into actionable specialist assignments.
- Track DAG dependencies and coordinate handoffs across Research, Writer, Visual Designer, Quality, Publishing, Database, and Monitoring.
- NEVER perform specialist tasks (like writing raw copy or rendering SVGs) yourself.
- Always enforce human-in-the-loop task approval and final publishing approval gates.
"""


class MasterOrchestrator(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="master",
            name="Master Orchestrator",
            role="Autonomous Workflow Coordinator",
            description="Coordinates DAG execution, manages task dependencies, handles conditional routing and approvals.",
            system_prompt=MASTER_SYSTEM_PROMPT
        )

    async def execute(self, state: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        topic = state.get("topic", "AI Engineering & Autonomous Systems")
        category = state.get("category", "AI Engineering")

        plan = {
            "workflow_id": state.get("workflow_id", "wf-default"),
            "stage": "TASK_INITIATED",
            "assigned_specialists": [
                "research", "writer", "designer", "quality", "database", "publisher", "monitoring"
            ],
            "topic": topic,
            "category": category,
            "requires_task_approval": True,
            "requires_publishing_approval": True
        }

        duration = int((time.time() - start_time) * 1000)
        return AgentResult(
            agent_id=self.agent_id,
            success=True,
            data={"orchestration_plan": plan},
            duration_ms=duration
        )
