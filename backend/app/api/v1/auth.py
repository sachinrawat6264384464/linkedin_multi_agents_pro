from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timezone
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token, oauth2_scheme
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# Seed admin user credentials for local bootstrap
# In production with DB configured, this checks Neon PostgreSQL
BOOTSTRAP_ADMIN = {
    "id": "00000000-0000-0000-0000-000000000001",
    "email": "admin@agentos.local",
    "password_hash": get_password_hash("Admin123!"),
    "role": "admin",
    "name": "Lead Architect",
    "is_active": True
}


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    """Dependency for authenticating API requests."""
    if not token:
        # Development fallback allows unauthenticated access in local development if configured
        if settings.APP_DEBUG:
            return BOOTSTRAP_ADMIN
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role", "user"),
        "name": payload.get("name", "User")
    }


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Authenticate user with email and password, returning JWT access token."""
    if credentials.email == BOOTSTRAP_ADMIN["email"] and verify_password(credentials.password, BOOTSTRAP_ADMIN["password_hash"]):
        token = create_access_token({
            "sub": BOOTSTRAP_ADMIN["id"],
            "email": BOOTSTRAP_ADMIN["email"],
            "role": BOOTSTRAP_ADMIN["role"],
            "name": BOOTSTRAP_ADMIN["name"]
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": BOOTSTRAP_ADMIN["id"],
                "email": BOOTSTRAP_ADMIN["email"],
                "name": BOOTSTRAP_ADMIN["name"],
                "role": BOOTSTRAP_ADMIN["role"]
            }
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Retrieve currently authenticated user profile."""
    return current_user
