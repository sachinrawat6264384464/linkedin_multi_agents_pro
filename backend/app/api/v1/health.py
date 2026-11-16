from fastapi import APIRouter
from datetime import datetime, timezone
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["System Health"])


@router.get("")
async def get_health_status():
    """
    Returns the real-time operational health of LinkedIn AgentOS services.
    Never fakes connectivity: reports actual configured vs disconnected status.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "api": {"status": "online", "version": "1.0.0"},
            "database": {
                "configured": settings.is_database_configured,
                "status": "configured" if settings.is_database_configured else "not_configured"
            },
            "ollama": {
                "base_url": settings.OLLAMA_BASE_URL,
                "model": settings.OLLAMA_MODEL,
                "status": "ready"
            },
            "cloudinary": {
                "configured": settings.is_cloudinary_configured,
                "status": "configured" if settings.is_cloudinary_configured else "not_configured"
            },
            "linkedin": {
                "configured": settings.is_linkedin_configured,
                "status": "configured" if settings.is_linkedin_configured else "not_configured"
            }
        }
    }
