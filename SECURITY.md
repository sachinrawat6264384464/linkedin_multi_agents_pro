# LinkedIn AgentOS — Enterprise Security Specification

## 1. Zero-Trust Architecture Overview

LinkedIn AgentOS is designed under a strict **Zero-Trust Human Governance** model. No autonomous AI agent, background scheduler, or automated quality gate is permitted to publish content directly to LinkedIn without an explicit, verifiable, human cryptographic signature.

```
+-----------------------------------------------------------------------------------+
|                            ZERO-TRUST PIPELINE GATES                              |
|                                                                                   |
|  [ Content Writer ] ---> [ Quality Auditor ] ---> [ SHA-256 Checksum Stamped ]    |
|                                                              |                    |
|                                                              v                    |
|                                                    [ DB Read-Back Verified ]      |
|                                                              |                    |
|                                                              v                    |
|                                                [ LangGraph Durable Interrupt ]    |
|                                                              |                    |
|                                                              v                    |
|                                                 [ Human Cryptographic Signing ]   |
|                                                              |                    |
|                                   +--------------------------+                    |
|                                   | Checksum Matches?                             |
|                                   v                                               |
|                    YES : [ LinkedIn UGC Dispatch ]                                |
|                    NO  : [ 403 Forbidden Blocked ]                                |
+-----------------------------------------------------------------------------------+
```

---

## 2. Cryptographic Content Fingerprinting (SHA-256)

Every draft iteration produces an immutable `ContentVersion` entity containing:
$$\text{Checksum} = \text{SHA256}(\text{hook} + \text{body} + \text{cta})$$

When an operator signs an approval ticket in the Approval Center:
1. The approval record permanently records the approved checksum.
2. When the publishing service receives a dispatch request, it computes $\text{SHA256}(\text{incoming\_content})$.
3. If the incoming hash does not match the approved checksum down to the exact byte, the request is immediately rejected with `403 Forbidden: Checksum drift detected`.
4. Any post-approval prompt injection or rogue LLM alteration is mathematically prevented from publishing.

---

## 3. Secret & OAuth Token Encryption

1. **Fernet Symmetric Cryptography**:
   - OAuth 2.0 access tokens and refresh tokens are encrypted at rest using AES-128 in CBC mode with HMAC-SHA256 authenticated encryption (`app.core.encryption.encrypt_secret`).
   - Plaintext access tokens are never committed to the database, logs, or API responses.
2. **Credential Masking**:
   - API keys and client secrets are masked in the UI and API responses (e.g. `77••••••••12`).
   - Environment variables are managed strictly via `.env` (strictly ignored by `.gitignore`).

---

## 4. Model Context Protocol (MCP) Least-Privilege Matrix

Agents do not have blanket access to all system tools. Access is mediated by `app.mcp.permission_manager.PermissionManager`:

| Agent | Read Research | Draft Content | Generate Media | Neon DB Write | LinkedIn Publish | System Monitor |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Agent 0 (Orchestrator)** | Read | Read | Read | Read | Read | Read/Write |
| **Agent 1 (Research)** | **Execute** | Denied | Denied | Denied | Denied | Denied |
| **Agent 2 (Writer)** | Read | **Execute** | Denied | Denied | Denied | Denied |
| **Agent 3 (Visual)** | Denied | Denied | **Execute** | Denied | Denied | Denied |
| **Agent 4 (Quality)** | Read | Read | Read | Denied | Denied | Denied |
| **Agent 5 (Publisher)** | Denied | Denied | Denied | Denied | **Execute** | Denied |
| **Agent 6 (Database)** | Denied | Denied | Denied | **Execute** | Denied | Denied |
| **Agent 7 (Monitoring)** | Denied | Denied | Denied | Denied | Denied | **Execute** |

Attempts to invoke tools outside an agent's allocated role trigger immediate security warnings and return `403 Forbidden`.

---

## 5. Database & Cloud Storage Security

1. **Neon PostgreSQL**:
   - Mandatory SSL encryption: all connection strings must specify `ssl=require` or `sslmode=require`. Unencrypted connections are rejected.
   - Separation of connection pools: Transactional application traffic uses pooled connections (`-pooler`); DDL schema migrations use direct connections.
2. **Cloudinary Asset Storage**:
   - PDF carousels are strictly handled with `resource_type="raw"` to prevent MIME corruption or invalid transformations.
   - Direct memory streaming avoids ephemeral disk writes on cloud container filesystems.

