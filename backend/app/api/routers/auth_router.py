from fastapi import APIRouter
from app.api.endpoints import auth_endpoints


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(username: str, password: str):
    return {"message": "User logged in"}

@auth_router.post("/logout")
async def logout():
    return {"message": "User logged out"}

@auth_router.post("/usercreate")
async def user_create(username: str, email: str, password: str):
    return {"message": "User created"}
