import uuid
import hashlib
from typing import Dict, Any, List, Optional
from app.db.models.content import ContentVersion
from app.agents import get_agent


class ContentService:
    """
    Core domain service managing LinkedIn content drafts, immutable versions,
    quality score auditing, and variation generation.
    """

    @staticmethod
    def calculate_checksum(hook: str, main_body: str, cta: str = "") -> str:
        """Calculate deterministic SHA-256 fingerprint."""
        return ContentVersion.calculate_checksum(hook, main_body, cta)

    @staticmethod
    async def generate_draft_variations(topic: str, research_context: str = "") -> List[Dict[str, Any]]:
        """
        Generate multiple high-converting variations of a LinkedIn technical post.
        """
        writer = get_agent("writer")
        variations = []

        # Style 1: The Counterintuitive Architectural Truth
        state_var1 = {
            "topic": topic,
            "research_summary": research_context,
            "quality_feedback": "Focus on common engineering misconceptions."
        }
        res1 = await writer.execute(state_var1)
        data1 = res1.data
        variations.append({
            "variation_label": "The Architectural Myth-Buster",
            "hook": data1.get("hook"),
            "main_body": data1.get("main_body"),
            "cta": data1.get("cta"),
            "hashtags": data1.get("hashtags"),
            "checksum": data1.get("checksum")
        })

        # Style 2: The Practical Blueprint & Step-by-Step Lesson
        state_var2 = {
            "topic": topic,
            "research_summary": research_context,
            "quality_feedback": "Provide a concrete 3-step technical implementation guide."
        }
        res2 = await writer.execute(state_var2)
        data2 = res2.data
        variations.append({
            "variation_label": "The Production Implementation Guide",
            "hook": "Here is the exact production architecture we used to scale autonomous agents without state loss.",
            "main_body": data2.get("main_body"),
            "cta": data2.get("cta"),
            "hashtags": data2.get("hashtags"),
            "checksum": ContentVersion.calculate_checksum(
                "Here is the exact production architecture we used to scale autonomous agents without state loss.",
                data2.get("main_body", ""),
                data2.get("cta", "")
            )
        })

        return variations
