from fastapi import status
from fastapi.responses import JSONResponse
from app.models.user import LoginRequest, RegisterRequest


async def login(request: LoginRequest):
    return JSONResponse(content={"message": "User logged in"}, status_code=status.HTTP_200_OK)

async def logout():
    return JSONResponse(content={"message": "User logged out"}, status_code=status.HTTP_200_OK)

async def usercreate(request: RegisterRequest):
    return JSONResponse(content={"message": "User created"}, status_code= status.HTTP_201_CREATED)
