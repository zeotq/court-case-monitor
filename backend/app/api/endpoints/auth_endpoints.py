from fastapi import status, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from datetime import timedelta
from json import dumps

from app.models.user import User
from app.services.database import fake_db
from app.utils.jwt import create_access_token, create_refresh_token, get_expiration_time
from app.utils.deps import get_current_user
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


def render(content) -> bytes:
        return dumps(content, ensure_ascii=False, allow_nan=False, indent=None, separators=(",", ":"),).encode("utf-8")


async def login(response: JSONResponse, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_db.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = get_expiration_time(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = await create_access_token({'sub': user.username}, expiry_date=access_token_expires)
    refresh_token = await create_refresh_token({'sub': user.username}, expiry_date=refresh_token_expires)

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"
    response.status_code = status.HTTP_200_OK

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=access_token_expires
    )  # Todo / перенести access token из куки

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=refresh_token_expires
    )
    response.body=render({"access_token": access_token, "token_type": "bearer"})
    return response


async def refresh_token(request: Request, response: JSONResponse):
    refresh_token = request.cookies.get("refresh_token")
    
    user = await get_current_user(request, refresh_token)

    new_access_token_expires = get_expiration_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    new_access_token = await create_access_token({'sub': user.username}, expiry_date=new_access_token_expires)

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"
    response.status_code = status.HTTP_200_OK

    response.set_cookie(
        key='access_token',
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=new_access_token_expires
    )
    response.body=render({"access_token": new_access_token, "token_type": "bearer"})
    return response
    

async def logout(response: JSONResponse):
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json"
    response.status_code = status.HTTP_200_OK
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.body=render({"message": "User logged out"})
    return response


async def registration(request: User):
    return JSONResponse(content={"message": "User created"}, status_code=status.HTTP_201_CREATED)
