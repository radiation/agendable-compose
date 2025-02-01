"""
Application dependencies.
"""

from app.core.redis_client import redis_client
from app.db.db import get_db
from app.db.repositories.meeting_repo import MeetingRepository
from app.db.repositories.recurrence_repo import RecurrenceRepository
from app.db.repositories.task_repo import TaskRepository
from app.db.repositories.user_repo import UserRepository
from app.services import MeetingService, RecurrenceService, TaskService, UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_redis_client():
    """Get the Redis client"""
    return redis_client


def get_meeting_repo(db: AsyncSession = Depends(get_db)) -> MeetingRepository:
    """Get the Meeting repository"""
    return MeetingRepository(db)


def get_meeting_service(
    db: AsyncSession = Depends(get_db), redis=Depends(lambda: redis_client)
) -> MeetingService:
    """Get the Meeting service"""
    meeting_repo = MeetingRepository(db)
    return MeetingService(meeting_repo, redis_client=redis)


def get_recurrence_repo(
    db: AsyncSession = Depends(get_db),
) -> RecurrenceRepository:
    """Get the Recurrence repository"""
    return RecurrenceRepository(db)


def get_recurrence_service(
    db: AsyncSession = Depends(get_db), redis=Depends(lambda: redis_client)
) -> RecurrenceService:
    """Get the Recurrence service"""
    recurrence_repo = RecurrenceRepository(db)
    return RecurrenceService(recurrence_repo, redis_client=redis)


def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    """Get the Task repository"""
    return TaskRepository(db)


def get_task_service(
    db: AsyncSession = Depends(get_db), redis=Depends(lambda: redis_client)
) -> TaskService:
    """Get the Task service"""
    task_repo = TaskRepository(db)
    return TaskService(task_repo, redis_client=redis)


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Get the User repository"""
    return UserRepository(db)


def get_user_service(
    db: AsyncSession = Depends(get_db), redis=Depends(lambda: redis_client)
) -> UserService:
    """Get the User service"""
    user_repo = UserRepository(db)
    return UserService(user_repo, redis_client=redis)
