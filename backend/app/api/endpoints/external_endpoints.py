from fastapi import HTTPException, Body, status
from fastapi.responses import JSONResponse
from time import time
from random import randint
import httpx

from app.models.arbitr import SearchRequestData
from app.utils.kad_parser import SearchResponseParser
from app.utils.kad_access_cookies import get_cookies_dict
from app.config import settings, ARBITR_URL


async def update_cookies():
    new_cookies = await get_cookies_dict(headless=True, debug=True)
    print(f"New Cookies: {new_cookies}")
    settings.cookies.update(new_cookies)


async def need_captcha():
    pass


async def search_case(
        request: SearchRequestData = Body(...),
    ):
    SEARCH_URL = f"{ARBITR_URL}/Kad/SearchInstances"

    data = {
        "Page": 1 if request.Page is None else request.Page,
        "Count": min(request.Count, 25) if request.Count else 25,
        "Courts": request.Courts or [],
        "DateFrom": request.DateFrom.isoformat() if request.DateFrom else None,
        "DateTo": request.DateTo.isoformat() if request.DateTo else None,
        "Sides": [side.model_dump() for side in (request.Sides or [])],
        "Judges": [judge.model_dump() for judge in (request.Judges or [])],
        "CaseNumbers": request.CaseNumbers or [],
        "WithVKSInstances": request.WithVKSInstances or False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(SEARCH_URL, headers=settings.headers, cookies=settings.cookies, json=data)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        await update_cookies()
        raise HTTPException(status_code=response.status_code, detail=f"httpx.HTTPStatusError at search_case: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"httpx.RequestError: {e}")

    parsed_repsonse_text = SearchResponseParser.parse(response.text)

    return JSONResponse(content=parsed_repsonse_text, status_code=response.status_code)
