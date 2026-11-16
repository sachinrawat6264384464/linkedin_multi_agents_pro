# LinkedIn AgentOS — API Reference Manual (v1.0.0)

Base URL: `http://localhost:8000/api/v1`

---

## 1. System Health & Sentinel Watchdog

### `GET /health`
Returns operational health status across core integrations.
- **Response `200 OK`**:
```json
{
  "status": "healthy",
  "app_name": "LinkedIn AgentOS",
  "environment": "development",
  "timestamp": "2026-11-17T01:30:00Z",
  "services": {
    "api": { "status": "online", "version": "1.0.0" },
    "database": { "configured": true, "status": "configured" },
    "ollama": { "base_url": "http://localhost:11434", "model": "qwen2.5:7b-instruct", "status": "ready" },
    "cloudinary": { "configured": false, "status": "not_configured" },
    "linkedin": { "configured": false, "status": "not_configured" }
  }
}
```

### `GET /monitoring/overview`
Aggregated system telemetry, uptime, and agent execution health score.
- **Response `200 OK`**:
```json
{
  "health_score": 100,
  "uptime_seconds": 1845,
  "uptime_formatted": "0:30:45",
  "total_agents": 8,
  "active_agents": 8,
  "total_agent_invocations": 40,
  "total_failures": 0,
  "pending_retries_count": 0,
  "memory_optimization_mode": "8GB_HOST_QUANTIZED_SINGLE_MODEL",
  "status": "HEALTHY"
}
```

### `GET /monitoring/agents`
Live telemetry, status, invocation counts, and moving average latency for each of the 8 agents.

### `GET /monitoring/logs`
Query fast in-memory ring-buffer audit logs with level filtering.
- **Query Params**: `level=ALL|INFO|WARN|ERROR`, `limit=100`

### `POST /monitoring/models/switch`
Dynamically switch the active Ollama model and inference hyperparameters.
- **Request Body**:
```json
{
  "model_tag": "qwen2.5:7b-instruct",
  "context_window": 4096,
  "temperature": 0.7
}
```

---

## 2. Multi-Agent Workflows & LangGraph Execution

### `POST /workflows/run`
Trigger end-to-end execution of the 8-agent LangGraph state machine.
- **Request Body**:
```json
{
  "topic": "Event-Driven Microservices with Kafka and Debezium",
  "category": "distributed-systems",
  "target_audience": "Senior Architects & Platform Engineers",
  "auto_approve": false
}
```
- **Response `200 OK`**:
```json
{
  "workflow_id": "wf-a1b2c3d4",
  "thread_id": "e5f6-7890",
  "status": "COMPLETED",
  "quality_approved": true,
  "persisted": true,
  "published": false,
  "next_action": "AWAITING_HUMAN_APPROVAL",
  "hook": "Why do microservices drop messages during failovers?",
  "checksum": "a8f5c3...64chars"
}
```

---

## 3. Human-in-the-Loop Approval Center

### `GET /approvals/pending`
Retrieve all drafts currently held at the LangGraph human approval checkpoint.

### `POST /approvals/{id}/sign`
Cryptographically sign or reject an approval ticket.
- **Request Body**:
```json
{
  "approval_id": "appr-12345678",
  "decision": "APPROVED",
  "reviewer_notes": "Verified architecture diagram and technical metrics."
}
```

---

## 4. LinkedIn Integration & Publishing

### `GET /publishing/status`
Check LinkedIn OAuth 2.0 configuration, connected accounts, and fallback mode.

### `GET /publishing/oauth/login`
Retrieve official LinkedIn OAuth 2.0 authorization URL.

### `POST /publishing/publish`
Publish an approved post to LinkedIn. Enforces zero-trust cryptographic signature matching.
- **Request Body**:
```json
{
  "content": "Full approved text content...",
  "approval_status": "APPROVED",
  "approval_checksum": "64_char_sha256_hash",
  "media_urls": ["https://res.cloudinary.com/.../carousel.pdf"]
}
```
- **Response `200 OK`**:
```json
{
  "id": "pub_uuid",
  "linkedin_urn": "urn:li:share:7165439820194816001",
  "publishing_status": "PUBLISHED",
  "post_url": "https://www.linkedin.com/feed/update/urn:li:share:7165439820194816001"
}
```
- **Error `403 Forbidden`**:
Returned if `approval_status != "APPROVED"` or if content text does not hash to `approval_checksum`.

### `POST /publishing/manual-copy`
Generates clean 1-click clipboard payload for LinkedIn web publishing in disconnected environments.

---

## 5. Model Context Protocol (MCP) Execution

### `GET /mcp/servers`
List all 7 registered MCP servers with status, transport, and exposed capabilities.

### `GET /mcp/tools`
Inspect full JSON schemas for all available MCP tools.

### `POST /mcp/execute`
Execute a tool through the MCP permission manager.
- **Request Body**:
```json
{
  "agent_id": "agent_1",
  "tool_name": "web_search",
  "arguments": { "query": "PostgreSQL 17 logical replication" }
}
```
- **Error `403 Forbidden`**: Returned if calling agent lacks required permission in the least-privilege matrix.

---

## 6. Media Studio & Visual Asset Generation

### `POST /media/diagram`
Synthesizes clean Mermaid.js architecture diagrams and flowcharts.

### `POST /media/carousel`
Builds a 1080x1080 multi-slide PDF carousel in memory via ReportLab and streams directly to Cloudinary using `resource_type="raw"`.

