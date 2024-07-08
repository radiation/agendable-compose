from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeetingRecurrenceBase(BaseModel):
    frequency: str
    week_day: Optional[int]
    month_week: Optional[int]
    interval: int
    end_recurrence: Optional[datetime]


class MeetingBase(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    duration: int
    location: str
    notes: str
    num_reschedules: int
    reminder_sent: bool


class MeetingCreate(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: int
    recurrence: Optional[MeetingRecurrenceBase]

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime]
    completed: bool
    completed_date: Optional[datetime]


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    assignee_id: int

    class Config:
        orm_mode = True


class MeetingTaskBase(BaseModel):
    meeting_id: int
    task_id: int


class MeetingTaskCreate(MeetingTaskBase):
    pass


class MeetingTask(MeetingTaskBase):
    id: int

    class Config:
        orm_mode = True
