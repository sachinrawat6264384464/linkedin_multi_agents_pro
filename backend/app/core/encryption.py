import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings


def _get_fernet() -> Fernet:
    """Derive a stable 32-byte Fernet key from APP_ENCRYPTION_KEY and APP_SECRET_KEY."""
    raw_key = (settings.APP_ENCRYPTION_KEY + settings.APP_SECRET_KEY).encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"agentos_salt_2026",
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(raw_key))
    return Fernet(key)


def encrypt_secret(plain_text: str) -> str:
    """Encrypt a secret string (e.g. OAuth access token) for safe database storage."""
    if not plain_text:
        return ""
    f = _get_fernet()
    encrypted_bytes = f.encrypt(plain_text.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")


def decrypt_secret(encrypted_text: str) -> str:
    """Decrypt an encrypted secret string from the database."""
    if not encrypted_text:
        return ""
    try:
        f = _get_fernet()
        decrypted_bytes = f.decrypt(encrypted_text.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except Exception:
        return ""
