# LinkedIn AgentOS — Database Schema & Data Integrity Architecture

LinkedIn AgentOS uses **Neon PostgreSQL** as its single, durable source of truth. SQLite, local files, and browser state are explicitly banned from holding persistent application data.

---

## Core Entities & Relationships

### 1. `users`
System operators and LinkedIn content authors.
- `id`: UUID (Primary Key)
- `email`: VARCHAR(255) (Unique Index)
- `password_hash`: VARCHAR(255) (Argon2id cryptographic hash)
- `name`: VARCHAR(120)
- `role`: VARCHAR(50) (e.g. `architect`, `admin`)
- `is_active`: BOOLEAN
- `created_at`, `updated_at`: TIMESTAMPTZ

### 2. `agents`
Autonomous specialist agent registry.
- `id`: VARCHAR(50) (Primary Key, e.g. `master`, `research`, `writer`)
- `name`: VARCHAR(100)
- `role`: VARCHAR(100)
- `description`: TEXT
- `system_prompt`: TEXT
- `model_name`: VARCHAR(100) (Default: `qwen2.5:7b-instruct`)
- `temperature`: FLOAT
- `max_tokens`: INTEGER
- `is_active`: BOOLEAN

### 3. `tasks`
Content creation goals and daily schedule workflows.
- `id`: UUID (Primary Key)
- `title`: VARCHAR(255)
- `topic`: VARCHAR(255)
- `category`: VARCHAR(100) (e.g. `AI Engineering`, `System Design`)
- `target_audience`: VARCHAR(255)
- `status`: VARCHAR(50) (`PENDING`, `IN_PROGRESS`, `AWAITING_APPROVAL`, `COMPLETED`, `FAILED`)
- `scheduled_at`: TIMESTAMPTZ

### 4. `workflow_runs` & `workflow_checkpoints`
LangGraph state machine executions with durable PostgreSQL checkpointer.
- `id`: UUID (Primary Key)
- `task_id`: UUID (Foreign Key -> `tasks.id`)
- `execution_id`: VARCHAR(64)
- `current_step`: VARCHAR(100)
- `status`: VARCHAR(50)
- `retry_count`: INTEGER
- `error_details`: TEXT
- `state_snapshot`: JSONB

### 5. `content_drafts` & `content_versions`
Immutable versioned LinkedIn posts.
- Every content revision creates a new `content_versions` record with:
  - `version_number`: INTEGER
  - `hook`: TEXT
  - `main_body`: TEXT
  - `hashtags`: JSONB
  - `cta`: VARCHAR(255)
  - `references`: JSONB
  - `quality_score`: FLOAT
  - `checksum`: VARCHAR(64) (SHA-256 fingerprint of text)
  - `is_approved`: BOOLEAN

### 6. `approvals`
Human-in-the-loop audit trail.
- `id`: UUID (Primary Key)
- `task_id`: UUID (Foreign Key -> `tasks.id`)
- `content_version_id`: UUID
- `approval_type`: VARCHAR(50) (`TASK_START` or `FINAL_PUBLISH`)
- `status`: VARCHAR(50) (`PENDING`, `APPROVED`, `REJECTED`, `REVISE`)
- `version_checksum`: VARCHAR(64) (Cryptographic guarantee of what was approved)
- `reviewer_notes`: TEXT
- `signed_at`: TIMESTAMPTZ

### 7. `generated_media`
Metadata of Cloudinary assets (diagrams, SVGs, PDF carousels).
- `id`: UUID (Primary Key)
- `task_id`: UUID (Foreign Key -> `tasks.id`)
- `media_type`: VARCHAR(50) (`DIAGRAM`, `INFOGRAPHIC`, `PDF_CAROUSEL`, `SVG`)
- `cloudinary_url`: VARCHAR(1024)
- `cloudinary_public_id`: VARCHAR(255)
- `resource_type`: VARCHAR(20) (`image` or `raw` for PDFs)
- `meta_info`: JSONB

### 8. `linkedin_accounts` & `published_posts`
OAuth 2.0 integration and publication verification.
- `encrypted_access_token`: TEXT (Symmetric Fernet encryption)
- `linkedin_urn`: VARCHAR(255) (Official LinkedIn post identifier)
- `post_url`: VARCHAR(1024)
- `api_response`: JSONB

---

## Agent 6 Read-Back Verification Protocol

```
1. Write Operation initiated via Scoped Repository (create / update)
2. Database commits transaction to Neon PostgreSQL
3. Immediate Read-Back: Database Agent queries entity by primary key
4. Integrity Check:
   - Verify all non-nullable fields match submitted payload
   - Verify SHA-256 content checksum matches computed hash
   - Verify Foreign Key relationships exist
5. Return VERIFIED or throw critical ACID alert on mismatch
```

