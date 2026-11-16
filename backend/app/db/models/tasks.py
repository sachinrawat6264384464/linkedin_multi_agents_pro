import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="AI Engineering")
    target_audience: Mapped[str] = mapped_column(String(255), default="Software Engineers & CTOs")
    status: Mapped[str] = mapped_column(String(50), default="PENDING", index=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    workflow_runs = relationship("WorkflowRun", back_populates="task", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="task", cascade="all, delete-orphan")
    drafts = relationship("ContentDraft", back_populates="task", cascade="all, delete-orphan")
    research_sources = relationship("ResearchSource", back_populates="task", cascade="all, delete-orphan")
    media_assets = relationship("GeneratedMedia", back_populates="task", cascade="all, delete-orphan")


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    execution_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    current_step: Mapped[str] = mapped_column(String(100), default="START")
    status: Mapped[str] = mapped_column(String(50), default="RUNNING", index=True)
    retry_count: Mapped[int] = mapped_column(default=0)
    error_details: Mapped[str] = mapped_column(Text, nullable=True)
    state_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    task = relationship("Task", back_populates="workflow_runs")


class WorkflowCheckpoint(Base):
    """PostgreSQL durable persistence for LangGraph workflow state."""
    __tablename__ = "workflow_checkpoints"

    thread_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    checkpoint_ns: Mapped[str] = mapped_column(String(64), primary_key=True, default="")
    checkpoint_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    parent_checkpoint_id: Mapped[str] = mapped_column(String(64), nullable=True)
    checkpoint_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    metadata_data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Approval(Base):
    """Durable record of human approval with version checksum verification."""
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), index=True, nullable=False)
    content_version_id: Mapped[str] = mapped_column(String(36), nullable=True)
    approval_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "TASK_START" or "FINAL_PUBLISH"
    status: Mapped[str] = mapped_column(String(50), default="PENDING", index=True)  # PENDING, APPROVED, REJECTED, REVISE
    version_checksum: Mapped[str] = mapped_column(String(64), nullable=True)
    reviewer_notes: Mapped[str] = mapped_column(Text, nullable=True)
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="approvals")
