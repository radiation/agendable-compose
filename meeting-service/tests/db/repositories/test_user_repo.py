import uuid

import pytest
from app.db.models.user import User
from app.db.repositories.user_repo import UserRepository
from tests.factories import UserFactory


@pytest.mark.asyncio
async def test_create_user(test_db_session):
    """Test creating a user."""
    repo = UserRepository(test_db_session)

    user_factory = UserFactory.build()
    created_user = await repo.create(user_factory)

    assert created_user.email == user_factory.email
    assert created_user.first_name == user_factory.first_name
    assert created_user.last_name == user_factory.last_name


@pytest.mark.asyncio
async def test_get_user_by_id(test_db_session):
    """Test getting a user by ID."""
    repo = UserRepository(test_db_session)

    user_factory = UserFactory.build()
    created_user = await repo.create(user_factory)

    retrieved = await repo.get_by_id(created_user.id)
    assert retrieved.email == user_factory.email
    assert retrieved.first_name == user_factory.first_name
    assert retrieved.last_name == user_factory.last_name


@pytest.mark.asyncio
async def test_update_user(test_db_session):
    """Test updating a user."""
    repo = UserRepository(test_db_session)

    user_factory = UserFactory.build()
    created_user = await repo.create(user_factory)
    created_user.first_name = "Updated"
    created_user.last_name = "Name"

    updated_user = await repo.update(created_user)
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"


@pytest.mark.asyncio
async def test_delete_user(test_db_session):
    """Test deleting a user."""
    repo = UserRepository(test_db_session)

    user_factory = UserFactory.build()
    created_user = await repo.create(user_factory)

    await repo.delete(created_user.id)
    deleted = await repo.get_by_id(created_user.id)
    assert deleted is None


@pytest.mark.asyncio
async def test_get_all_users(test_db_session):
    """Test getting all users."""
    repo = UserRepository(test_db_session)

    user1 = User(
        id=uuid.uuid4(), email="test1@example.com", first_name="First", last_name="User"
    )
    user2 = User(
        id=uuid.uuid4(),
        email="test2@example.com",
        first_name="Second",
        last_name="User",
    )

    test_db_session.add_all([user1, user2])
    await test_db_session.commit()

    users = await repo.get_all()
    assert len(users) == 2
    assert users[0].email == "test1@example.com"
    assert users[1].email == "test2@example.com"
