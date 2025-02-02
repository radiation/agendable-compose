"""
Routes for user management.
"""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.decorators import log_execution_time
from app.core.dependencies import get_user_service
from app.core.logging_config import logger
from app.exceptions import NotFoundError
from app.schemas import UserCreate, UserRetrieve, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserRetrieve)
@log_execution_time
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    """
    Create a new user with the provided data.
    """
    logger.info(f"Creating user with data: {user.model_dump()}")
    return await service.create(user)


@router.get("/", response_model=list[UserRetrieve])
@log_execution_time
async def get_users(
    service: UserService = Depends(get_user_service),
) -> list[UserRetrieve]:
    """
    Fetch all users.
    """
    logger.info("Fetching all users.")
    result = await service.get_all()
    logger.info(f"Retrieved {len(result)} users.")
    return result


@router.get("/{user_id}", response_model=UserRetrieve)
@log_execution_time
async def get_user(
    user_id: UUID, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    """
    Fetch a user by ID.
    """
    logger.info(f"Fetching user with ID: {user_id}")
    result = await service.get_by_id(user_id)
    if result is None:
        logger.warning(f"User with ID {user_id} not found")
        raise NotFoundError(f"User with ID {user_id} not found")
    logger.info(f"User retrieved: {result}")
    return result


@router.get("/by-email/{email}", response_model=UserRetrieve)
@log_execution_time
async def get_user_by_email(
    email: str, service: UserService = Depends(get_user_service)
) -> UserRetrieve:
    """
    Fetch a user by email.
    """
    logger.info(f"Fetching user with email: {email}")
    result = await service.get_by_field("email", email)
    if result is None:
        logger.warning(f"User with email {email} not found")
        raise NotFoundError(f"User with email {email} not found")
    logger.info(f"User retrieved: {result}")
    return result[0]


@router.put("/{user_id}", response_model=UserRetrieve)
@log_execution_time
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserRetrieve:
    """
    Update a user with the provided data.
    """
    logger.info(f"Updating user with ID: {user_id} with data: {user.model_dump()}")
    result = await service.update(user_id, user)
    if result is None:
        logger.warning(f"User with ID {user_id} not found")
        raise NotFoundError(f"User with ID {user_id} not found")
    logger.info(f"User updated successfully: {result}")
    return result


@router.delete("/{user_id}", status_code=204)
@log_execution_time
async def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    """
    Delete a user by ID.
    """
    logger.info(f"Deleting user with ID: {user_id}")
    success = await service.delete(user_id)
    if not success:
        logger.warning(f"User with ID {user_id} not found")
        raise NotFoundError(f"User with ID {user_id} not found")
    logger.info(f"User with ID {user_id} deleted successfully.")
