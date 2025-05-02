from fastapi import HTTPException, Body, status
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import select

from app.database import get_db
from app.models.organisation import OrganisationDB
from app.models.case import CourtCaseDB
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
        session: Session = Depends(get_db),
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

    parsed_response_text = SearchResponseParser.parse(response.text)

    parsed_response_text = SearchResponseParser.parse(response.text)
    save_cases_to_db(session, parsed_response_text['cases'])

    return JSONResponse(content=parsed_response_text, status_code=response.status_code)


def save_cases_to_db(session: Session, cases_data: list) -> None:
    try:
        for case_data in cases_data:
            case_date = datetime.strptime(
                case_data['date'], 
                "%d.%m.%Y %H:%M:%S"
            )

            plaintiff = process_organisation(
                session,
                case_data['plaintiff']['inn'],
                case_data['plaintiff']['name']
            )
            
            respondent = process_organisation(
                session,
                case_data['respondent']['inn'],
                case_data['respondent']['name']
            )

            process_court_case(
                session,
                case_date,
                case_data['case_number'],
                case_data['case_link'],
                case_data['court'],
                plaintiff.id,
                respondent.id
            )
        
        session.commit()
    
    except IntegrityError as e:
        session.rollback()
        print(f"Duplicate case number: {e}")
    
    except Exception as e:
        session.rollback()
        print(f"Database Error: {e}")


def process_organisation(
    session: Session, 
    inn: str, 
    name: str
) -> OrganisationDB:
    org = session.execute(
        select(OrganisationDB)
        .where(OrganisationDB.inn == inn)
    ).scalar_one_or_none()
    
    if not org:
        org = OrganisationDB(inn=inn, name=name)
        session.add(org)
        session.flush()
    
    return org

def process_court_case(
    session: Session,
    date: datetime,
    case_number: str,
    case_link: str,
    court: str,
    plaintiff_id: int,
    respondent_id: int
):
    existing_case = session.execute(
        select(CourtCaseDB)
        .where(CourtCaseDB.case_number == case_number)
    ).scalar_one_or_none()
    
    if not existing_case:
        new_case = CourtCaseDB(
            date=date,
            case_number=case_number,
            case_link=case_link,
            court=court,
            plaintiff_id=plaintiff_id,
            respondent_id=respondent_id
        )
        session.add(new_case)
        session.flush()