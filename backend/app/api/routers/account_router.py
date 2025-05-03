from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.account_endpoints import update_user_courts_data, get_user_by_id
from app.models.user import CourtsCreate, UserBase
from app.services.jwt_validation import access_header_validation
from app.database import get_db


account_router = APIRouter(prefix="/account", tags=["account"])

@account_router.get("/self", response_model=UserBase, response_class=JSONResponse)
async def get_user_profile(
    user: UserBase = Depends(access_header_validation),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    return await get_user_by_id(db, user.id)


@account_router.post("/self", response_model=UserBase, response_class=JSONResponse)
async def update_user_profile(
    new_data: CourtsCreate,
    user: UserBase = Depends(access_header_validation),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    return await update_user_courts_data(db, user.id, new_data)
