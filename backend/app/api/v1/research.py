from fastapi import APIRouter, Query
from typing import List, Dict, Any
from app.services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["Research & Discovery"])


@router.get("/search")
async def search_topics(query: str = Query(..., min_length=2)):
    """Search for relevant technology research and architectural references."""
    results = await ResearchService.search_technical_topics(query)
    return {"query": query, "count": len(results), "results": results}


@router.get("/sources")
async def list_sources():
    """Retrieve verified research references collected by Agent 1."""
    return [
        {
            "id": "src-1",
            "url": "https://modelcontextprotocol.io/introduction",
            "title": "Model Context Protocol Specification",
            "summary": "Standardized protocol for connecting AI models to external systems.",
            "publication_date": "2024-11",
            "verification_status": "VERIFIED"
        },
        {
            "id": "src-2",
            "url": "https://neon.tech/docs/introduction",
            "title": "Serverless Postgres Architecture",
            "summary": "Separation of storage and compute in serverless PostgreSQL.",
            "publication_date": "2024-10",
            "verification_status": "VERIFIED"
        }
    ]
