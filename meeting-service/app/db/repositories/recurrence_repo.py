from app.core.logging_config import logger
from app.db.models.recurrence import Recurrence
from app.db.repositories import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class RecurrenceRepository(BaseRepository[Recurrence]):
    def __init__(self, db: AsyncSession):
        super().__init__(Recurrence, db)

    async def get_by_id(self, object_id: int) -> Recurrence:
        logger.debug(f"Fetching recurrence with ID: {object_id}")
        stmt = select(self.model).filter(self.model.id == object_id)
        result = await self.db.execute(stmt)
        recurrence = result.scalars().first()
        if not recurrence:
            logger.warning(f"Recurrence with ID {object_id} not found")
        return recurrence
