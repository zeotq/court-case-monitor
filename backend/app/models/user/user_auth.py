from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class AuthUserInDB(AuthUser):
    hashed_password: str

class AuthUserCreate(AuthUser):
    email: str
    password: str