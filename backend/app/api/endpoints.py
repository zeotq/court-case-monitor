from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import requests

from models.models import SearchRequest
from config import settings

router = APIRouter()

@router.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/pages/")

@router.post("/search", response_class=HTMLResponse)
async def search_case(request: SearchRequest):
    case_number = request.CaseNumbers[0] if request.CaseNumbers else "СИП-198/2025"
    
    url = "https://kad.arbitr.ru/Kad/SearchInstances"
    data = {
        "Page": 1,
        "Count": 25,
        "Courts": [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": [],
        "Judges": [],
        "CaseNumbers": [case_number],
        "WithVKSInstances": False
    }
    
    try:
        response = requests.post(url, headers=settings.headers, cookies=settings.cookies, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запроса: {e}")

    return HTMLResponse(content=response.text, status_code=response.status_code)

@router.post("/main", response_class=HTMLResponse)
async def main_case():
    url = "https://kad.arbitr.ru"
    try:
        response = requests.get(url, headers=settings.headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запроса: {e}")
    return HTMLResponse(content=response.text, status_code=response.status_code)
