from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models.user import CourtsCreate, UserBase


async def update_user_courts_data(
        db: AsyncSession,
        user: UserBase,
        new_data: CourtsCreate,
    ) -> UserBase:
    return user.id


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(UserDB)
        .options(
            selectinload(UserDB.organisations),
            selectinload(UserDB.tasks)
        )
        .where(UserDB.id == user_id)
    )
    return result.scalars().first()