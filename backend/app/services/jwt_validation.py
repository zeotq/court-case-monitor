from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import decode_token
from app.models.user import UserInDB
from app.models.token import TokenPayload
from app.services.database import fake_db 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/exchange")


async def refresh_cookie_validation(request: Request) -> UserInDB:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await process_token(token)
    return user


async def access_cookie_validation(request: Request) -> UserInDB:
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


async def process_token(token: TokenPayload) -> UserInDB:
    payload = await decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    username = payload.sub
    user = fake_db.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")

    return user
