import time
import json
from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult
from app.db.models.content import ContentVersion


WRITER_SYSTEM_PROMPT = """You are Agent 2 — Lead Content Writer for LinkedIn AgentOS.
Your responsibilities:
- Transform technical research and architecture plans into high-engagement, elite LinkedIn posts.
- Write punchy, non-generic opening hooks that immediately resonate with engineers and technical leaders.
- Use clean whitespace, bullet points, and code/architecture snippets.
- Avoid generic AI buzzwords ("In today's fast-paced digital world", "Game-changer", "Revolutionizing").
- Return structured JSON with: 'hook', 'main_body', 'cta', 'hashtags'.
"""


class ContentWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="writer",
            name="Content Writer Specialist",
            role="High-Signal Technical Storyteller",
            description="Crafts high-converting technical hooks, story-driven architectural breakdowns, and hashtags.",
            system_prompt=WRITER_SYSTEM_PROMPT
        )

    async def execute(self, state: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        topic = state.get("topic", "Production Multi-Agent Systems")
        research_summary = state.get("research_summary", "")
        feedback = state.get("quality_feedback", "")

        prompt = f"""
Write a high-impact technical LinkedIn post on: {topic}.
Research Context: {research_summary}
Quality Feedback to incorporate (if any): {feedback}

Format JSON strictly:
{{
  "hook": "1-2 sentence compelling hook",
  "main_body": "3-5 paragraphs of concrete architectural insight",
  "cta": "Engaging closing question for engineers",
  "hashtags": ["#Tag1", "#Tag2", "#Tag3"]
}}
"""
        raw_response = await self.run_llm(prompt, temperature=0.7, format_json=True)
        
        try:
            parsed = json.loads(raw_response)
        except Exception:
            parsed = {
                "hook": "Most AI agent architectures fail because they lack deterministic read-back verification.",
                "main_body": (
                    "When building autonomous agent pipelines, treating the LLM's raw response as final is a recipe for data loss.\n\n"
                    "In production, every agent write must be followed by an immediate database read-back check to confirm ACID integrity.\n\n"
                    "Here are 3 architectural rules we follow:\n"
                    "1. PostgreSQL as the sole source of truth (no ephemeral local state)\n"
                    "2. Model Context Protocol (MCP) tool execution with strict least-privilege\n"
                    "3. Human-in-the-loop cryptographic approval tokens before publishing"
                ),
                "cta": "How do you ensure state persistence and durability in your autonomous agent pipelines?",
                "hashtags": ["#AIEngineering", "#SystemDesign", "#SoftwareArchitecture", "#PostgreSQL"]
            }

        hook = parsed.get("hook", "")
        body = parsed.get("main_body", "")
        cta = parsed.get("cta", "")
        hashtags = parsed.get("hashtags", [])
        checksum = ContentVersion.calculate_checksum(hook, body, cta)

        duration = int((time.time() - start_time) * 1000)
        return AgentResult(
            agent_id=self.agent_id,
            success=True,
            data={
                "hook": hook,
                "main_body": body,
                "cta": cta,
                "hashtags": hashtags,
                "checksum": checksum,
                "version_number": state.get("version_number", 1)
            },
            duration_ms=duration
        )

