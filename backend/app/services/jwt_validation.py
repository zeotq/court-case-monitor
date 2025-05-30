from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.jwt import decode_token
from app.services.is_banned import raise_if_user_banned
from app.models.user import UserBase, UserDB
from app.models.token import TokenPayload
from app.database import AsyncSessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/exchange")


async def refresh_cookie_validation(request: Request) -> UserBase:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await process_token(token)
    return user


async def access_cookie_validation(request: Request) -> UserBase:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await process_token(token)
    return user


async def access_header_validation(token: str = Depends(oauth2_scheme)) -> UserBase:
    return await process_token(token)


async def process_token(token: TokenPayload) -> UserBase:
    payload = await decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    username: str = payload.sub

    async with AsyncSessionLocal() as db:
        stmt = (
            select(UserDB)
            .options(selectinload(UserDB.bans))
            .where(username == username)
        )
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await raise_if_user_banned(user)

        return user