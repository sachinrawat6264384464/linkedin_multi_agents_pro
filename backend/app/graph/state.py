from typing import TypedDict, Optional, List, Dict, Any, Annotated
import operator


class WorkflowState(TypedDict, total=False):
    """
    Typed state dictionary passed through every node of the LangGraph DAG.
    """
    # Task metadata
    task_id: str
    workflow_id: str
    topic: str
    category: str
    target_audience: str

    # Workflow progress & routing
    current_node: str
    retry_count: int
    quality_loop_count: int
    execution_history: Annotated[List[Dict[str, Any]], operator.add]

    # Human Approval Gates
    task_approved: bool
    human_approved: bool
    approval_checksum: Optional[str]
    human_notes: Optional[str]

    # Specialist Agent Outputs
    research_summary: Optional[str]
    research_sources: List[Dict[str, Any]]
    key_findings: List[str]

    # Content Drafting
    hook: Optional[str]
    main_body: Optional[str]
    cta: Optional[str]
    hashtags: List[str]
    checksum: Optional[str]
    version_number: int

    # Visual Media
    media_asset: Optional[Dict[str, Any]]

    # Quality Audit
    quality_approved: bool
    quality_scorecard: Optional[Dict[str, Any]]
    quality_feedback: Optional[str]

    # Persistence & Read-Back Verification
    persisted: bool
    persisted_version_id: Optional[str]
    read_back_status: Optional[str]

    # Publishing
    published: bool
    post_urn: Optional[str]
    post_url: Optional[str]
    publishing_mode: Optional[str]

