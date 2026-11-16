import time
import uuid
from typing import Dict, Any, List, Optional
from app.db.models.content import ContentVersion
from app.core.logging import logger


class ApprovalService:
    """
    Enforces Human-in-the-Loop Zero-Trust governance.
    No post can ever reach LinkedIn without an active, cryptographically
    matching human approval signature.
    """

    _APPROVALS_STORE: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def request_approval(
        cls,
        task_id: str,
        content_version_id: str,
        version_checksum: str,
        approval_type: str = "FINAL_PUBLISH",
        title: str = "LinkedIn Technical Post"
    ) -> Dict[str, Any]:
        """Create a pending human approval ticket locked to a specific checksum."""
        approval_id = f"appr-{uuid.uuid4().hex[:8]}"
        record = {
            "id": approval_id,
            "task_id": task_id,
            "title": title,
            "content_version_id": content_version_id,
            "version_checksum": version_checksum,
            "approval_type": approval_type,
            "status": "PENDING",  # PENDING, APPROVED, REJECTED, REVISION_REQUESTED
            "reviewer_notes": "",
            "signed_at": None,
            "created_at": int(time.time())
        }
        cls._APPROVALS_STORE[approval_id] = record
        return record

    @classmethod
    def sign_approval(
        cls,
        approval_id: str,
        status: str,
        reviewer_notes: str = ""
    ) -> Dict[str, Any]:
        """Sign or reject an approval ticket."""
        if approval_id not in cls._APPROVALS_STORE:
            raise KeyError(f"Approval ticket '{approval_id}' not found.")

        record = cls._APPROVALS_STORE[approval_id]
        record["status"] = status
        record["reviewer_notes"] = reviewer_notes
        record["signed_at"] = int(time.time())
        return record

    @classmethod
    def is_publishing_authorized(cls, content_checksum: str) -> bool:
        """
        Verify if an APPROVED human signature exists that matches the exact checksum.
        If content changed after signing, this returns False automatically.
        """
        for record in cls._APPROVALS_STORE.values():
            if (
                record.get("approval_type") == "FINAL_PUBLISH"
                and record.get("status") == "APPROVED"
                and record.get("version_checksum") == content_checksum
            ):
                return True
        return False

    @classmethod
    def list_pending_approvals(cls) -> List[Dict[str, Any]]:
        return [a for a in cls._APPROVALS_STORE.values() if a["status"] == "PENDING"]

    @classmethod
    def list_all_approvals(cls) -> List[Dict[str, Any]]:
        return list(cls._APPROVALS_STORE.values())

