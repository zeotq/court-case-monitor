from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.endpoints.account_endpoints import update_user_courts_data
from app.models.user import CourtsCreate, UserPublicFields
from app.services.jwt_validation import access_header_validation
from app.database import get_db


account_router = APIRouter(prefix="/account", tags=["account"])

@account_router.get("/self", response_model=UserPublicFields, response_class=JSONResponse)
async def get_user_profile(
    user: UserPublicFields = Depends(access_header_validation),
) -> JSONResponse:
    return user

@account_router.post("/self", response_model=UserPublicFields, response_class=JSONResponse)
async def update_user_profile(
    new_data: CourtsCreate,
    user: UserPublicFields = Depends(access_header_validation),
    db: Session = Depends(get_db)
) -> JSONResponse:
    return await update_user_courts_data(new_data, user, db)
