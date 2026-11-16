import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class MCPServer(Base):
    __tablename__ = "mcp_servers"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # e.g. "research_server"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="CONNECTED")  # CONNECTED, DISCONNECTED, ERROR
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    tools = relationship("MCPTool", back_populates="server", cascade="all, delete-orphan")


class MCPTool(Base):
    __tablename__ = "mcp_tools"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)  # e.g. "research_server:search_web"
    server_id: Mapped[str] = mapped_column(String(50), ForeignKey("mcp_servers.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    input_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    is_dangerous: Mapped[bool] = mapped_column(Boolean, default=False)

    server = relationship("MCPServer", back_populates="tools")
    permissions = relationship("MCPToolPermission", back_populates="tool", cascade="all, delete-orphan")


class MCPToolPermission(Base):
    """Enforces least-privilege matrix: which agent can execute which tool."""
    __tablename__ = "mcp_tool_permissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id: Mapped[str] = mapped_column(String(50), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    tool_id: Mapped[str] = mapped_column(String(100), ForeignKey("mcp_tools.id", ondelete="CASCADE"), nullable=False)
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=True)

    agent = relationship("Agent", back_populates="permissions")
    tool = relationship("MCPTool", back_populates="permissions")

