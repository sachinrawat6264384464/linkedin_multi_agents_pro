import uuid
import hashlib
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class ContentDraft(Base):
    __tablename__ = "content_drafts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="AI Engineering")
    target_audience: Mapped[str] = mapped_column(String(255), default="Software Engineers")
    current_version_id: Mapped[str] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="drafts")
    versions = relationship("ContentVersion", back_populates="draft", cascade="all, delete-orphan")


class ContentVersion(Base):
    """Immutable version of drafted LinkedIn content."""
    __tablename__ = "content_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    draft_id: Mapped[str] = mapped_column(String(36), ForeignKey("content_drafts.id", ondelete="CASCADE"), index=True, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    hook: Mapped[str] = mapped_column(Text, nullable=False)
    main_body: Mapped[str] = mapped_column(Text, nullable=False)
    hashtags: Mapped[list] = mapped_column(JSON, default=list)
    cta: Mapped[str] = mapped_column(String(255), nullable=True)
    references: Mapped[list] = mapped_column(JSON, default=list)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    quality_report: Mapped[dict] = mapped_column(JSON, default=dict)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    draft = relationship("ContentDraft", back_populates="versions")

    @staticmethod
    def calculate_checksum(hook: str, main_body: str, cta: str = "") -> str:
        """Generate SHA-256 fingerprint of the immutable content text."""
        content_string = f"{hook.strip()}|{main_body.strip()}|{(cta or '').strip()}"
        return hashlib.sha256(content_string.encode("utf-8")).hexdigest()


class ResearchSource(Base):
    """Verified research references collected by the Research Agent."""
    __tablename__ = "research_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_findings: Mapped[list] = mapped_column(JSON, default=list)
    publication_date: Mapped[str] = mapped_column(String(50), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED")  # VERIFIED, UNVERIFIED, CONFLICT
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="research_sources")

