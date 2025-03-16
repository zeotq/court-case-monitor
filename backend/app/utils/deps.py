from fastapi import HTTPException, status, Request
from typing import Optional
from app.utils.jwt import decode_token
from app.models.user import UserInDB
from app.services.database import fake_db 


async def get_current_user(request: Request, token: Optional[str] = None) -> UserInDB:
    token = token or request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

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
