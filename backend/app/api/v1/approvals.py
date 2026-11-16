from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.approval_service import ApprovalService

router = APIRouter(prefix="/approvals", tags=["Human Approvals"])


class SignApprovalRequest(BaseModel):
    decision: str  # "APPROVED", "REJECTED", "REVISION_REQUESTED"
    reviewer_notes: Optional[str] = ""


class CreateApprovalRequest(BaseModel):
    task_id: str
    title: str
    content_version_id: str
    version_checksum: str
    approval_type: Optional[str] = "FINAL_PUBLISH"


@router.get("/pending")
async def get_pending_approvals():
    """Retrieve all tickets awaiting human review and cryptographic signing."""
    pending = ApprovalService.list_pending_approvals()
    # If empty in local dev, provide one sample staged ticket for demonstration
    if not pending:
        ApprovalService.request_approval(
            task_id="task-sample-1",
            title="State Persistence in Autonomous Agent Swarms",
            content_version_id="ver-sample-1",
            version_checksum="fea2d0428b8600496b3d18154f7490c4500119bc3294baa8b3f9796c52593c8a",
            approval_type="FINAL_PUBLISH"
        )
        pending = ApprovalService.list_pending_approvals()
    return pending


@router.get("/all")
async def get_all_approvals():
    """Retrieve complete immutable human approval audit trail."""
    return ApprovalService.list_all_approvals()


@router.post("/{approval_id}/sign")
async def sign_approval_ticket(approval_id: str, request: SignApprovalRequest):
    """
    Sign or reject an approval ticket.
    Enforces status transition and records reviewer notes.
    """
    try:
        updated = ApprovalService.sign_approval(
            approval_id=approval_id,
            status=request.decision,
            reviewer_notes=request.reviewer_notes or ""
        )
        return {"status": "success", "ticket": updated}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Approval ticket '{approval_id}' not found"
        )
