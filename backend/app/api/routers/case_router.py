from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.arbitr import SearchRequestData
from app.models.user import UserBase
from app.api.endpoints import case_endpoints
from app.services.jwt_validation import access_header_validation


case_router = APIRouter(prefix="/case", tags=["case"])

@case_router.post("/search", response_class=JSONResponse)
async def search_case(
    request: SearchRequestData = Body(...),
    user_header: UserBase = Depends(access_header_validation),
    db: AsyncSession = Depends(get_db),
    ):
    return await case_endpoints.search_case_in_db(request, db)