import uuid
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.graph.builder import compiled_workflow
from app.core.logging import logger

router = APIRouter(prefix="/workflows", tags=["Workflows"])


class RunWorkflowRequest(BaseModel):
    topic: str
    category: Optional[str] = "AI Engineering"
    target_audience: Optional[str] = "Software Engineers & Tech Leaders"
    auto_approve: Optional[bool] = False  # Set true for simulated end-to-end tests


@router.post("/run")
async def trigger_workflow(request: RunWorkflowRequest):
    """
    Trigger an execution run of the complete 8-agent LangGraph workflow.
    """
    thread_id = str(uuid.uuid4())
    workflow_id = f"wf-{thread_id[:8]}"

    initial_state = {
        "task_id": str(uuid.uuid4()),
        "workflow_id": workflow_id,
        "topic": request.topic,
        "category": request.category,
        "target_audience": request.target_audience,
        "execution_history": [],
        "human_approved": request.auto_approve,
        "quality_loop_count": 0,
        "version_number": 1
    }

    config = {"configurable": {"thread_id": thread_id}}

    try:
        final_state = await compiled_workflow.ainvoke(initial_state, config=config)
        return {
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "status": "COMPLETED",
            "topic": final_state.get("topic"),
            "quality_approved": final_state.get("quality_approved"),
            "persisted": final_state.get("persisted"),
            "published": final_state.get("published"),
            "post_urn": final_state.get("post_urn"),
            "post_url": final_state.get("post_url"),
            "hook": final_state.get("hook"),
            "main_body": final_state.get("main_body"),
            "cta": final_state.get("cta"),
            "hashtags": final_state.get("hashtags"),
            "checksum": final_state.get("checksum"),
            "execution_steps": len(final_state.get("execution_history", []))
        }
    except Exception as e:
        logger.error(f"LangGraph execution error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(e)}"
        )

