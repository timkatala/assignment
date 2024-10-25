from uuid import UUID

from src.domain.models import Message
from src.infrastructure.repositories.base_repository import BaseRepository

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Message)

    async def get_by_sender_id(self, sender_id: UUID, limit: int = None, offset: int = None) -> list[Message]:
        messages = await self.list(limit=limit, offset=offset, filters=[Message.sender_id == sender_id])
        return messages

    async def soft_delete_by_sender_id(self, sender_id: UUID) -> None:
        query = (
            update(Message)
            .where(Message.sender_id == sender_id)
            .values(is_deleted=True)  # Mark as soft deleted and update timestamp
        )

        await self.session.execute(query)
        await self.session.commit()
