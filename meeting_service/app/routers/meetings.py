import crud.meeting_crud as crud
import db
from fastapi import APIRouter, Depends, HTTPException
from schemas import meeting_schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Create a new meeting
@router.post("/", response_model=meeting_schemas.Meeting)
async def create_meeting(
    meeting: meeting_schemas.MeetingCreate, db: AsyncSession = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    return await crud.create_meeting(db=db, meeting=meeting)


# List all meetings
@router.get("/", response_model=list[meeting_schemas.Meeting])
async def get_meetings(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[meeting_schemas.Meeting]:
    return await crud.get_meetings(db=db, skip=skip, limit=limit)


# Get a meeting by ID
@router.get("/{meeting_id}", response_model=meeting_schemas.Meeting)
async def get_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> meeting_schemas.Meeting:
    db_meeting = await crud.get_meeting(db=db, meeting_id=meeting_id)
    if db_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return db_meeting


# Update an existing meeting
@router.put("/{meeting_id}", response_model=meeting_schemas.Meeting)
async def update_meeting(
    meeting_id: int,
    meeting: meeting_schemas.MeetingUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.Meeting:
    updated_meeting = await crud.update_meeting(
        db=db, meeting_id=meeting_id, meeting=meeting
    )
    if updated_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return updated_meeting


# Delete a meeting
@router.delete("/{meeting_id}", status_code=204)
async def delete_meeting(meeting_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await crud.delete_meeting(db=db, meeting_id=meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meeting not found")


# Complete a meeting and roll tasks over to the next occurrence
@router.post("/{meeting_id}/complete/", response_model=dict)
async def complete_meeting(meeting_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await crud.complete_meeting(db=db, meeting_id=meeting_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Meeting not found or already completed"
        )
    return {"message": "Meeting completed"}


# Add a recurrence to a meeting
@router.post("/{meeting_id}/add_recurrence/", response_model=meeting_schemas.Meeting)
async def add_recurrence(
    meeting_id: int,
    recurrence_data: meeting_schemas.MeetingRecurrenceCreate,
    db: AsyncSession = Depends(db.get_db),
):
    meeting = await crud.add_recurrence(
        db=db, meeting_id=meeting_id, recurrence_data=recurrence_data
    )
    if meeting is None:
        raise
