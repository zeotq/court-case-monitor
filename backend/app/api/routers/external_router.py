from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from app.models.arbitr import SearchRequestData
from app.models.user import UserInDB
from app.api.endpoints import external_endpoints
from app.services.jwt_validation import access_header_validation


external_router = APIRouter(prefix="/external", tags=["external"])

@external_router.post("/search", response_class=JSONResponse)
async def search_case(
    request: SearchRequestData = Body(...),
    user_header: UserInDB = Depends(access_header_validation)
    ):
    return await external_endpoints.search_case(request)