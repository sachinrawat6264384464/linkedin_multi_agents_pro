import uuid
import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
import httpx
from app.core.config import settings
from app.core.encryption import encrypt_secret, decrypt_secret
from app.core.logging import get_logger

logger = get_logger("linkedin_service")


class PublishSecurityError(Exception):
    """Raised when an unapproved draft or altered checksum attempts to publish."""
    pass


class LinkedInPublishError(Exception):
    """Raised when LinkedIn API rejects or fails a publishing request."""
    pass


class LinkedInService:
    """Enterprise LinkedIn OAuth 2.0 and UGC Publishing Service.
    
    Enforces:
    1. Zero-trust human approval validation before sending any data to LinkedIn.
    2. Fernet symmetric encryption of OAuth access tokens at rest.
    3. Graceful disconnected mode and manual copy-paste fallback.
    4. Audit trail logging of all publication attempts and API responses.
    """

    def __init__(self):
        self._mock_accounts: Dict[str, Dict[str, Any]] = {}
        self._mock_published_posts: List[Dict[str, Any]] = []

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Construct the LinkedIn OAuth 2.0 authorization URL."""
        state = state or secrets.token_urlsafe(16)
        client_id = settings.LINKEDIN_CLIENT_ID or "placeholder_client_id"
        redirect_uri = settings.LINKEDIN_REDIRECT_URI
        scope = "w_member_social%20openid%20profile%20email"
        
        auth_url = (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&scope={scope}"
        )
        logger.info("Generated LinkedIn authorization URL", extra={"state": state})
        return auth_url

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange the OAuth authorization code for access token."""
        if not settings.is_linkedin_configured:
            logger.warning("LinkedIn not configured; returning mock token exchange response")
            return {
                "access_token": f"mock_li_at_{uuid.uuid4().hex[:12]}",
                "expires_in": 5184000,
                "scope": "w_member_social openid profile email"
            }

        url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, data=data, headers=headers)
            if response.status_code != 200:
                logger.error("LinkedIn token exchange failed", extra={"status": response.status_code, "body": response.text})
                raise LinkedInPublishError(f"LinkedIn token exchange failed ({response.status_code}): {response.text}")
            return response.json()

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Fetch LinkedIn authenticated user identity."""
        if not settings.is_linkedin_configured or access_token.startswith("mock_"):
            return {
                "sub": "urn:li:person:demo_architect_99",
                "name": "LinkedIn AgentOS Operator",
                "email": "operator@agentos.internal",
                "picture": None
            }

        url = "https://api.linkedin.com/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise LinkedInPublishError(f"Failed to fetch LinkedIn user info: {response.status_code}")
            return response.json()

    def store_account(self, member_id: str, display_name: str, access_token: str, expires_in: int = 5184000) -> Dict[str, Any]:
        """Encrypt and store the LinkedIn account credentials."""
        encrypted_token = encrypt_secret(access_token)
        account_id = str(uuid.uuid4())
        account_record = {
            "id": account_id,
            "member_id": member_id,
            "display_name": display_name,
            "encrypted_access_token": encrypted_token,
            "token_expires_at": (datetime.now(timezone.utc) + timedelta(seconds=expires_in)).isoformat(),
            "is_connected": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._mock_accounts[account_id] = account_record
        logger.info("Encrypted and stored LinkedIn account", extra={"account_id": account_id, "member_id": member_id})
        return account_record

    async def publish_post(
        self,
        content: str,
        approval_status: str,
        approval_checksum: str,
        author_urn: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        account_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Publish a verified post to LinkedIn UGC API with zero-trust validation."""
        # 1. Zero-Trust Check: Approval status must be APPROVED
        if approval_status.upper() != "APPROVED":
            raise PublishSecurityError(
                f"Zero-trust security violation: Cannot publish content with status '{approval_status}'. Human approval is required."
            )

        # 2. Zero-Trust Check: Content SHA-256 fingerprint must match approval checksum
        content_hash = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()
        if content_hash != approval_checksum:
            raise PublishSecurityError(
                f"Zero-trust security violation: Content checksum drift detected! "
                f"Approved: {approval_checksum[:12]}... Computed: {content_hash[:12]}..."
            )

        # 3. Check configuration and execute publish or staged manual mode
        if not settings.is_linkedin_configured:
            logger.info("LinkedIn API unconfigured; staging post in manual fallback mode")
            fake_urn = f"urn:li:share:manual_{uuid.uuid4().hex[:10]}"
            result = {
                "id": str(uuid.uuid4()),
                "linkedin_urn": fake_urn,
                "publishing_status": "STAGED_MANUAL",
                "post_url": "https://www.linkedin.com/feed/",
                "content_preview": content[:140] + ("..." if len(content) > 140 else ""),
                "published_at": datetime.now(timezone.utc).isoformat(),
                "author": author_urn or "urn:li:person:demo_architect_99",
                "note": "LinkedIn API credentials not set. Post is cryptographically approved and staged for manual 1-click clipboard publishing.",
                "clipboard_payload": content,
                "media_urls": media_urls or []
            }
            self._mock_published_posts.append(result)
            return result

        # 4. Actual LinkedIn UGC Posts API invocation
        target_author = author_urn or "urn:li:person:me"
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        # Retrieve and decrypt access token if account provided
        access_token = None
        if account_id and account_id in self._mock_accounts:
            enc = self._mock_accounts[account_id]["encrypted_access_token"]
            access_token = decrypt_secret(enc)

        headers = {
            "Authorization": f"Bearer {access_token or 'mock_token'}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }

        share_media_category = "NONE"
        media_entities = []
        if media_urls:
            share_media_category = "IMAGE"
            for m_url in media_urls:
                media_entities.append({
                    "status": "READY",
                    "description": {"text": "Supporting technical visual"},
                    "media": m_url,
                    "title": {"text": "AgentOS Technical Visual"}
                })

        share_content: Dict[str, Any] = {
            "shareCommentary": {"text": content},
            "shareMediaCategory": share_media_category
        }
        if media_entities:
            share_content["media"] = media_entities

        payload = {
            "author": target_author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": share_content
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code not in (200, 201):
                logger.error("LinkedIn UGC API returned error", extra={"code": resp.status_code, "body": resp.text})
                raise LinkedInPublishError(f"LinkedIn UGC API error ({resp.status_code}): {resp.text}")

            resp_data = resp.json()
            post_urn = resp_data.get("id") or resp.headers.get("x-restli-id", f"urn:li:share:{uuid.uuid4().hex[:8]}")
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}"

            published_record = {
                "id": str(uuid.uuid4()),
                "linkedin_urn": post_urn,
                "publishing_status": "PUBLISHED",
                "post_url": post_url,
                "content_preview": content[:140] + ("..." if len(content) > 140 else ""),
                "published_at": datetime.now(timezone.utc).isoformat(),
                "author": target_author,
                "api_response": resp_data,
                "clipboard_payload": content,
                "media_urls": media_urls or []
            }
            self._mock_published_posts.append(published_record)
            logger.info("Successfully published post to LinkedIn", extra={"urn": post_urn})
            return published_record

    def get_publishing_history(self) -> List[Dict[str, Any]]:
        """Return the audit log of published and staged posts."""
        if not self._mock_published_posts:
            # Seed with one initial demonstrative record so the UI is immediately functional and instructive
            return [
                {
                    "id": "pub_sample_1",
                    "linkedin_urn": "urn:li:share:7165439820194816001",
                    "publishing_status": "PUBLISHED",
                    "post_url": "https://www.linkedin.com/feed/update/urn:li:share:7165439820194816001",
                    "content_preview": "Why AI Agent Teams Need Deterministic State Machines, Not Just Chat Loops...\n\nMost agent failures happen between steps...",
                    "published_at": (datetime.now(timezone.utc) - timedelta(hours=4)).isoformat(),
                    "author": "urn:li:person:demo_architect_99",
                    "media_urls": ["https://res.cloudinary.com/demo/image/upload/sample.jpg"],
                    "clipboard_payload": "Why AI Agent Teams Need Deterministic State Machines, Not Just Chat Loops...\n\nMost agent failures happen between steps. Here is how LangGraph + AgentOS solves it.\n\n#SoftwareEngineering #AIAgents"
                }
            ]
        return self._mock_published_posts

    def get_status(self) -> Dict[str, Any]:
        """Return connection state, credentials masking, and stats."""
        masked_client = ""
        if settings.LINKEDIN_CLIENT_ID:
            cid = settings.LINKEDIN_CLIENT_ID
            masked_client = cid[:4] + "••••" + cid[-4:] if len(cid) > 8 else "••••••••"

        return {
            "is_configured": settings.is_linkedin_configured,
            "client_id_masked": masked_client,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "active_accounts_count": len(self._mock_accounts),
            "total_posts_published": len(self._mock_published_posts),
            "has_accounts_connected": len(self._mock_accounts) > 0,
            "mode": "Live OAuth 2.0" if settings.is_linkedin_configured else "Manual Fallback & Staged Mode",
            "supported_scopes": ["w_member_social", "openid", "profile", "email"]
        }


# Global Singleton Service
linkedin_service = LinkedInService()

