from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.database import router as database_router
from app.api.v1.agents import router as agents_router
from app.api.v1.workflows import router as workflows_router
from app.api.v1.mcp import router as mcp_router
from app.api.v1.research import router as research_router
from app.api.v1.content import router as content_router
from app.api.v1.media import router as media_router
from app.api.v1.approvals import router as approvals_router
from app.api.v1.publishing import router as publishing_router
from app.api.v1.monitoring import router as monitoring_router

api_v1_router = APIRouter(prefix="/api/v1")

# Include core sub-routers
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(database_router)
api_v1_router.include_router(agents_router)
api_v1_router.include_router(workflows_router)
api_v1_router.include_router(mcp_router)
api_v1_router.include_router(research_router)
api_v1_router.include_router(content_router)
api_v1_router.include_router(media_router)
api_v1_router.include_router(approvals_router)
api_v1_router.include_router(publishing_router)
api_v1_router.include_router(monitoring_router)
