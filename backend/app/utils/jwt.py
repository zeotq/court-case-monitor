import jwt
from datetime import datetime, timedelta, timezone
from app.utils.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.models.token import TokenPayload


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return await _create_token(data, expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    return await _create_token(data, expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


async def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def decode_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None