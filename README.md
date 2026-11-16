# LinkedIn AgentOS 🚀
### Autonomous Multi-Agent Content Research, Verification, Media Generation & Publishing Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Next.js](https://img.shields.io/badge/Next.js-15.1+-black.svg)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/Neon-PostgreSQL%20Serverless-00E599.svg)](https://neon.tech)
[![Tests](https://img.shields.io/badge/Pytest-40%2F40%20Passed-brightgreen.svg)](TESTING.md)
[![Zero--Trust](https://img.shields.io/badge/Security-SHA--256%20Zero--Trust-red.svg)](SECURITY.md)

---

## 1. System Overview

**LinkedIn AgentOS** is an enterprise-grade autonomous multi-agent platform designed to conduct deep technical research, synthesize viral LinkedIn thought leadership content, generate supporting architecture diagrams and PDF carousels, run rigorous automated quality checks, persist all versions with read-back verification, enforce zero-trust human cryptographic approvals, and publish directly to LinkedIn through official OAuth 2.0 UGC APIs.

### Key Architectural Principles
- **Zero-Trust Human Governance**: No autonomous agent or scheduled job may publish content to LinkedIn without a human operator cryptographically signing off on an exact SHA-256 fingerprint.
- **Durable Source of Truth**: Neon PostgreSQL serves as the permanent source of truth with mandatory immediate read-back verification on every database write.
- **Resource-Efficient Local Execution**: Optimized for 8GB RAM host environments by sharing a single quantized local Ollama LLM (`qwen2.5:7b-instruct`) across all 8 specialist agents.
- **Custom MCP Tool Architecture**: 7 custom Model Context Protocol (MCP) servers enforced by an agent-specific least-privilege permission matrix.
- **Media Streaming**: In-memory synthesis of Mermaid diagrams and 1080x1080 ReportLab PDF carousels streamed directly to Cloudinary with `resource_type="raw"`.

---

## 2. System Architecture

```
+-----------------------------------------------------------------------------------------+
|                                    LINKEDIN AGENTOS                                     |
+-----------------------------------------------------------------------------------------+
                                             |
                                    [ User Request / Cron ]
                                             |
                                             v
                           +-----------------------------------+
                           |    Agent 0: Master Orchestrator   |
                           |   (LangGraph StateGraph Engine)   |
                           +-----------------------------------+
                                             |
                   +-------------------------+-------------------------+
                   |                         |                         |
                   v                         v                         v
        +---------------------+   +---------------------+   +---------------------+
        | Agent 1: Research   |   | Agent 2: Writer     |   | Agent 3: Visual     |
        | - Web Search MCP    |   | - Viral Hooks       |   | - Mermaid Diagrams  |
        | - Fact Grounding    |   | - Technical Body    |   | - ReportLab PDF     |
        | - Source Tracking   |   | - Call-to-Actions   |   | - Cloudinary Stream |
        +---------------------+   +---------------------+   +---------------------+
                   |                         |                         |
                   +-------------------------+-------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Agent 4: Quality & Fact Checker   |
                           | (Score >= 80% / Revision Loop)    |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Agent 6: Database Guardian        |
                           | (Neon Read-Back Verification)     |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | [ HUMAN APPROVAL CENTER ]         |
                           | - SHA-256 Checksum Signature Gate |
                           | - LangGraph Durable State Hold    |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Agent 5: LinkedIn Publisher       |
                           | - OAuth 2.0 UGC Posts API         |
                           | - Manual 1-Click Fallback Mode    |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Agent 7: Monitoring Sentinel      |
                           | - Real-time Agent Heartbeats      |
                           | - Stalled Task Detector           |
                           | - Exponential Retries (Max 3)     |
                           +-----------------------------------+
```

---

## 3. The 8 Specialized AI Agents

1. **Agent 0 — Master Orchestrator**: LangGraph state machine coordinator managing execution flow, routing, and conditional revisions.
2. **Agent 1 — Research Specialist**: Gathers technical sources, fetches web articles, extracts facts, and records citations.
3. **Agent 2 — Content Writer**: Engineers high-retention hooks, professional technical discourse, code snippets, and relevant hashtags.
4. **Agent 3 — Visual Designer**: Renders Mermaid architecture diagrams and compiles 1080x1080 square multi-slide PDF carousels in memory.
5. **Agent 4 — Quality & Fact Checker**: Audits technical accuracy, originality, readability, and LinkedIn formatting. Re-routes drafts scoring under 80% back for revision.
6. **Agent 5 — LinkedIn Publisher**: Interfaces with official LinkedIn OAuth 2.0 & UGC API; validates cryptographic signatures and manages manual fallback copy modes.
7. **Agent 6 — Database Guardian**: Executes CRUD transactions against Neon PostgreSQL with immediate read-back verification.
8. **Agent 7 — Monitoring Sentinel**: Tracks heartbeats across all 8 agents, detects stalled tasks, triggers exponential retries, and buffers live execution logs.

---

## 4. UI Design System (Black, White & Red)

The frontend is an enterprise dark AI command center inspired by modern security operations centers:
- **Background**: `#090909` (Primary background), `#111111` (Secondary), `#171717` (Elevated panels)
- **Typography**: Inter / Geist sans-serif, high contrast white `#FFFFFF` and muted text `#A3A3A3`
- **Accent Red**: `#E53935` used exclusively for active navigation, critical approval actions, security alerts, and live execution indicators
- **Navigation**: Collapsible 15-module sidebar with real-time status indicators and system health header

---

## 5. Quickstart & Installation

### Prerequisites
- Python 3.12+
- Node.js 18.18+ or 20+
- Git

### 1. Clone & Set Up Python Virtual Environment
```powershell
git clone https://github.com/sachinrawat6264384464/linkedin_multi_agents_pro.git
cd linkedin_multi_agents_pro

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables
```powershell
cp .env.example .env
# Edit .env to add your keys (Neon, Cloudinary, LinkedIn, Ollama)
```

### 3. Launch the Backend API
```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger API Explorer is available at: `http://localhost:8000/docs`

### 4. Launch the Next.js Frontend
```powershell
cd frontend
npm install --legacy-peer-deps
npm run dev
```
Open `http://localhost:3000` to access the Command Center.

---

## 6. Verification & Test Suite

All 10 project phases are covered by an automated test suite:
```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\pytest.exe backend\tests -v
```
**Result**: `40 passed in 30.09s (100% pass rate)`

To verify the Next.js production build:
```powershell
cd frontend
npm run build
```

---

## 7. Documentation Index

- 📘 [API Documentation](API_DOCUMENTATION.md) — Complete REST endpoint specifications, schemas, and curl examples.
- 🛡️ [Security Specification](SECURITY.md) — Zero-trust gates, SHA-256 fingerprinting, Fernet encryption, and MCP least-privilege matrix.
- 🧪 [Testing Manual](TESTING.md) — Test architecture, coverage breakdown, and reproduction commands.
- ⚙️ [Operations Guide](OPERATIONS_GUIDE.md) — Production deployment runbook, hardware sizing, and LinkedIn developer app setup.
- 🗺️ [Development Roadmap](DEVELOPMENT_ROADMAP.md) — Full phased delivery log from initial setup to release acceptance.
- 🤖 [Agent Architecture](AGENT_ARCHITECTURE.md) — LangGraph state machine, typed dictionaries, and specialist agent prompts.
- 🗄️ [Database Schema](DATABASE_SCHEMA.md) — Normalized PostgreSQL ER model and read-back verification specifications.
- 🔌 [MCP Architecture](MCP_ARCHITECTURE.md) — Custom MCP tool registry, JSON schemas, and execution security.
