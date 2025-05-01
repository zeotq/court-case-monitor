from fastapi import HTTPException, Body, status
from fastapi.responses import JSONResponse
import httpx

from app.models.arbitr import SearchRequestData
from app.utils.kad_parser import SearchResponseParser
from app.config import settings, ARBITR_URL, COOKIE_URL


async def fetch_cookies_from_file():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{COOKIE_URL}/cookies/file", timeout=60)
        r.raise_for_status()
        return r.json()


async def fetch_cookies():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{COOKIE_URL}/cookies?headless=false&debug=false", timeout=60)
        r.raise_for_status()
        return r.json()


async def need_captcha():
    pass


async def search_case(
        request: SearchRequestData = Body(...),
    ):
    SEARCH_URL = f"{ARBITR_URL}/Kad/SearchInstances"
    if not settings.cookies:
        settings.cookies = await fetch_cookies_from_file()

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
        settings.cookies = await fetch_cookies()
        raise HTTPException(status_code=response.status_code, detail=f"Try again.\nhttpx.HTTPStatusError at search_case: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"httpx.RequestError: {e}")

    parsed_repsonse_text = SearchResponseParser.parse(response.text)

    return JSONResponse(content=parsed_repsonse_text, status_code=response.status_code)
