import pytest
from sqlalchemy import select

from src.domain.models import Message
from src.infrastructure.repositories.message import MessageRepository


@pytest.mark.asyncio
async def test_create_message(session_fixture, user):
    message_repo = MessageRepository(session_fixture)
    new_message = Message(sender_id=user.id, content="Lorem ipsum")

    created_message = await message_repo.create(new_message)

    assert created_message.id is not None
    assert created_message.sender_id == user.id
    assert created_message.content == "Lorem ipsum"


@pytest.mark.asyncio
async def test_get_by_sender_id(session_fixture, user, messages):
    message_repo = MessageRepository(session_fixture)

    sender_messages = await message_repo.get_by_sender_id(user.id)

    assert sender_messages == messages


@pytest.mark.asyncio
async def test_soft_delete_message(session_fixture, messages):
    message_repo = MessageRepository(session_fixture)
    message = messages[0]

    await message_repo.soft_delete(message.id)

    deleted_user = await message_repo.get_by_id(message.id)

    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_by_sender_id_with_pagination(session_fixture, user, messages):
    message_repo = MessageRepository(session_fixture)

    messages = await message_repo.get_by_sender_id(sender_id=user.id, limit=5, offset=0)

    assert len(messages) == 5

    messages_offset = await message_repo.get_by_sender_id(sender_id=user.id, limit=5, offset=5)

    assert len(messages_offset) == 5
    assert messages_offset[0].content == "Message 5 content"


@pytest.mark.asyncio
async def test_get_by_sender_id_active_messages(session_fixture, user, messages):
    message_repo = MessageRepository(session_fixture)

    # Soft delete one message
    await message_repo.soft_delete(messages[3].id)

    # List all active messages of user
    users = await message_repo.get_by_sender_id(sender_id=user.id)

    # Assert that only 9 messages are active (1 is soft deleted)
    assert len(users) == 9


@pytest.mark.asyncio
async def test_soft_delete_by_sender_id(session_fixture, messages, user):
    message_repo = MessageRepository(session_fixture)

    # Soft delete messages by sender_id
    await message_repo.soft_delete_by_sender_id(sender_id=user.id)

    # Verify that the messages are soft deleted
    query = select(Message).where(Message.sender_id == user.id)
    result = await session_fixture.execute(query)
    messages = result.scalars().all()

    assert all(message.is_deleted for message in messages)
