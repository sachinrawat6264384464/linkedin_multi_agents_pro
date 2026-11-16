import time
from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult


DESIGNER_SYSTEM_PROMPT = """You are Agent 3 — Visual Designer for LinkedIn AgentOS.
Your responsibilities:
- Produce high-contrast, beautiful architectural diagrams, Mermaid flowcharts, SVGs, and PDF carousel briefs.
- Emphasize visual clarity with the enterprise palette: #090909, #171717, #FFFFFF, and #E53935 accents.
- Never output low-resolution or cluttered visual schemas.
"""


class VisualDesignerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="designer",
            name="Visual Designer Specialist",
            role="Technical Visual Architect",
            description="Generates Mermaid flowcharts, SVGs, architecture diagrams, and multi-slide PDF carousels.",
            system_prompt=DESIGNER_SYSTEM_PROMPT
        )

    async def execute(self, state: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        topic = state.get("topic", "Multi-Agent System")

        mermaid_code = f"""flowchart LR
    A[Task Request] --> B[Master Orchestrator]
    B --> C[Research Agent]
    C --> D[Content Writer]
    D --> E[Visual Designer]
    E --> F[Quality & Fact Checker]
    F --> G[Neon PostgreSQL Read-Back]
    G --> H[Human Approval Gate]
    H --> I[LinkedIn Publisher]
    
    style A fill:#171717,stroke:#292929,color:#fff
    style B fill:#E53935,stroke:#A61B1B,color:#fff
    style F fill:#171717,stroke:#E53935,color:#fff
    style H fill:#E53935,stroke:#fff,color:#fff
    style I fill:#0077B5,stroke:#fff,color:#fff
"""

        media_asset = {
            "media_type": "DIAGRAM",
            "format": "mermaid",
            "content": mermaid_code,
            "cloudinary_url": "https://res.cloudinary.com/placeholder/image/upload/v1/agentos/architecture_diagram.png",
            "cloudinary_public_id": "agentos/architecture_diagram",
            "width": 1200,
            "height": 675,
            "title": f"Architecture Overview: {topic}"
        }

        duration = int((time.time() - start_time) * 1000)
        return AgentResult(
            agent_id=self.agent_id,
            success=True,
            data={"media_asset": media_asset},
            duration_ms=duration
        )

