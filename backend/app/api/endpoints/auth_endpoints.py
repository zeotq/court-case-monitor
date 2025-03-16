from fastapi import status, Response, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from datetime import timedelta

from app.models.user import User
from app.services.database import fake_db
from app.utils.jwt import create_access_token, decode_token
from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_db.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token({'sub': user.username}, expires_delta=access_token_expires)
    refresh_token = create_access_token({'sub': user.username}, expires_delta=refresh_token_expires)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=access_token_expires
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=refresh_token_expires
    )

    return JSONResponse(content={"message": "User logged in"}, status_code=status.HTTP_200_OK)


async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = await decode_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    username = payload.get('sub')

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    new_access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token({'sub': username}, expires_delta=new_access_token_expires)


    response.set_cookie(
        key='access_token',
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite='strict',
        expires=new_access_token_expires
    )

    return JSONResponse(content={"message": "User logged in"}, status_code=status.HTTP_200_OK)


async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return JSONResponse(content={"message": "User logged out"}, status_code=status.HTTP_200_OK)


async def registration(request: User):
    return JSONResponse(content={"message": "User created"}, status_code= status.HTTP_201_CREATED)
