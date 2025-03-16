from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.api.endpoints import auth_endpoints
from app.models.user import User
from app.models.token import Token


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await auth_endpoints.login(response, form_data)

@auth_router.post("/logout")
async def logout(response: Response):
    return await auth_endpoints.logout(response)

@auth_router.post("/registration")
async def registration(request: User):
    return await auth_endpoints.registration(request)