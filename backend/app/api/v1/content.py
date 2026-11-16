import uuid
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.services.content_service import ContentService
from app.agents import get_agent

router = APIRouter(prefix="/content", tags=["Content Studio"])


class GenerateContentRequest(BaseModel):
    topic: str
    category: Optional[str] = "AI Engineering"
    research_summary: Optional[str] = ""


class SaveDraftRequest(BaseModel):
    title: str
    topic: str
    category: str
    hook: str
    main_body: str
    cta: Optional[str] = ""
    hashtags: List[str] = Field(default_factory=list)


# In-memory storage for active sessions / dev mode
_SAVED_DRAFTS: List[Dict[str, Any]] = []


@router.post("/generate")
async def generate_content_variations(request: GenerateContentRequest):
    """Generate multiple high-converting variations of a LinkedIn post."""
    variations = await ContentService.generate_draft_variations(
        topic=request.topic,
        research_context=request.research_summary
    )
    return {
        "topic": request.topic,
        "count": len(variations),
        "variations": variations
    }


@router.post("/drafts")
async def save_content_draft(request: SaveDraftRequest):
    """
    Save content draft, calculate deterministic SHA-256 fingerprint,
    and create new immutable version record.
    """
    checksum = ContentService.calculate_checksum(request.hook, request.main_body, request.cta or "")
    draft_id = str(uuid.uuid4())
    version_id = str(uuid.uuid4())

    draft_record = {
        "id": draft_id,
        "title": request.title,
        "topic": request.topic,
        "category": request.category,
        "current_version": {
            "id": version_id,
            "version_number": 1,
            "hook": request.hook,
            "main_body": request.main_body,
            "cta": request.cta,
            "hashtags": request.hashtags,
            "checksum": checksum,
            "is_approved": False
        }
    }
    _SAVED_DRAFTS.append(draft_record)

    return {
        "status": "saved",
        "draft_id": draft_id,
        "version_id": version_id,
        "checksum": checksum
    }


@router.get("/drafts")
async def list_content_drafts():
    """Retrieve all saved content drafts and current versions."""
    return _SAVED_DRAFTS

