# LinkedIn AgentOS — System Architecture & Specification

## Executive Summary
**LinkedIn AgentOS** is an enterprise autonomous multi-agent content research, creation, quality verification, media generation, human-in-the-loop approval, scheduling, and publishing platform designed specifically for technical thought leaders, AI researchers, and software engineers on LinkedIn.

---

## 1. Core Principles
1. **Source of Truth**: Neon PostgreSQL is the durable source of truth. SQLite, in-memory structures, and local files are never used for application state.
2. **Durable Media Storage**: All generated media (Mermaid architecture diagrams, SVG charts, infographics, PDF carousels) are stored directly in Cloudinary. PostgreSQL stores only URLs, metadata, and checksums.
3. **8-Agent Separation of Concerns**: One Master Orchestrator delegates tasks to seven specialized agents. The Master Orchestrator coordinates; specialists execute scoped work.
4. **Mandatory Database Read-Back Verification**: The Database Agent verifies every database write by immediately reading back the record from PostgreSQL, checking fields and checksums, and guaranteeing ACID consistency.
5. **Zero-Trust Publishing Security**: The LinkedIn Publishing Agent requires an explicit, immutable human approval record signed against the specific content version checksum. Backend services enforce approval validity—frontend UI cannot bypass this check.
6. **Standardized Tool Access via MCP**: Agents interact with environment capabilities exclusively through Model Context Protocol (MCP) servers with typed schemas and least-privilege permissions.
7. **Graceful Disconnected Mode**: The application boots safely and operates in offline/manual mode if external credentials (LinkedIn OAuth, Tavily, Cloudinary, Ollama) are not yet configured.

---

## 2. Multi-Agent Ecosystem (8 Agents)

```
+-----------------------------------------------------------------------------------+
|                            0. MASTER ORCHESTRATOR                                 |
|          Coordinates Task DAG, Manages Approvals, Handles Conditional Routing     |
+-----------------------------------------------------------------------------------+
       |                 |                   |                   |               |
       v                 v                   v                   v               v
+--------------+ +---------------+ +------------------+ +---------------+ +---------------+
|  1. RESEARCH | |   2. WRITER   | |    3. DESIGNER   | |   4. QUALITY  | | 5. PUBLISHER  |
|  Web Search  | | Hook Strategy | | Architecture SVG | | Fact-Checking | | Official OAuth|
|  Article Ext | | Technical Copy| | Multi-slide PDF  | | Readability   | | URN Tracking  |
|  Claim Verify| | CTA & Tags    | | Cloudinary Media | | Scorecard     | | Re-approval   |
+--------------+ +---------------+ +------------------+ +---------------+ +---------------+
                                            |
                                            v
                         +--------------------------------------+
                         |     6. DATABASE & PERSISTENCE        |
                         |   CRUD Tools & Read-Back Verification|
                         +--------------------------------------+
                                            |
                                            v
                         +--------------------------------------+
                         |     7. MONITORING & HEALTH           |
                         | Watchdog, Heartbeats & Safe Retries  |
                         +--------------------------------------+
```

---

## 3. LangGraph Workflow Execution Graph

```
[START]
   |
   v
[Master: Plan & Validate Task]
   |
   v
[Task Approval: Human-in-the-Loop Interrupt] ----(REJECTED)----> [CANCEL / REVISE]
   | (APPROVED)
   v
[Research Agent: Fetch & Verify Trends/Sources]
   |
   v
[Content Writer Agent: Draft Hook, Body, CTA & Hashtags]
   |
   v
[Visual Designer Agent: Render Architecture Diagram / PDF Carousel]
   |
   v
[Quality Agent: Verify Accuracy, Grammar & Technical Depth]
   |
   +----(SCORE < 80% or CRITICAL FLAW)----> [Loop back to Writer with Feedback]
   |
   v (QUALITY APPROVED)
[Database Agent: Write Content & Media + Read-Back Verify from Neon]
   |
   +----(CHECKSUM / INTEGRITY MISMATCH)----> [Flag Database Inconsistency]
   |
   v (VERIFIED PERSISTENT)
[Final Publishing Approval: Human-in-the-Loop Interrupt]
   |
   +----(REVISE / REJECT)----> [Human Feedback Loop to Writer]
   |
   v (HUMAN APPROVED & SIGNED)
[LinkedIn Publishing Agent: Validate Token -> Upload Media -> Publish Post]
   |
   v
[Publishing Verification: Store LinkedIn URN & API Response]
   |
   v
[Database Agent: Mark Task & Post as PUBLISHED]
   |
   v
[Monitoring Agent: Audit Trail & Duration Metrics]
   |
   v
[END]
```

---

## 4. MCP Servers & Scoped Tools

| MCP Server | Exposed Tools | Authorized Agents |
| :--- | :--- | :--- |
| `research_mcp` | `search_web`, `fetch_article`, `extract_article`, `verify_sources`, `save_research` | Research Agent (1) |
| `content_mcp` | `generate_post`, `rewrite_post`, `check_grammar`, `generate_hashtags`, `save_draft` | Content Writer (2) |
| `media_mcp` | `generate_mermaid`, `render_svg`, `create_infographic`, `create_carousel`, `upload_to_cloudinary` | Visual Designer (3) |
| `quality_mcp` | `verify_facts`, `check_readability`, `check_originality`, `generate_scorecard` | Quality Agent (4) |
| `linkedin_mcp`| `get_profile`, `upload_media`, `create_post_draft`, `publish_approved_post`, `get_post_status` | LinkedIn Publisher (5) |
| `database_mcp`| `create_record`, `get_record`, `update_record`, `verify_record`, `database_health` | Database Agent (6) |
| `agent_mcp`   | `assign_task`, `get_agent_status`, `get_task_result`, `request_approval` | Master Orchestrator (0) |
| `monitoring_mcp` | `get_system_health`, `get_agent_health`, `get_failure_report`, `retry_failed_task` | Monitoring Agent (7) |

