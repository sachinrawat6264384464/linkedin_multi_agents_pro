# LinkedIn AgentOS — Environment Setup Guide

This guide walks you through setting up and running **LinkedIn AgentOS** locally on Windows PowerShell.

---

## Prerequisites
1. **Python 3.12+**: Installed at `C:\Program Files\Python312\python.exe`
2. **Node.js 20+** / npm 10+
3. **Git**
4. *(Optional but Recommended)* **Ollama**: For local LLM inference (`ollama run qwen2.5:7b-instruct`)
5. *(Optional)* **Neon PostgreSQL Account**: Free tier serverless Postgres database
6. *(Optional)* **Cloudinary Account**: Free tier for image and PDF storage

---

## 1. Virtual Environment Setup

From the project root (`d:\linkedin_agents`):

```powershell
# Create Python 3.12 virtual environment (already initialized in Phase 1)
py -3.12 -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend\requirements.txt
```

---

## 2. Environment Configuration

Copy the example configuration to `.env`:
```powershell
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Neon PostgreSQL Connection (SSL required)
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>/<dbname>?ssl=require
DATABASE_URL_DIRECT=postgresql+psycopg2://<user>:<password>@<host>/<dbname>?sslmode=require

# Cloudinary Media Storage
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

# Ollama Local LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct

# LinkedIn OAuth 2.0
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/v1/publishing/oauth/callback
```

> **Note**: LinkedIn AgentOS boots cleanly in **Safe Disconnected Mode** even if Cloudinary, LinkedIn, or Neon credentials are not yet entered.

---

## 3. Running Backend Services

```powershell
# From project root with venv active
cd backend
..\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload
```

- API Docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
- Live WebSocket: `ws://localhost:8000/ws/live`

---

## 4. Running Frontend Services

```powershell
# From project root
cd frontend
npm install
npm run dev
```

- Web Dashboard: [http://localhost:3000](http://localhost:3000)

---

## 5. Running Tests

```powershell
# From project root
.\venv\Scripts\pytest.exe backend/tests -v
```

