# LinkedIn AgentOS — Production Operations & Deployment Guide

This guide provides instructions for deploying, configuring, and operating **LinkedIn AgentOS** in development and production environments.

---

## 1. System Requirements & Hardware Constraints

- **Python**: 3.12+ (tested on Python 3.12.6)
- **Node.js**: 18.18+ or 20+
- **Host RAM**: Optimized for 8GB RAM host environments.
  - Utilizes a single shared local Ollama model instance across all 8 specialist agents.
  - Enforces serialized LLM execution to avoid memory exhaustion.

---

## 2. Environment Configuration (`.env`)

Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

Key environment parameters:
```ini
# Application
APP_ENV=development
SECRET_KEY=generate_with_openssl_rand_hex_32
ENCRYPTION_KEY=generate_with_cryptography_Fernet_generate_key

# Neon PostgreSQL
DATABASE_URL=postgresql+asyncpg://neondb_owner:YOUR_KEY@ep-sample-pooler.us-east-2.aws.neon.tech/neondb?ssl=require
DATABASE_URL_DIRECT=postgresql+psycopg2://neondb_owner:YOUR_KEY@ep-sample.us-east-2.aws.neon.tech/neondb?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Ollama Local LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct
OLLAMA_TIMEOUT=120

# LinkedIn OAuth 2.0
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/v1/publishing/oauth/callback
```

---

## 3. Launching Backend & Frontend

### Starting the FastAPI Backend
```powershell
# In project root
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### Starting the Next.js Frontend
```powershell
cd frontend
npm run dev
```
Access the Enterprise AI Command Center at: `http://localhost:3000`

---

## 4. LinkedIn Developer Portal Setup

1. Navigate to [LinkedIn Developer Portal](https://www.linkedin.com/developers/).
2. Create an App and request the following products:
   - **Share on LinkedIn** (`w_member_social`)
   - **Sign In with LinkedIn using OpenID Connect** (`openid`, `profile`, `email`)
3. Under the **Auth** tab, add the Authorized Redirect URL:
   `http://localhost:8000/api/v1/publishing/oauth/callback`
4. Copy the Client ID and Client Secret into your `.env` or paste them into the AgentOS **Settings** center.

---

## 5. Graceful Disconnected & Manual Fallback Mode

If LinkedIn or Cloudinary credentials are not yet configured:
- The system automatically engages **Manual Fallback Mode**.
- The approval gate still enforces SHA-256 zero-trust verification.
- Once approved, the post is staged for manual publishing, providing a 1-click formatted clipboard copy button in the **Publishing History** view so operators can paste directly to the LinkedIn web interface.
