import jwt
from datetime import datetime, timedelta, timezone
from app.utils.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.models.token import TokenPayload


def get_expiration_time(expires_delta: timedelta) -> datetime:
    now = datetime.now(timezone.utc)
    expiration = now + expires_delta
    return expiration


async def create_access_token(data: dict, expiry_date: datetime | None = None):
    return await _create_token(data, expiry_date or get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)))


async def create_refresh_token(data: dict, expiry_date: datetime | None = None):
    return await _create_token(data, expiry_date or get_expiration_time(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)))


async def _create_token(data: dict, expiry_date: datetime) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expiry_date})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def decode_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None