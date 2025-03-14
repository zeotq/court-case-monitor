from fastapi import HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import httpx

from app.models import SearchRequestData
from app.services.kad_parser import SearchResponseParser
from app.config import settings


async def search_case(request: SearchRequestData = Body(...)):
    url = "https://kad.arbitr.ru/Kad/SearchInstances"

    data = {
        "Page": 1 if request.Page is None else request.Page,
        "Count": min(request.Count, 25) if request.Count else 25,
        "Courts": request.Courts or [],
        "DateFrom": request.DateFrom.isoformat() if request.DateFrom else None,
        "DateTo": request.DateTo.isoformat() if request.DateTo else None,
        "Sides": [side.dict() for side in (request.Sides or [])],
        "Judges": [judge.dict() for judge in (request.Judges or [])],
        "CaseNumbers": request.CaseNumbers or [],
        "WithVKSInstances": request.WithVKSInstances or False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=settings.headers, cookies=settings.cookies, json=data)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Ошибка запроса: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запроса: {e}")

    parsed_repsonse_text = SearchResponseParser.parse(response.text)

    return JSONResponse(content=parsed_repsonse_text, status_code=response.status_code)
