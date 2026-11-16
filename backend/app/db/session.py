from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from app.core.logging import logger

# Base Model for all SQLAlchemy entities
class Base(DeclarativeBase):
    pass


# Initialize async engine if database is configured
_engine = None
_async_session_factory = None


def normalize_db_url(raw_url: str) -> str:
    """Ensure standard postgresql+asyncpg driver prefix and asyncpg-compatible SSL parameters."""
    url = raw_url.strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # asyncpg uses ssl=require rather than sslmode=require
    if "sslmode=require" in url:
        url = url.replace("sslmode=require", "ssl=require")
    elif "ssl=" not in url and ("neon.tech" in url or "prisma.io" in url or "aws" in url):
        url += ("&" if "?" in url else "?") + "ssl=require"

    return url


def get_engine():
    global _engine
    if _engine is None and settings.is_database_configured:
        db_url = normalize_db_url(settings.DATABASE_URL)
        _engine = create_async_engine(
            db_url,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            connect_args={"timeout": 3},
            echo=False,
            future=True,
        )
    return _engine


def get_session_factory():
    global _async_session_factory
    if _async_session_factory is None:
        try:
            engine = get_engine()
            if engine:
                _async_session_factory = async_sessionmaker(
                    bind=engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                    autoflush=False
                )
        except Exception as e:
            logger.warning(f"Could not initialize database session factory: {e}")
            _async_session_factory = None
    return _async_session_factory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for injecting an active SQLAlchemy async session."""
    factory = get_session_factory()
    if not factory:
        yield None
        return

    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rolled back: {e}")
            raise
        finally:
            await session.close()
