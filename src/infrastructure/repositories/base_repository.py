from datetime import datetime
from typing import TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import IntegrityError

ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, session: AsyncSession, model: ModelType):
        self.session = session
        self.model = model  # Store the model type for later use

    async def create(self, obj: ModelType) -> ModelType:
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)  # Fetches the newly created record
            return obj
        except IntegrityError as e:
            await self.session.rollback()
            raise e

    async def get_by_id(self, id: UUID) -> ModelType:
        stmt = self._active_query().filter(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, obj_id: UUID, obj: ModelType) -> ModelType:
        try:
            obj.updated_at = datetime.utcnow()
            stmt = (
                update(self.model)
                .where(self.model.id == obj_id)
                .values(**obj.model_dump(exclude_unset=True))
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return await self.get_by_id(obj_id)
        except IntegrityError as e:
            await self.session.rollback()
            raise e

    async def soft_delete(self, id: UUID) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(is_deleted=True)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def hard_delete(self, id: UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id).execution_options(synchronize_session="fetch")
        await self.session.execute(stmt)
        await self.session.commit()

    async def list(self, filters: list = None, limit: int = None, offset: int = None) -> list[ModelType]:
        query = self._active_query().filter(*filters or [])

        # Apply pagination
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    def _active_query(self):
        """Return a query that filters out deleted records by default."""
        return select(self.model).filter(self.model.is_deleted == False)  # noqa
