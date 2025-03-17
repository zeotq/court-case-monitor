from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated

from app.api.endpoints import auth_endpoints
from app.models.user import User
from app.models.token import TokenPayload


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> RedirectResponse:
    return await auth_endpoints.login(form_data)

@auth_router.get("/exchange")
async def exchange_code_for_tokens(code: str) -> RedirectResponse:
    return await auth_endpoints.exchange_code_for_tokens(code)

@auth_router.post("/refresh")
async def refresh_token(request: Request) -> TokenPayload:
    return await auth_endpoints.refresh_token(request)

@auth_router.post("/logout")
async def logout() -> JSONResponse:
    return await auth_endpoints.logout()

@auth_router.post("/registration")
async def registration(request: User) -> JSONResponse:
    return await auth_endpoints.registration(request)