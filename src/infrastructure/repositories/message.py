from uuid import UUID

from sqlmodel import select

from src.domain.models import Message
from src.infrastructure.repositories.base_repository import BaseRepository

from sqlalchemy import update, func
from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Message)

    async def get_by_sender_id(self, sender_id: UUID, limit: int = None, offset: int = None) -> list[Message]:
        messages = await self.list(limit=limit, offset=offset, filters=[Message.sender_id == sender_id])
        return messages

    async def get_by_sender_id_count(self, sender_id: UUID) -> int:
        query = (
            select(func.count())
            .select_from(Message)
            .where(Message.is_deleted == False, Message.sender_id == sender_id)  # noqa
        )
        total_count = await self.session.execute(query)
        return total_count.scalar_one()

    async def soft_delete_by_sender_id(self, sender_id: UUID) -> None:
        query = (
            update(Message)
            .where(Message.sender_id == sender_id)
            .values(is_deleted=True)  # Mark as soft deleted and update timestamp
        )

        await self.session.execute(query)
        await self.session.commit()
