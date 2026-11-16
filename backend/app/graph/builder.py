from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import WorkflowState
from app.graph.nodes import (
    master_planning_node,
    research_node,
    writer_node,
    designer_node,
    quality_node,
    database_persistence_node,
    publisher_node,
    monitoring_node
)
from app.graph.routing import route_quality_decision, route_human_approval_decision


def build_workflow_graph():
    """
    Assembles the 8-agent production DAG for LinkedIn AgentOS.
    """
    workflow = StateGraph(WorkflowState)

    # Add Nodes
    workflow.add_node("master_planning", master_planning_node)
    workflow.add_node("research", research_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("designer", designer_node)
    workflow.add_node("quality", quality_node)
    workflow.add_node("database", database_persistence_node)
    workflow.add_node("publisher", publisher_node)
    workflow.add_node("monitoring", monitoring_node)

    # Define Linear Edges
    workflow.add_edge(START, "master_planning")
    workflow.add_edge("master_planning", "research")
    workflow.add_edge("research", "writer")
    workflow.add_edge("writer", "designer")
    workflow.add_edge("designer", "quality")

    # Conditional Routing after Quality Fact-Check
    workflow.add_conditional_edges(
        "quality",
        route_quality_decision,
        {
            "database": "database",
            "writer": "writer",
            "monitoring": "monitoring"
        }
    )

    # Conditional Routing after Database Persistence (Approval Gate before Publishing)
    workflow.add_conditional_edges(
        "database",
        route_human_approval_decision,
        {
            "publisher": "publisher",
            "monitoring": "monitoring"
        }
    )

    workflow.add_edge("publisher", "monitoring")
    workflow.add_edge("monitoring", END)

    # Checkpointer for durable thread state
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)


# Global compiled workflow instance
compiled_workflow = build_workflow_graph()
