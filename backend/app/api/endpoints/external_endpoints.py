import httpx
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.arbitr import SearchRequestData
from app.utils.kad_parser import SearchResponseParser, case_type_to_litter
from app.services.case_base import save_cases_to_db
from app.config import settings, ARBITR_URL, COOKIE_URL


async def fetch_cookies(from_file: bool = False):
    TARGET_URL = f"{COOKIE_URL}/cookies/file" if from_file else f"{COOKIE_URL}/cookies?headless=false&debug=false"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(TARGET_URL, timeout=60)
            r.raise_for_status()
            return r.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Cookie service return status code {e.response.status_code} with error {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't connect to cookie service")


async def need_captcha():
    pass


async def search_case(
        request: SearchRequestData,
        session: AsyncSession
    ):
    SEARCH_URL = f"{ARBITR_URL}/Kad/SearchInstances"

    if not settings.cookies:
        settings.cookies = await fetch_cookies(from_file=True)

    data = {
        "Page": 1 if request.Page is None else request.Page,
        "Count": min(request.Count, 25) if request.Count else 25,
        "Courts": request.Courts or [],
        "DateFrom": datetime.strptime(request.DateFrom, "%Y-%m-%d").replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S") if request.DateFrom else None,
        "DateTo": datetime.strptime(request.DateTo, "%Y-%m-%d").replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S") if request.DateTo else None,
        "Sides": [side.model_dump() for side in (request.Sides or [])],
        "Judges": [judge.JudgeId for judge in (request.Judges or [])],
        "CaseNumbers": request.CaseNumbers or [],
        "WithVKSInstances": request.WithVKSInstances or False
    }

    if request.CaseType:
        data.update({"CaseType" : case_type_to_litter(request.CaseType)})

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SEARCH_URL, headers=settings.headers, cookies=settings.cookies, json=data)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS:
                settings.cookies = await fetch_cookies()
                response = await client.post(SEARCH_URL, headers=settings.headers, cookies=settings.cookies, json=data)
                response.raise_for_status()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Try again later. {SEARCH_URL} return code {e.response.status_code} with error {e.response.text}"
                )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"RequestError: {e}"
            )

    parsed_response_text = SearchResponseParser.parse(response.text)
    await save_cases_to_db(session, parsed_response_text['cases'])

    return JSONResponse(content=parsed_response_text, status_code=response.status_code)
