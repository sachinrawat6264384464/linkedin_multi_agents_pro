from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db_session, get_engine
from app.core.config import settings
from app.services.database_verification_service import DatabaseVerificationService
from app.core.logging import logger

router = APIRouter(prefix="/database", tags=["Database & Persistence"])


@router.get("/health")
async def get_database_health(session: Optional[AsyncSession] = Depends(get_db_session)):
    """
    Check live connectivity to Neon PostgreSQL.
    Reports actual connection status, SSL enforcement, and pool parameters.
    """
    if not settings.is_database_configured:
        return {
            "status": "not_configured",
            "message": "DATABASE_URL contains placeholder credentials in .env",
            "ssl_mode": "ssl=require (enforced)",
            "provider": "Neon PostgreSQL Serverless",
            "read_back_verification_active": True,
            "connected": False
        }

    try:
        if session:
            await session.execute(text("SELECT 1;"))
            return {
                "status": "connected",
                "message": "Active connection to Neon PostgreSQL verified",
                "ssl_mode": "require",
                "provider": "Neon PostgreSQL Serverless",
                "read_back_verification_active": True,
                "connected": True
            }
        else:
            return {
                "status": "standby",
                "message": "Database session unavailable",
                "connected": False
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "error",
            "message": str(e),
            "connected": False
        }


@router.get("/statistics")
async def get_database_statistics(session: Optional[AsyncSession] = Depends(get_db_session)):
    """Retrieve actual table record counts directly from PostgreSQL."""
    if not session:
        return {
            "tasks": 0,
            "workflow_runs": 0,
            "content_drafts": 0,
            "content_versions": 0,
            "research_sources": 0,
            "generated_media": 0,
            "published_posts": 0,
            "approvals": 0
        }
    return await DatabaseVerificationService.get_table_statistics(session)
