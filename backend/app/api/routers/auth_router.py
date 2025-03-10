from fastapi import APIRouter
from app.api.endpoints import auth_endpoints


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(username: str, password: str):
    return await auth_endpoints.login(username, password)

@auth_router.post("/logout")
async def logout():
    return await auth_endpoints.logout()

@auth_router.post("/usercreate")
async def user_create(username: str, email: str, password: str):
    return await auth_endpoints.user_create(username, email, password)