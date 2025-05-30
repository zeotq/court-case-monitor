from fastapi import APIRouter, Request, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.api.endpoints import auth_endpoints
from app.models.user import AuthUserCreate
from app.models.token import TokenPayload


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/authorize", response_class=JSONResponse)
async def authorize_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        code_challenge: str = Form(...),
        callback_uri: str = Form(...),
        db: AsyncSession = Depends(get_db)
    ) -> JSONResponse:
    return await auth_endpoints.authorize_user(form_data, code_challenge, callback_uri, db)

@auth_router.get("/token")
async def exchange_code_for_tokens(
        code: str,
        code_verifier: str,
        callback_uri: str
    ) -> JSONResponse:
    return await auth_endpoints.exchange_code_for_tokens(code, code_verifier, callback_uri)

@auth_router.post("/refresh")
async def exchange_refresh_token_for_access_token(request: Request) -> TokenPayload:
    return await auth_endpoints.refresh_token(request)

@auth_router.post("/logout")
async def logout() -> JSONResponse:
    return await auth_endpoints.logout()

@auth_router.post("/registration")
async def register(
        form_data: AuthUserCreate,
        db: AsyncSession = Depends(get_db)
    ) -> JSONResponse:
    return await auth_endpoints.registration(form_data, db)