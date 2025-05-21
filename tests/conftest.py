import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database.models import Base


@pytest.fixture
async def db_session():
    # Create an in-memory SQLite database for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

    await engine.dispose()
