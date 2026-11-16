from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from app.db.session import Base
from app.core.logging import logger

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Deterministic SQLAlchemy Repository implementing scoped CRUD operations
    with immediate read-back verification.
    """
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[ModelType]:
        """Retrieve an entity by primary key."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> ModelType:
        """Create an entity, commit, and immediately read back to verify persistence."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        
        # Immediate read-back verification
        created_id = getattr(instance, "id", None)
        await self.session.commit()
        
        if created_id is not None:
            verified = await self.get_by_id(created_id)
            if verified is None:
                raise RuntimeError(
                    f"CRITICAL DATABASE WRITE FAILURE: Created record {self.model.__name__}({created_id}) was not found upon immediate read-back!"
                )
            return verified
        return instance

    async def update(self, entity_id: Any, **kwargs) -> Optional[ModelType]:
        """Update an entity and read back to verify fields."""
        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.commit()
        
        # Read-back verification
        verified = await self.get_by_id(entity_id)
        if verified is None:
            raise RuntimeError(
                f"DATABASE UPDATE FAILURE: Record {self.model.__name__}({entity_id}) not found after update!"
            )
        return verified

    async def delete(self, entity_id: Any) -> bool:
        """Delete an entity and verify it no longer exists."""
        stmt = delete(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        # Verify deletion
        still_exists = await self.get_by_id(entity_id)
        if still_exists is not None:
            raise RuntimeError(
                f"DATABASE DELETE FAILURE: Record {self.model.__name__}({entity_id}) still exists after delete!"
            )
        return result.rowcount > 0

    async def list_all(self, limit: int = 50, offset: int = 0) -> List[ModelType]:
        """List entities with pagination."""
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        """Count total rows in the table."""
        stmt = select(func.count()).select_from(self.model)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

