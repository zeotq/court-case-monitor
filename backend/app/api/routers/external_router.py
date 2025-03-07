from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.models.kad_models import SearchRequestData
from app.api.endpoints import external_endpoints


external_router = APIRouter(prefix="/external", tags=["external"])

@external_router.post("/search", response_class=JSONResponse)
async def search_case(request: SearchRequestData = Body(...)):
    return await external_endpoints.search_case(request)