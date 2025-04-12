from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.jwt import decode_token
from app.utils.is_banned import raise_if_user_banned
from app.models.user import AuthUserInDB, UserDB
from app.models.blacklist import BannedUsersDB
from app.models.token import TokenPayload
from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/exchange")


async def refresh_cookie_validation(request: Request) -> AuthUserInDB:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await process_token(token)
    return user


async def access_cookie_validation(request: Request) -> AuthUserInDB:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await process_token(token)
    return user


async def access_header_validation(token: str = Depends(oauth2_scheme)):
    return await process_token(token)


async def process_token(token: TokenPayload) -> AuthUserInDB:
    payload = await decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    username: str = payload.sub
    db: Session = SessionLocal()
    user = db.query(UserDB).filter_by(username=username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise_if_user_banned(user)

    return user
