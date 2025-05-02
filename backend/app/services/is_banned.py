from fastapi import HTTPException, status
from app.models.blacklist import BannedUsersDB
from app.models.user import UserDB


async def raise_if_user_banned(user: UserDB) -> None:
    if user.bans:
        latest_ban: BannedUsersDB = user.bans[-1]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is banned. Reason: {latest_ban.reason}"
    )