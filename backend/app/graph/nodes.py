import time
from typing import Dict, Any
from app.graph.state import WorkflowState
from app.agents import get_agent
from app.core.logging import logger


async def master_planning_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 0: Master Orchestrator plans task execution."""
    agent = get_agent("master")
    res = await agent.execute(dict(state))
    return {
        "current_node": "master_planning",
        "execution_history": [{
            "node": "master_planning",
            "agent": "master",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "COMPLETED"
        }]
    }


async def research_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 1: Technical Research Agent collects sources."""
    agent = get_agent("research")
    res = await agent.execute(dict(state))
    return {
        "current_node": "research",
        "research_summary": res.data.get("research_summary"),
        "key_findings": res.data.get("key_findings", []),
        "research_sources": res.data.get("sources", []),
        "execution_history": [{
            "node": "research",
            "agent": "research",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "COMPLETED"
        }]
    }


async def writer_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 2: Content Writer drafts technical post."""
    agent = get_agent("writer")
    res = await agent.execute(dict(state))
    return {
        "current_node": "writer",
        "hook": res.data.get("hook"),
        "main_body": res.data.get("main_body"),
        "cta": res.data.get("cta"),
        "hashtags": res.data.get("hashtags", []),
        "checksum": res.data.get("checksum"),
        "version_number": state.get("version_number", 1),
        "execution_history": [{
            "node": "writer",
            "agent": "writer",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "COMPLETED"
        }]
    }


async def designer_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 3: Visual Designer creates diagrams and carousels."""
    agent = get_agent("designer")
    res = await agent.execute(dict(state))
    return {
        "current_node": "designer",
        "media_asset": res.data.get("media_asset"),
        "execution_history": [{
            "node": "designer",
            "agent": "designer",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "COMPLETED"
        }]
    }


async def quality_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 4: Quality & Fact-Checking Agent audits post."""
    agent = get_agent("quality")
    res = await agent.execute(dict(state))
    is_approved = res.data.get("quality_approved", False)
    loop_count = state.get("quality_loop_count", 0) + (0 if is_approved else 1)
    return {
        "current_node": "quality",
        "quality_approved": is_approved,
        "quality_scorecard": res.data.get("scorecard"),
        "quality_loop_count": loop_count,
        "execution_history": [{
            "node": "quality",
            "agent": "quality",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "APPROVED" if is_approved else "REJECTED_REVISION"
        }]
    }


async def database_persistence_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 6: Database Agent persists to PostgreSQL and executes read-back audit."""
    agent = get_agent("database")
    res = await agent.execute(dict(state))
    updates: Dict[str, Any] = {
        "current_node": "database",
        "persisted": res.data.get("persisted", False),
        "persisted_version_id": res.data.get("persisted_version_id"),
        "read_back_status": res.data.get("read_back_status"),
        "execution_history": [{
            "node": "database",
            "agent": "database",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "VERIFIED"
        }]
    }
    # If human_approved flag is set (e.g. test pipeline), sign the immutable checksum
    if state.get("human_approved"):
        updates["approval_checksum"] = state.get("checksum")

    return updates


async def publisher_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 5: LinkedIn Publishing Agent verifies approval and publishes."""
    agent = get_agent("publisher")
    res = await agent.execute(dict(state))
    return {
        "current_node": "publisher",
        "published": res.data.get("published", False),
        "post_urn": res.data.get("post_urn"),
        "post_url": res.data.get("post_url"),
        "publishing_mode": res.data.get("mode"),
        "execution_history": [{
            "node": "publisher",
            "agent": "publisher",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "PUBLISHED" if res.success else "FAILED"
        }]
    }


async def monitoring_node(state: WorkflowState) -> Dict[str, Any]:
    """Node 7: Monitoring Agent produces execution metrics."""
    agent = get_agent("monitoring")
    res = await agent.execute(dict(state))
    return {
        "current_node": "monitoring",
        "execution_history": [{
            "node": "monitoring",
            "agent": "monitoring",
            "duration_ms": res.duration_ms,
            "timestamp": int(time.time()),
            "status": "COMPLETED"
        }]
    }
