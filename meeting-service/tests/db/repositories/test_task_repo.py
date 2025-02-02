import pytest
from tests.factories import TaskFactory

from app.db.repositories.task_repo import TaskRepository


@pytest.mark.asyncio
async def test_create_task(test_db_session):
    repo = TaskRepository(test_db_session)

    task_factory = TaskFactory.build()
    created_task = await repo.create(task_factory)

    assert created_task.title == task_factory.title


@pytest.mark.asyncio
async def test_get_task_by_id(test_db_session):
    repo = TaskRepository(test_db_session)

    task_factory = TaskFactory.build()
    created_task = await repo.create(task_factory)

    retrieved = await repo.get_by_id(created_task.id)
    assert retrieved.title == created_task.title


@pytest.mark.asyncio
async def test_update_task(test_db_session):
    repo = TaskRepository(test_db_session)

    task_factory = TaskFactory.build()
    created_task = await repo.create(task_factory)
    assert created_task.title == task_factory.title

    created_task.title = "Updated Task"
    updated_task = await repo.update(created_task)
    assert updated_task.title == "Updated Task"


@pytest.mark.asyncio
async def test_delete_task(test_db_session):
    repo = TaskRepository(test_db_session)

    task_factory = TaskFactory.build()
    created_task = await repo.create(task_factory)

    await repo.delete(created_task.id)
    deleted = await repo.get_by_id(created_task.id)
    assert deleted is None


@pytest.mark.asyncio
async def test_get_all_tasks(test_db_session):
    repo = TaskRepository(test_db_session)

    task1 = TaskFactory.build()
    task2 = TaskFactory.build()

    test_db_session.add_all([task1, task2])
    await test_db_session.commit()

    tasks = await repo.get_all()
    assert len(tasks) == 2
    assert tasks[0].title == task1.title
    assert tasks[1].title == task2.title
