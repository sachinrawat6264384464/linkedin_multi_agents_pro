import uuid
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.services.media_service import MediaService

router = APIRouter(prefix="/media", tags=["Media Studio"])


class DiagramRequest(BaseModel):
    topic: str
    flow_type: Optional[str] = "architecture"


class CarouselRequest(BaseModel):
    title: str
    slides: List[Dict[str, Any]] = Field(default_factory=list)


# Staged assets store for active session
_SAVED_MEDIA_ASSETS: List[Dict[str, Any]] = []


@router.post("/diagram")
async def create_diagram(request: DiagramRequest):
    """Generate architectural Mermaid diagram and register media asset."""
    syntax = MediaService.generate_mermaid_diagram(request.topic, request.flow_type or "architecture")
    
    asset = {
        "id": f"dia-{uuid.uuid4().hex[:8]}",
        "media_type": "DIAGRAM",
        "title": f"Architecture: {request.topic}",
        "syntax": syntax,
        "format": "mermaid",
        "cloudinary_url": "https://res.cloudinary.com/agentos/image/upload/agentos/diagrams/arch_flow.png",
        "public_id": "agentos/diagrams/arch_flow",
        "resource_type": "image"
    }
    _SAVED_MEDIA_ASSETS.append(asset)
    return asset


@router.post("/carousel")
async def create_carousel(request: CarouselRequest):
    """
    Generate LinkedIn multi-slide PDF carousel and stream to Cloudinary with resource_type='raw'.
    """
    slides = request.slides
    if not slides:
        slides = [
            {"title": "01: The Problem with In-Memory State", "points": ["LLM agent crashes lose in-flight steps", "Restarting from scratch wastes token budgets", "PostgreSQL checkpoints make DAGs resumable"]},
            {"title": "02: Mandatory Read-Back Verification", "points": ["Never trust execution success messages blindly", "Query database record by ID immediately", "Verify cryptographic content checksum"]},
            {"title": "03: The Human-in-the-Loop Gate", "points": ["Zero unapproved posts published", "Approval signatures tied to immutable version hash", "Complete audit trail for compliance"]}
        ]

    pdf_bytes = MediaService.generate_pdf_carousel_bytes(slides)
    
    # Upload to Cloudinary with resource_type="raw" as required for PDFs
    upload_res = await MediaService.upload_asset_to_cloudinary(
        file_bytes=pdf_bytes,
        filename="linkedin_carousel",
        resource_type="raw",
        folder="agentos/carousels"
    )

    asset = {
        "id": f"car-{uuid.uuid4().hex[:8]}",
        "media_type": "PDF_CAROUSEL",
        "title": request.title,
        "slides_count": len(slides),
        "cloudinary_url": upload_res.get("secure_url"),
        "public_id": upload_res.get("public_id"),
        "resource_type": "raw",
        "format": "pdf"
    }
    _SAVED_MEDIA_ASSETS.append(asset)
    return asset


@router.get("/assets")
async def list_media_assets():
    """Retrieve all generated diagram and carousel assets."""
    return _SAVED_MEDIA_ASSETS
