from pydantic import Field, EmailStr
from .user_schema import UserBase


class AuthUserCheck(UserBase):
    hashed_password: str

class AuthUserCreate(UserBase):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)