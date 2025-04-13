from sqlalchemy.orm import Session
from app.models.user import CourtsCreate, UserPublicFields


async def update_user_courts_data(
        new_data: CourtsCreate,
        user: UserPublicFields,
        db: Session
    ) -> UserPublicFields:
    return user