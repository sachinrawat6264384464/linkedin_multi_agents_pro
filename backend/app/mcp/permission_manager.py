from typing import Set, Dict
from app.core.logging import logger

# Static default permission matrix enforcing least privilege
# In production, this can also be extended by database-backed permissions
_ALLOWED_PERMISSIONS: Dict[str, Set[str]] = {
    "master": {
        "agent:assign_task",
        "agent:get_agent_status",
        "agent:get_task_result",
        "agent:request_approval",
        "agent:get_execution_logs"
    },
    "research": {
        "research:search_web",
        "research:fetch_article",
        "research:extract_article",
        "research:verify_sources",
        "research:save_research"
    },
    "writer": {
        "content:generate_post",
        "content:rewrite_post",
        "content:check_grammar",
        "content:generate_hashtags",
        "content:save_draft"
    },
    "designer": {
        "media:generate_mermaid",
        "media:render_svg",
        "media:create_infographic",
        "media:create_pdf",
        "media:create_carousel",
        "media:upload_to_cloudinary"
    },
    "quality": {
        "quality:verify_facts",
        "quality:check_readability",
        "quality:check_originality",
        "quality:generate_scorecard"
    },
    "publisher": {
        "linkedin:get_profile",
        "linkedin:upload_media",
        "linkedin:create_post_draft",
        "linkedin:publish_approved_post",
        "linkedin:get_post_status"
    },
    "database": {
        "database:create_record",
        "database:get_record",
        "database:update_record",
        "database:delete_record",
        "database:list_records",
        "database:verify_record",
        "database:database_health"
    },
    "monitoring": {
        "monitoring:get_system_health",
        "monitoring:get_agent_health",
        "monitoring:get_workflow_status",
        "monitoring:get_failure_report",
        "monitoring:retry_failed_task"
    }
}


class MCPPermissionManager:
    """Validates whether a specific agent is authorized to invoke a target MCP tool."""

    @staticmethod
    def is_authorized(agent_id: str, tool_id: str) -> bool:
        allowed = _ALLOWED_PERMISSIONS.get(agent_id, set())
        is_ok = tool_id in allowed
        if not is_ok:
            logger.warning(f"SECURITY ALERT: Agent '{agent_id}' was DENIED permission to execute MCP tool '{tool_id}'")
        return is_ok

    @staticmethod
    def get_allowed_tools_for_agent(agent_id: str) -> Set[str]:
        return _ALLOWED_PERMISSIONS.get(agent_id, set())

