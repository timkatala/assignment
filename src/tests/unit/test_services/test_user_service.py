from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from src.domain.exceptions.user import UserNotFoundException, UserAlreadyExistsException
from src.domain.models import User
from src.infrastructure.services.user_service import UserService


@pytest.mark.asyncio
class TestUserService:
    @pytest.fixture
    def user_service(self):
        # Create mock repositories
        user_repository = AsyncMock()
        message_repository = AsyncMock()

        # Create the UserService with the mocked dependencies
        return UserService(user_repository=user_repository, message_repository=message_repository)

    @pytest.fixture
    def user(self):
        return User(id=uuid4(), name="John Doe", email="johndoe@example.com")

    @pytest.fixture
    def user_data(self):
        return {"name": "John Doe", "email": "johndoe@example.com"}

    async def test_create_user_success(self, user_service, user):
        user_service.user_repository.create.return_value = user

        result = await user_service.create_user(user)

        user_service.user_repository.create.assert_awaited_once_with(user)
        assert result == user

    async def test_create_user_duplicate_email(self, user_service, user):
        # Simulate IntegrityError for duplicate email
        user_service.user_repository.create.side_effect = IntegrityError(
            "duplicate key value violates unique constraint", None, None
        )

        with pytest.raises(UserAlreadyExistsException) as e:
            await user_service.create_user(user)

        assert str(e.value) == f"User with email {user.email} already exists."

    async def test_get_user_by_email_found(self, user_service, user):
        user_service.user_repository.get_by_email.return_value = user

        result = await user_service.get_user_by_email(user.email)

        assert result == user

    async def test_get_user_by_email_not_found(self, user_service):
        user_service.user_repository.get_by_email.return_value = None

        result = await user_service.get_user_by_email("unknown@example.com")

        assert result is None

    async def test_update_user(self, user_service, user):
        user_service.user_repository.update.return_value = user

        result = await user_service.update_user(user.id, user)

        assert result == user

    async def test_delete_user_success(self, user_service, user):
        user_service.user_repository.get_by_id.return_value = user
        user_service.user_repository.soft_delete.return_value = None
        user_service.message_repository.soft_delete_by_sender_id.return_value = None

        await user_service.delete_user(user.id)

        user_service.user_repository.get_by_id.assert_awaited_once_with(user.id)
        user_service.user_repository.soft_delete.assert_awaited_once_with(user.id)
        user_service.message_repository.soft_delete_by_sender_id.assert_awaited_once_with(sender_id=user.id)

    async def test_delete_user_not_found(self, user_service):
        user_service.user_repository.get_by_id.return_value = None
        user_id = uuid4()

        with pytest.raises(UserNotFoundException) as e:
            await user_service.delete_user(user_id)

        assert str(e.value) == f"User with ID {user_id} not found."
