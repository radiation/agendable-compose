"""
This module contains the SQLAlchemy relationship tables for the many-to-many
relationships between meetings and tasks, and meetings and users.
"""

from app.db.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, text
from sqlalchemy.dialects.postgresql import UUID

meeting_tasks = Table(
    "meeting_tasks",
    Base.metadata,
    Column(
        "meeting_id",
        Integer,
        ForeignKey("meetings.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "created_at", DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    ),
)

meeting_users = Table(
    "meeting_users",
    Base.metadata,
    Column(
        "meeting_id",
        Integer,
        ForeignKey("meetings.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at", DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    ),
)
