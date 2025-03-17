from uuid import uuid4
from datetime import datetime, timedelta, timezone

from app.utils.jwt import get_expiration_time


auth_codes = {}

AUTH_CODE_EXPIRE_MINUTES = 1

def create_auth_code(user_id: str) -> str:
    code = str(uuid4())
    expire_time = get_expiration_time(timedelta(minutes=AUTH_CODE_EXPIRE_MINUTES))
    auth_codes[code] = {"user_id": user_id, "expires": expire_time}
    return code

def validate_auth_code(code: str) -> str | None:
    if code in auth_codes:
        data = auth_codes[code]
        if data["expires"] > datetime.now(timezone.utc):
            return data["user_id"]
    return None

def delete_auth_code(code: str):
    if code in auth_codes:
        del auth_codes[code]