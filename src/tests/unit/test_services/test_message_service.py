from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from src.domain.exceptions.message import MessageNotFoundException
from src.domain.exceptions.user import UserNotFoundException
from src.domain.models import Message
from src.infrastructure.services.message_service import MessageService


class TestMessageService:
    @pytest_asyncio.fixture
    def message_service(self):
        user_repository = AsyncMock()
        message_repository = AsyncMock()
        return MessageService(user_repository=user_repository, message_repository=message_repository)

    @pytest_asyncio.fixture
    def user(self):
        return {"id": uuid4(), "name": "Test User", "email": "testuser@example.com"}

    @pytest_asyncio.fixture
    def message(self, user):
        return Message(
            id=uuid4(),
            sender_id=user["id"],
            recipient_id=uuid4(),
            content="This is a test message.",
            timestamp=datetime.utcnow(),
        )

    @pytest.mark.asyncio
    async def test_create_message_success(self, message_service, user, message):
        message_service.user_repository.get_by_id.return_value = user

        message_service.message_repository.create.return_value = message

        result = await message_service.create_message(message)

        message_service.user_repository.get_by_id.assert_awaited_once_with(message.sender_id)
        message_service.message_repository.create.assert_awaited_once_with(message)

        assert result == message

    @pytest.mark.asyncio
    async def test_create_message_user_not_found(self, message_service, message):
        message_service.user_repository.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            await message_service.create_message(message)

        message_service.user_repository.get_by_id.assert_awaited_once_with(message.sender_id)

    @pytest.mark.asyncio
    async def test_get_messages_by_sender_id_success(self, message_service, message):
        message_service.message_repository.get_by_sender_id.return_value = [message]

        result = await message_service.get_mesages_by_sender_id(message.sender_id)

        message_service.message_repository.get_by_sender_id.assert_awaited_once_with(sender_id=message.sender_id)
        assert result == [message]

    @pytest.mark.asyncio
    async def test_get_messages_by_sender_id_no_messages(self, message_service):
        sender_id = uuid4()

        message_service.message_repository.get_by_sender_id.return_value = []

        result = await message_service.get_mesages_by_sender_id(sender_id)

        message_service.message_repository.get_by_sender_id.assert_awaited_once_with(sender_id=sender_id)
        assert result == []

    @pytest.mark.asyncio
    async def test_delete_message_success(self, message_service, message):
        message_service.message_repository.get_by_id.return_value = message

        message_service.message_repository.soft_delete.return_value = None

        await message_service.delete_message(message.id)

        message_service.message_repository.get_by_id.assert_awaited_once_with(message.id)
        message_service.message_repository.soft_delete.assert_awaited_once_with(message.id)

    @pytest.mark.asyncio
    async def test_delete_message_not_found(self, message_service):
        message_id = uuid4()

        message_service.message_repository.get_by_id.return_value = None

        with pytest.raises(MessageNotFoundException):
            await message_service.delete_message(message_id)

        message_service.message_repository.get_by_id.assert_awaited_once_with(message_id)
