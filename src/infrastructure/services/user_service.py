import logging

from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.domain.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from src.domain.models import User
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.message import MessageRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository, message_repository: MessageRepository):
        """
        Initializes the UserService with user and message repository dependencies.

        Parameters:
            user_repository (UserRepository): Repository for accessing user-related data.
            message_repository (MessageRepository): Repository for accessing message-related data.
        """
        self.user_repository = user_repository
        self.message_repository = message_repository

    async def create_user(self, user: User) -> User:
        """
        Creates a new user if the email is unique.
        """
        try:
            user = await self.user_repository.create(user)
            return user
        except IntegrityError:
            logger.info(f"User with email {user.email} already exists.")
            raise UserAlreadyExistsException(f"User with email {user.email} already exists.")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.
        """
        return await self.user_repository.get_by_email(email)

    async def update_user(self, user_id: UUID, user: User) -> User:
        """
        Updates an existing user's information.
        """
        try:
            return await self.user_repository.update(user_id, user)
        except IntegrityError:
            logger.info(f"User with email {user.email} already exists.")
            raise UserAlreadyExistsException(f"User with email {user.email} already exists.")

    async def delete_user(self, user_id: UUID):
        """
        Soft deletes a user by their ID, along with all messages sent by them.
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            logger.info(f"User with ID {user_id} not found.")
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        await self.user_repository.soft_delete(user_id)
        await self.message_repository.soft_delete_by_sender_id(sender_id=user_id)
