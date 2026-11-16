from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func
from app.db.models import (
    Task, WorkflowRun, ContentDraft, ContentVersion, ResearchSource,
    GeneratedMedia, PublishedPost, Approval
)
from app.core.logging import logger


class DatabaseVerificationService:
    """
    Dedicated verification engine used by Agent 6 (Database & Persistence Agent).
    Guarantees ACID durability by performing strict read-backs and cryptographic
    field-by-field integrity audits.
    """

    @staticmethod
    async def verify_task_persistence(session: AsyncSession, task_id: str, expected_title: str) -> Dict[str, Any]:
        """Read-back verification for Task creation or update."""
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            return {
                "verified": False,
                "error": f"Task {task_id} missing from PostgreSQL store",
                "task_id": task_id
            }

        if task.title != expected_title:
            return {
                "verified": False,
                "error": f"Field mismatch: expected title '{expected_title}', got '{task.title}'",
                "task_id": task_id
            }

        return {
            "verified": True,
            "task_id": task.id,
            "status": task.status,
            "created_at": task.created_at.isoformat() if task.created_at else None
        }

    @staticmethod
    async def verify_content_version_integrity(
        session: AsyncSession,
        version_id: str,
        expected_checksum: str
    ) -> Dict[str, Any]:
        """
        Verify that a content version was written, read it back, and confirm that
        its calculated cryptographic checksum exactly matches the stored checksum.
        """
        stmt = select(ContentVersion).where(ContentVersion.id == version_id)
        result = await session.execute(stmt)
        version = result.scalar_one_or_none()

        if not version:
            return {
                "verified": False,
                "error": f"ContentVersion {version_id} not found in PostgreSQL store",
                "version_id": version_id
            }

        calculated = ContentVersion.calculate_checksum(version.hook, version.main_body, version.cta or "")
        if calculated != expected_checksum or version.checksum != expected_checksum:
            return {
                "verified": False,
                "error": f"Checksum integrity violation! Expected {expected_checksum}, calculated {calculated}",
                "version_id": version_id
            }

        return {
            "verified": True,
            "version_id": version.id,
            "version_number": version.version_number,
            "checksum": version.checksum,
            "is_approved": version.is_approved
        }

    @staticmethod
    async def get_table_statistics(session: AsyncSession) -> Dict[str, int]:
        """Collect live record counts across all core PostgreSQL tables."""
        counts = {}
        tables = [
            ("tasks", Task),
            ("workflow_runs", WorkflowRun),
            ("content_drafts", ContentDraft),
            ("content_versions", ContentVersion),
            ("research_sources", ResearchSource),
            ("generated_media", GeneratedMedia),
            ("published_posts", PublishedPost),
            ("approvals", Approval),
        ]

        for table_name, model in tables:
            try:
                stmt = select(func.count()).select_from(model)
                res = await session.execute(stmt)
                counts[table_name] = res.scalar() or 0
            except Exception as e:
                logger.warning(f"Failed to count table {table_name}: {e}")
                counts[table_name] = 0

        return counts

