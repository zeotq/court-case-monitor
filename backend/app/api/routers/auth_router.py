from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated

from app.api.endpoints import auth_endpoints
from app.models.user import User
from app.models.token import Token


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(response: JSONResponse, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await auth_endpoints.login(response, form_data)

@auth_router.post("/refresh")
async def refresh_token(request: Request, response: JSONResponse):
    return await auth_endpoints.refresh_token(request, response)

@auth_router.post("/logout")
async def logout(response: JSONResponse):
    return await auth_endpoints.logout(response)

@auth_router.post("/registration")
async def registration(request: User):
    return await auth_endpoints.registration(request)