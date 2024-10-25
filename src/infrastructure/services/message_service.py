import logging

from typing import List
from uuid import UUID

from src.domain.exceptions.message import MessageNotFoundException
from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import Message
from src.infrastructure.repositories.message import MessageRepository
from src.infrastructure.repositories.user import UserRepository

logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self, user_repository: UserRepository, message_repository: MessageRepository):
        """
        Initializes the MessageService with user and message repository dependencies.
        """
        self.user_repository = user_repository
        self.message_repository = message_repository

    async def create_message(self, message: Message) -> Message:
        """
        Creates a new message if the sender exists.
        """
        sender = await self.user_repository.get_by_id(message.sender_id)
        if sender is None:
            logger.info(f"User with ID {message.sender_id} not found for {message.id}.")
            raise UserNotFoundException(f"Sender with ID {message.sender_id} not found.")

        return await self.message_repository.create(message)

    async def get_mesages_by_sender_id(self, sender_id: UUID) -> List[Message]:
        """
        Retrieves all messages sent by a specific user.
        """
        return await self.message_repository.get_by_sender_id(sender_id=sender_id)

    async def delete_message(self, message_id: UUID) -> None:
        """
        Soft deletes a message by its ID, if it exists.
        """
        message = await self.message_repository.get_by_id(message_id)
        if message is None:
            raise MessageNotFoundException(f"Message with ID {message_id} not found.")

        await self.message_repository.soft_delete(message_id)
