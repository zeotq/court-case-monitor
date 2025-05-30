from uuid import uuid4
from base64 import urlsafe_b64encode
from hashlib import sha256
from datetime import datetime, timedelta, timezone

from app.utils.jwt import get_expiration_time


auth_codes = {}

AUTH_CODE_EXPIRE_MINUTES = 1

def create_auth_code(
        user_id: str,
        code_challenge: str,
    ) -> str:
    code = str(uuid4())
    expire_time = get_expiration_time(timedelta(minutes=AUTH_CODE_EXPIRE_MINUTES))
    auth_codes[code] = {"user_id": user_id, "expires": expire_time, "code_challenge": code_challenge}
    return code

def validate_auth_code(
        code: str,
        code_verifier: str
    ) -> dict:
    if not code in auth_codes:
        return None
    data = auth_codes[code]

    if data["expires"] < datetime.now(timezone.utc):
        return None

    computed_challenge = urlsafe_b64encode(
        sha256(code_verifier.encode()).digest()
    ).decode('utf-8').rstrip("=")

    if computed_challenge != data["code_challenge"]:
        return None

    return data

def delete_auth_code(code: str):
    if code in auth_codes:
        del auth_codes[code]