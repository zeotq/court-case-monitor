from fastapi import APIRouter
from app.api.endpoints import auth_endpoints
from app.models.user import LoginRequest, RegisterRequest


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(request: LoginRequest):
    return await auth_endpoints.login(request)

@auth_router.post("/logout")
async def logout():
    return await auth_endpoints.logout()

@auth_router.post("/usercreate")
async def user_create(request: RegisterRequest):
    return await auth_endpoints.usercreate(request)