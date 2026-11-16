# LinkedIn AgentOS — Model Context Protocol (MCP) Architecture

## 1. Overview
LinkedIn AgentOS adopts the **Model Context Protocol (MCP)** as its standardized tool-access and capability abstraction layer.
- **MCP Host**: AgentOS FastAPI backend.
- **MCP Clients**: Autonomous agents in the LangGraph workflow.
- **MCP Registry**: Central repository of typed tool schemas and connection endpoints.
- **Least-Privilege Permission Manager**: Strictly governs which agent can call which tool.

---

## 2. Seven Dedicated MCP Servers

### 1. `research_server`
- `research:search_web`: Queries technical search APIs (Tavily or mock) for papers, releases, and trends.
- `research:fetch_article`: Retrieves full-text article content from URLs.
- `research:extract_article`: Parses HTML/markdown into structured claims.
- `research:verify_sources`: Checks publication timestamps and cross-references.
- `research:save_research`: Stores structured report into PostgreSQL via scoped repository.

### 2. `content_server`
- `content:generate_post`: Generates technical hook, post body, and CTAs.
- `content:rewrite_post`: Revises draft based on quality critique.
- `content:check_grammar`: Linguistic and readability validator.
- `content:generate_hashtags`: Suggests high-intent technical hashtags.
- `content:save_draft`: Stores immutable draft version and calculates SHA-256 fingerprint.

### 3. `media_server`
- `media:generate_mermaid`: Produces architecture diagrams in Mermaid syntax.
- `media:render_svg`: Renders custom vector infographics.
- `media:create_carousel`: Compiles multi-slide PDF carousels using ReportLab.
- `media:upload_to_cloudinary`: Direct stream upload to Cloudinary storage.

### 4. `quality_server`
- `quality:verify_facts`: Cross-checks claims against verified sources.
- `quality:check_readability`: Computes Flesch-Kincaid and LinkedIn format scores.
- `quality:check_originality`: Anti-hallucination and plagiarism check.
- `quality:generate_scorecard`: Produces final APPROVE/REJECT scorecard.

### 5. `database_server`
- `database:create_record`: Parameterized insert with immediate read-back.
- `database:get_record`: Primary key lookup from Neon PostgreSQL.
- `database:update_record`: Scoped update with verification.
- `database:verify_record`: Audits persisted entity and checksum.
- `database:database_health`: Checks live Neon SSL connection.

### 6. `linkedin_server`
- `linkedin:get_profile`: Fetches authorized user's LinkedIn profile.
- `linkedin:upload_media`: Registers and uploads image/PDF to LinkedIn API.
- `linkedin:publish_approved_post`: Official v2 UGC post endpoint.
- `linkedin:get_post_status`: Polls status of published post.

### 7. `monitoring_server`
- `monitoring:get_system_health`: Telemetry across all services.
- `monitoring:get_agent_health`: Execution latencies and status.
- `monitoring:get_workflow_status`: Active LangGraph node inspect.
- `monitoring:retry_failed_task`: Safe exponential backoff retry.

---

## 3. Least-Privilege Permission Matrix

| Tool Namespace | Master | Research | Writer | Designer | Quality | Publisher | Database | Monitoring |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `research:*` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `content:*` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `media:*` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `quality:*` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `linkedin:*` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `database:*` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `monitoring:*` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `agent:*` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
