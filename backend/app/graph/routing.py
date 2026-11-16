from typing import Literal
from app.graph.state import WorkflowState
from app.core.logging import logger


def route_quality_decision(state: WorkflowState) -> Literal["database", "writer", "monitoring"]:
    """
    Evaluates Quality Agent verdict.
    If approved -> moves to database persistence.
    If rejected & within loop budget -> sends back to writer for revision.
    If exceeded loop budget -> terminates to prevent runaway cycles.
    """
    is_approved = state.get("quality_approved", False)
    loop_count = state.get("quality_loop_count", 0)

    if is_approved:
        return "database"

    if loop_count < 3:
        logger.info(f"Quality check rejected. Routing revision loop attempt {loop_count + 1} to Writer.")
        return "writer"

    logger.warning("Quality check failed 3 times. Halting loop to prevent infinite token consumption.")
    return "monitoring"


def route_human_approval_decision(state: WorkflowState) -> Literal["publisher", "monitoring"]:
    """
    Evaluates Human Approval Gate before publishing.
    Publishing requires human_approved=True AND matching version checksum.
    """
    approved = state.get("human_approved", False)
    approval_checksum = state.get("approval_checksum")
    content_checksum = state.get("checksum")

    if approved and approval_checksum == content_checksum:
        return "publisher"

    logger.info("Human approval pending or checksum mismatch. Publishing held.")
    return "monitoring"

