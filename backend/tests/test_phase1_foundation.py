import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.core.encryption import encrypt_secret, decrypt_secret


@pytest.mark.asyncio
async def test_root_endpoint():
    """Verify root endpoint is operational."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == settings.APP_NAME
        assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_health_endpoint():
    """Verify health endpoint accurately reflects services status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data
        assert "database" in data["services"]
        assert "ollama" in data["services"]


def test_password_hashing():
    """Verify Argon2 password hashing and verification."""
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_tokens():
    """Verify JWT creation and decoding."""
    payload = {"sub": "user-uuid-123", "role": "admin"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user-uuid-123"
    assert decoded["role"] == "admin"


def test_secret_encryption():
    """Verify symmetric encryption and decryption for sensitive tokens at rest."""
    secret = "AQEDAT7q8Q4FF-sample-linkedin-access-token"
    encrypted = encrypt_secret(secret)
    assert encrypted != secret
    decrypted = decrypt_secret(encrypted)
    assert decrypted == secret
