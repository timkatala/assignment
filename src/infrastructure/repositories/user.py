from typing import Optional

from src.domain.models import User
from src.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = self._active_query().filter(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list_users(self, limit: int = None, offset: int = None) -> list[User]:
        # Use the list method from BaseRepository with pagination
        users = await self.list(limit=limit, offset=offset)
        return users
