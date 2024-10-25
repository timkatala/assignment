import pytest

from sqlalchemy.exc import IntegrityError

from src.domain.models import User
from src.infrastructure.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_create_user(session_fixture):
    user_repo = UserRepository(session_fixture)
    new_user = User(name="John Doe", email="john@example.com")

    created_user = await user_repo.create(new_user)

    assert created_user.id is not None
    assert created_user.name == "John Doe"
    assert created_user.email == "john@example.com"


@pytest.mark.asyncio
async def test_get_by_id(session_fixture):
    user_repo = UserRepository(session_fixture)
    new_user = User(name="Jane Doe", email="jane@example.com")

    created_user = await user_repo.create(new_user)

    fetched_user = await user_repo.get_by_id(created_user.id)

    assert fetched_user.id == created_user.id
    assert fetched_user.name == "Jane Doe"


@pytest.mark.asyncio
async def test_soft_delete_user(session_fixture, user):
    user_repo = UserRepository(session_fixture)

    # Soft delete the user
    await user_repo.soft_delete(user.id)

    # Try to fetch the user, expecting None due to soft delete
    deleted_user = await user_repo.get_by_id(user.id)

    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_by_email(session_fixture, user):
    user_repo = UserRepository(session_fixture)

    result = await user_repo.get_by_email(user.email)

    assert user == result


@pytest.mark.asyncio
async def test_list_users_with_pagination(session_fixture):
    user_repo = UserRepository(session_fixture)

    for i in range(10):
        await user_repo.create(User(name=f"User {i}", email=f"user{i}@example.com"))

    # Fetch users with pagination (limit 5, offset 0)
    users = await user_repo.list_users(limit=5, offset=0)

    # Assert that we get 5 users in the result
    assert len(users) == 5

    users_offset = await user_repo.list_users(limit=5, offset=5)

    assert len(users_offset) == 5
    assert users_offset[0].name == "User 5"


@pytest.mark.asyncio
async def test_list_active_users(session_fixture, users):
    user_repo = UserRepository(session_fixture)

    # Soft delete one user
    await user_repo.soft_delete(users[3].id)

    # List all active users
    users = await user_repo.list_users()

    # Assert that only 4 users are active (1 is soft deleted)
    assert len(users) == 4


@pytest.mark.asyncio
async def test_update_user(session_fixture, user):
    user_repo = UserRepository(session_fixture)
    user.name = "New name"

    updated_user = await user_repo.update(user.id, user)

    assert updated_user.id == user.id
    assert updated_user.name == "New name"
    assert updated_user.email == user.email


@pytest.mark.asyncio
async def test_update_user_unique_violation_email(session_fixture, user):
    user_repo = UserRepository(session_fixture)

    new_user = User(name="John Doe", email="john.doe@example.com")
    await user_repo.create(new_user)

    new_user.email = user.email

    with pytest.raises(IntegrityError):
        await user_repo.update(new_user.id, new_user)


@pytest.mark.asyncio
async def test_create_user_unique_violation_email(session_fixture, user):
    user_repo = UserRepository(session_fixture)
    new_user = User(name="John Doe", email=user.email)

    with pytest.raises(IntegrityError):
        await user_repo.create(new_user)
