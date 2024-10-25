from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_URL = settings.database_url

# Create the async engine using asyncpg
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create the sessionmaker for async operations
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
