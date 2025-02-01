"""
Fixtures for testing the FastAPI application
"""

from unittest.mock import AsyncMock

import pytest
from app.core.dependencies import (
    get_meeting_service,
    get_recurrence_service,
    get_task_service,
    get_user_service,
)
from app.db.db import get_db
from app.db.models import Base
from app.db.repositories.meeting_repo import MeetingRepository
from app.db.repositories.recurrence_repo import RecurrenceRepository
from app.db.repositories.task_repo import TaskRepository
from app.db.repositories.user_repo import UserRepository
from app.main import app
from app.services import MeetingService, RecurrenceService, TaskService, UserService
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(name="test_engine", scope="session")
async def _test_engine():
    """Create a new test database for the entire test session"""
    _engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield _engine
    await _engine.dispose()


@pytest.fixture(scope="session")
async def tables(test_engine):
    """Create tables for the test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(name="test_db_session", scope="function")
async def _test_db_session(test_engine):
    """Create a new test session for each test function"""
    async_session_factory = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        yield session

    await test_engine.dispose()


@pytest.fixture(name="test_mock_redis")
async def _test_mock_redis():
    """Mock Redis client for testing"""
    mock = AsyncMock()
    mock.publish = AsyncMock()
    return mock


@pytest.fixture
async def test_client(test_db_session, test_mock_redis):
    """Test client with dependency overrides for services"""
    app.dependency_overrides[get_db] = lambda: test_db_session

    app.dependency_overrides[get_meeting_service] = lambda: MeetingService(
        MeetingRepository(test_db_session), test_mock_redis
    )

    app.dependency_overrides[get_recurrence_service] = lambda: RecurrenceService(
        RecurrenceRepository(test_db_session), test_mock_redis
    )

    app.dependency_overrides[get_task_service] = lambda: TaskService(
        TaskRepository(test_db_session), test_mock_redis
    )

    app.dependency_overrides[get_user_service] = lambda: UserService(
        UserRepository(test_db_session), test_mock_redis
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
async def meeting_service(test_db_session, test_mock_redis):
    """Create a new MeetingService instance for each test function"""
    repo = MeetingRepository(test_db_session)
    service = MeetingService(repo, test_mock_redis)
    return service


@pytest.fixture
async def recurrence_service(test_db_session, test_mock_redis):
    """Create a new RecurrenceService instance for each test function"""
    repo = RecurrenceRepository(test_db_session)
    service = RecurrenceService(repo, test_mock_redis)
    return service


@pytest.fixture
async def task_service(test_db_session, test_mock_redis):
    """Create a new TaskService instance for each test function"""
    repo = TaskRepository(test_db_session)
    service = TaskService(repo, test_mock_redis)
    return service


@pytest.fixture
async def user_service(test_db_session, test_mock_redis):
    """Create a new UserService instance for each test function"""
    repo = UserRepository(test_db_session)
    service = UserService(repo, test_mock_redis)
    return service
