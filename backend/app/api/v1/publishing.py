from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from app.services.linkedin_service import (
    linkedin_service,
    PublishSecurityError,
    LinkedInPublishError,
)
from app.core.logging import get_logger

logger = get_logger("publishing_api")

router = APIRouter(prefix="/publishing", tags=["Publishing & LinkedIn Integration"])


class PublishRequest(BaseModel):
    content: str = Field(..., description="Final text content to publish")
    approval_status: str = Field(..., description="Approval status (must be 'APPROVED')")
    approval_checksum: str = Field(..., description="Cryptographic SHA-256 fingerprint verified by human")
    author_urn: Optional[str] = Field(None, description="LinkedIn Person or Organization URN")
    media_urls: Optional[List[str]] = Field(default_factory=list, description="Associated image or document asset URLs")
    account_id: Optional[str] = Field(None, description="Saved account ID to use for credentials")


class OAuthCallbackRequest(BaseModel):
    code: str = Field(..., description="OAuth 2.0 authorization code received from LinkedIn callback")
    state: Optional[str] = Field(None, description="CSRF state token verification")


class ManualCopyRequest(BaseModel):
    title: str = Field(..., description="Internal post title")
    hook: str = Field(..., description="Opening attention hook")
    body: str = Field(..., description="Core post body")
    cta: str = Field(..., description="Call to action")
    hashtags: List[str] = Field(default_factory=list, description="Relevant hashtags")
    media_urls: List[str] = Field(default_factory=list, description="Attached media links")


@router.get("/status")
async def get_publishing_status() -> Dict[str, Any]:
    """Check LinkedIn integration status, configured mode, and connected accounts."""
    return linkedin_service.get_status()


@router.get("/oauth/login")
async def get_oauth_authorization_url(state: Optional[str] = None) -> Dict[str, str]:
    """Retrieve official LinkedIn OAuth 2.0 authorization redirect URL."""
    auth_url = linkedin_service.get_authorization_url(state=state)
    return {"authorization_url": auth_url}


@router.post("/oauth/callback")
async def handle_oauth_callback(payload: OAuthCallbackRequest) -> Dict[str, Any]:
    """Handle LinkedIn OAuth callback, exchange code, encrypt token and register account."""
    try:
        tokens = await linkedin_service.exchange_code_for_token(payload.code)
        access_token = tokens["access_token"]
        user_info = await linkedin_service.get_user_info(access_token)
        
        member_id = user_info.get("sub", "urn:li:person:unknown")
        display_name = user_info.get("name", "LinkedIn Member")
        expires_in = tokens.get("expires_in", 5184000)

        account = linkedin_service.store_account(
            member_id=member_id,
            display_name=display_name,
            access_token=access_token,
            expires_in=expires_in
        )
        return {
            "status": "connected",
            "account_id": account["id"],
            "member_id": member_id,
            "display_name": display_name,
            "expires_at": account["token_expires_at"]
        }
    except LinkedInPublishError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("OAuth callback processing error", extra={"error": str(e)})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"OAuth processing error: {str(e)}")


@router.post("/publish")
async def publish_content(payload: PublishRequest) -> Dict[str, Any]:
    """Publish verified post to LinkedIn with strict zero-trust cryptographic validation."""
    try:
        result = await linkedin_service.publish_post(
            content=payload.content,
            approval_status=payload.approval_status,
            approval_checksum=payload.approval_checksum,
            author_urn=payload.author_urn,
            media_urls=payload.media_urls,
            account_id=payload.account_id
        )
        return result
    except PublishSecurityError as e:
        logger.warning("Zero-trust publishing check rejected post", extra={"error": str(e)})
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except LinkedInPublishError as e:
        logger.error("LinkedIn API publishing failed", extra={"error": str(e)})
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
    except Exception as e:
        logger.error("Unexpected publishing error", extra={"error": str(e)})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Publishing failed: {str(e)}")


@router.get("/history")
async def get_publishing_history() -> List[Dict[str, Any]]:
    """Retrieve full audit log of published and staged LinkedIn posts."""
    return linkedin_service.get_publishing_history()


@router.post("/manual-copy")
async def format_for_manual_copy(payload: ManualCopyRequest) -> Dict[str, Any]:
    """Format an approved draft into an instant 1-click clipboard payload for LinkedIn web publishing."""
    tags_formatted = " ".join(f"#{t.strip('#')}" for t in payload.hashtags if t.strip())
    formatted_post = f"{payload.hook}\n\n{payload.body}\n\n{payload.cta}\n\n{tags_formatted}".strip()
    
    return {
        "formatted_text": formatted_post,
        "character_count": len(formatted_post),
        "linkedin_limit": 3000,
        "is_within_limit": len(formatted_post) <= 3000,
        "media_count": len(payload.media_urls),
        "media_urls": payload.media_urls,
        "ready_for_web_paste": True
    }

