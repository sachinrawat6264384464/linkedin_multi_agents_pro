# LinkedIn AgentOS — Autonomous Multi-Agent Content & Publishing Platform

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/next.js-15+-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)](https://github.com/langchain-ai/langgraph)
[![PostgreSQL](https://img.shields.io/badge/Neon-PostgreSQL-336791.svg)](https://neon.tech)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise autonomous AI operations command center designed to research, draft, design, fact-check, persist, approve, and publish LinkedIn content at scale.

---

## ⚡ Key Highlights

- **8-Agent Architecture**: 1 Master Orchestrator + 7 Specialists (Research, Writer, Visual Designer, Quality/Fact-Checker, LinkedIn Publisher, Database/Persistence, Monitoring).
- **PostgreSQL Source of Truth**: Durable persistence backed by Neon PostgreSQL.
- **Mandatory Read-Back Verification**: Every database write is read back from PostgreSQL to guarantee ACID consistency.
- **Durable Media Storage**: Architecture diagrams, SVGs, and multi-slide PDF carousels uploaded to Cloudinary.
- **Standardized MCP Layer**: Model Context Protocol servers for least-privilege, typed tool execution.
- **Zero-Trust Publishing Security**: Backend-enforced cryptographic approval check preventing unapproved publishing.
- **Resource-Efficient Local LLM**: Shared Ollama execution with graceful disconnected standby mode.
- **Enterprise Dark Theme**: Built with Next.js 15 App Router, React 19, and Tailwind CSS (`#090909`, `#171717`, `#E53935`).

---

## 🏗️ 8-Agent Ecosystem

| # | Agent Name | Core Responsibilities |
|---|---|---|
| **0** | **Master Orchestrator** | Task DAG execution, human-in-the-loop interrupts, conditional routing, retries |
| **1** | **Research Agent** | Real-time web discovery, article parsing, claim verification, structured reports |
| **2** | **Content Writer** | High-conversion technical hooks, story-driven body copy, CTAs, hashtags |
| **3** | **Visual Designer** | Mermaid architecture diagrams, SVGs, multi-slide PDF carousels, Cloudinary storage |
| **4** | **Quality & Fact-Checker** | Independent claim verification, readability scoring, anti-hallucination guardrails |
| **5** | **LinkedIn Publishing** | Official OAuth 2.0 publishing, media attachment, URN tracking, immutable approval check |
| **6** | **Database & Persistence** | Scoped CRUD tools, mandatory read-back verification against Neon PostgreSQL |
| **7** | **Monitoring & Health** | Service watchdogs, telemetry, execution duration metrics, safe exponential backoff retries |

---

## 🚀 Quickstart (Windows PowerShell)

### 1. Clone & Setup Environment
```powershell
git clone https://github.com/sachinrawat6264384464/linkedin_multi_agents_pro.git
cd linkedin_multi_agents_pro

# Create Python 3.12 venv
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend\requirements.txt
```

### 2. Configure Environment Keys
```powershell
cp .env.example .env
# Edit .env with your Neon PostgreSQL, Cloudinary, Ollama, and LinkedIn API credentials
```

### 3. Run Backend (FastAPI)
```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### 4. Run Frontend (Next.js 15)
```powershell
cd frontend
npm install --legacy-peer-deps
npm run dev
```
- Command Center UI: [http://localhost:3000](http://localhost:3000)

### 5. Run Automated Tests
```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\pytest.exe backend\tests -v
```

---

## 📜 Documentation

- [System Architecture (ARCHITECTURE.md)](./ARCHITECTURE.md)
- [Environment Setup Guide (ENV_SETUP.md)](./ENV_SETUP.md)
- [Development Roadmap (DEVELOPMENT_ROADMAP.md)](./DEVELOPMENT_ROADMAP.md)
