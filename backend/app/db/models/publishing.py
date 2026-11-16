import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class LinkedInAccount(Base):
    """Connected LinkedIn OAuth account with encrypted token storage."""
    __tablename__ = "linkedin_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    member_id: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    encrypted_access_token: Mapped[str] = mapped_column(Text, nullable=False)
    token_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_connected: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="linkedin_accounts")
    published_posts = relationship("PublishedPost", back_populates="account")


class PublishedPost(Base):
    """Immutable audit record of posts published to LinkedIn."""
    __tablename__ = "published_posts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    linkedin_account_id: Mapped[str] = mapped_column(String(36), ForeignKey("linkedin_accounts.id"), nullable=True)
    content_version_id: Mapped[str] = mapped_column(String(36), nullable=False)
    linkedin_urn: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    post_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    publishing_status: Mapped[str] = mapped_column(String(50), default="PUBLISHED")
    api_response: Mapped[dict] = mapped_column(JSON, default=dict)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    account = relationship("LinkedInAccount", back_populates="published_posts")
