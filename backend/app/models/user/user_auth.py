from pydantic import BaseModel, Field, EmailStr


class AuthUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class AuthUserInDB(AuthUser):
    hashed_password: str

class AuthUserCreate(AuthUser):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)