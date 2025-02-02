"""
Routes for meeting management.
"""

from fastapi import APIRouter, Depends

from app.core.decorators import log_execution_time
from app.core.dependencies import get_meeting_service
from app.core.logging_config import logger
from app.exceptions import NotFoundError
from app.schemas import (
    AddUsersRequest,
    MeetingCreate,
    MeetingCreateBatch,
    MeetingRetrieve,
    MeetingUpdate,
)
from app.services.meeting_service import MeetingService

router = APIRouter()


@router.post("/", response_model=MeetingRetrieve)
@log_execution_time
async def create_meeting(
    meeting: MeetingCreate,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingRetrieve:
    """
    Create a new meeting with the provided data.
    """
    logger.info(f"Creating meeting with data: {meeting.model_dump()}")
    return await service.create(meeting)


@router.get("/", response_model=list[MeetingRetrieve])
@log_execution_time
async def get_meetings(
    skip: int = 0,
    limit: int = 10,
    service: MeetingService = Depends(get_meeting_service),
) -> list[MeetingRetrieve]:
    """
    Fetch all meetings with pagination.
    """
    logger.info(f"Fetching all meetings with skip={skip} and limit={limit}")
    result = await service.get_all(skip, limit)
    logger.info(f"Retrieved {len(result)} meetings.")
    return result


@router.get("/{meeting_id}", response_model=MeetingRetrieve)
@log_execution_time
async def get_meeting(
    meeting_id: int,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingRetrieve:
    """
    Fetch a meeting by its ID.
    """
    logger.info(f"Fetching meeting with ID: {meeting_id}")
    meeting = await service.get_by_id(meeting_id)
    if meeting is None:
        logger.warning(f"Meeting with ID {meeting_id} not found")
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    logger.info(f"Meeting retrieved: {meeting}")
    return meeting


@router.put("/{meeting_id}", response_model=MeetingRetrieve)
@log_execution_time
async def update_meeting(
    meeting_id: int,
    meeting: MeetingUpdate,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingRetrieve:
    """
    Update a meeting with the provided data.
    """
    logger.info(
        f"Updating meeting with ID: {meeting_id} and data: {meeting.model_dump()}"
    )
    updated_meeting = await service.update(meeting_id, meeting)
    if updated_meeting is None:
        logger.warning(f"Meeting with ID {meeting_id} not found")
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    logger.info(f"Meeting updated successfully: {updated_meeting}")
    return updated_meeting


@router.delete("/{meeting_id}", status_code=204)
@log_execution_time
async def delete_meeting(
    meeting_id: int, service: MeetingService = Depends(get_meeting_service)
):
    """
    Delete a meeting by its ID.
    """
    logger.info(f"Deleting meeting with ID: {meeting_id}")
    success = await service.delete(meeting_id)
    if not success:
        logger.warning(f"Meeting with ID {meeting_id} not found")
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    logger.info(f"Meeting with ID {meeting_id} deleted successfully.")


@router.post("/{meeting_id}/complete/", response_model=MeetingRetrieve)
@log_execution_time
async def complete_meeting(
    meeting_id: int,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingRetrieve:
    """
    Complete a meeting by its ID.
    """
    logger.info(f"Completing meeting with ID: {meeting_id}")
    completed_meeting = await service.complete_meeting(meeting_id)
    if not completed_meeting:
        logger.warning(f"Meeting with ID {meeting_id} not found or already completed")
        raise NotFoundError(
            detail=f"Meeting with ID {meeting_id} not found or already completed"
        )
    logger.info(f"Meeting completed successfully: {completed_meeting}")
    return completed_meeting


@router.post(
    "/{meeting_id}/add_recurrence/{recurrence_id}",
    response_model=MeetingRetrieve,
)
@log_execution_time
async def add_recurrence(
    meeting_id: int,
    recurrence_id: int,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingRetrieve:
    """
    Add a recurrence to a meeting by their IDs.
    """
    logger.info(
        f"Adding recurrence with ID {recurrence_id} to meeting with ID {meeting_id}"
    )
    meeting = await service.update(
        meeting_id, MeetingUpdate(recurrence_id=recurrence_id)
    )
    if meeting is None:
        logger.warning(f"Meeting with ID {meeting_id} not found")
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    logger.info(f"Recurrence added successfully to meeting: {meeting}")
    return meeting


@router.get("/{meeting_id}/next/", response_model=MeetingRetrieve)
@log_execution_time
async def next_meeting(
    meeting_id: int,
    service: MeetingService = Depends(get_meeting_service),
) -> MeetingRetrieve:
    """
    Fetch the next meeting after the meeting with the provided ID.
    """
    logger.info(f"Fetching next meeting after meeting with ID: {meeting_id}")
    next_meeting_instance = await service.get_subsequent_meeting(meeting_id)
    if not next_meeting_instance:
        logger.warning(f"Next meeting after ID {meeting_id} not found")
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    logger.info(f"Next meeting retrieved: {next_meeting_instance}")
    return next_meeting_instance


@router.post("/{meeting_id}/users/")
@log_execution_time
async def add_users_to_meeting(
    meeting_id: int,
    request: AddUsersRequest,
    meeting_service: MeetingService = Depends(get_meeting_service),
):
    """
    Add users to a meeting from a list of UUIDS.
    """
    logger.info(request.user_ids)
    await meeting_service.add_users(meeting_id, request.user_ids)
    return {"message": "Users added to meeting successfully"}


@router.get("/{meeting_id}/users/")
@log_execution_time
async def get_users_from_meeting(
    meeting_id: int,
    meeting_service: MeetingService = Depends(get_meeting_service),
):
    """
    Fetch all users associated with a meeting.
    """
    users = await meeting_service.get_users(meeting_id)
    return users


@router.post("/recurring-meetings", response_model=list[MeetingRetrieve])
@log_execution_time
async def create_recurring_meetings(
    recurrence_id: int,
    meeting_data: MeetingCreateBatch,
    service: MeetingService = Depends(get_meeting_service),
):
    """
    Create a batch of recurring meetings for the provided recurrence.
    """
    logger.info(f"Creating recurring meetings with data: {meeting_data.model_dump()}")
    result = await service.create_recurring_meetings(
        recurrence_id, meeting_data.base_meeting, meeting_data.dates
    )
    logger.info("Recurring meetings created successfully")
    return result


@router.get("/by_user/{user_id}", response_model=list[MeetingRetrieve])
@log_execution_time
async def get_meetings_by_user(
    user_id: int,
    service: MeetingService = Depends(get_meeting_service),
) -> list[MeetingRetrieve]:
    """
    Fetch all meetings associated with a user.
    """
    logger.info(f"Fetching meetings for user with ID: {user_id}")
    result = await service.get_meetings_by_user_id(user_id)
    logger.info(f"Retrieved {len(result)} meetings for user ID: {user_id}")
    return result
