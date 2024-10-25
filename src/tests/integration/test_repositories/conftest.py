import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from src.domain.models import User, Message

# Use an SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///test.db"

# Create an async engine for testing
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True}, poolclass=NullPool, echo=True
)

# Async session for database transactions
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    """
    Fixture to create the database schema and provide a session for the tests.
    Rolls back the session after each test to ensure test isolation.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def session_fixture() -> AsyncSession:
    """
    Fixture to create a new session for each test.
    """
    async with AsyncSessionLocal() as session:

        yield session
        await session.rollback()  # Rollback after test for isolation


@pytest_asyncio.fixture
async def user(session_fixture):
    # Create a test user
    test_user = User(name="Test User", email="test@example.com")
    session_fixture.add(test_user)
    await session_fixture.commit()
    await session_fixture.refresh(test_user)
    yield test_user


@pytest_asyncio.fixture
async def users(session_fixture):
    user_list = []

    # Create multiple users
    for i in range(5):
        new_user = User(name=f"User {i}", email=f"user{i}@example.com")
        session_fixture.add(new_user)
        await session_fixture.commit()
        await session_fixture.refresh(new_user)
        user_list.append(new_user)

    yield user_list


@pytest_asyncio.fixture
async def messages(session_fixture, user):
    message_list = []

    for i in range(10):
        new_message = Message(sender_id=user.id, content=f"Message {i} content", cceated_at="2024-10-22T12:00:00")
        session_fixture.add(new_message)
        await session_fixture.commit()
        await session_fixture.refresh(new_message)
        message_list.append(new_message)

    yield message_list
