from fastapi import status, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated
from datetime import timedelta

from app.models.user import User
from app.services.database import fake_db
from app.services.cache import create_auth_code, validate_auth_code, delete_auth_code
from app.services.jwt_validation import refresh_cookie_validation
from app.utils.jwt import create_access_token, create_refresh_token, get_expiration_time
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


async def authorize_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        code_challenge: str,
        callback_uri: str
    ) -> JSONResponse:
    
    user = fake_db.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    code = create_auth_code(user.username, code_challenge)

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"code": code, "callback_uri": callback_uri}
    )

    return response
    

async def exchange_code_for_tokens(
        code: str,
        code_verifier: str,
        callback_uri: str
    ) -> JSONResponse:

    user_auth_data = validate_auth_code(code, code_verifier)
    delete_auth_code(code)

    if not user_auth_data or not 'user_id' in user_auth_data:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    access_token_expires = get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = get_expiration_time(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = await create_access_token({'sub': user_auth_data['user_id']}, expiry_date=access_token_expires)
    refresh_token = await create_refresh_token({'sub': user_auth_data['user_id']}, expiry_date=refresh_token_expires)

    response = JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"access_token": access_token, 
                 "token_type": "bearer",
                 "redirect_uri": callback_uri},
    )

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=refresh_token_expires
    )

    return response


async def refresh_token(
        request: Request
    ) -> JSONResponse:

    user = await refresh_cookie_validation(request)
    new_access_token_expires = get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    new_access_token = await create_access_token({'sub': user.username}, expiry_date=new_access_token_expires)

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": new_access_token, "token_type": "bearer"},
    )

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"

    return response
    

async def logout() -> JSONResponse:
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User logged out"},
    )

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


async def registration(request: User):
    return JSONResponse(content={"message": "User created"}, status_code=status.HTTP_201_CREATED)
