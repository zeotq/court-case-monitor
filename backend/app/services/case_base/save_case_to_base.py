from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.organisation import OrganisationDB
from app.models.case import CourtCaseDB


async def save_cases_to_db(session: AsyncSession, cases_data: list) -> None:
    async with session.begin():
        for case_data in cases_data:
            case_date = datetime.strptime(
                case_data['date'], 
                "%d.%m.%Y %H:%M:%S"
            )

            plaintiff = await process_organisation(
                session,
                case_data['plaintiff']['inn'],
                case_data['plaintiff']['name']
            )
            
            respondent = await process_organisation(
                session,
                case_data['respondent']['inn'],
                case_data['respondent']['name']
            )

            await process_court_case(
                session,
                case_date,
                case_data['case_number'],
                case_data['case_link'],
                case_data['court'],
                plaintiff.id,
                respondent.id
            )


async def process_organisation(
    session: AsyncSession, 
    inn: str, 
    name: str
) -> OrganisationDB:
    result = await session.execute(
        select(OrganisationDB).where(OrganisationDB.inn == inn)
    )
    org = result.scalar_one_or_none()
    
    if not org:
        org = OrganisationDB(inn=inn, name=name)
        session.add(org)
        await session.flush()
    
    return org


async def process_court_case(
    session: AsyncSession,
    date: datetime,
    case_number: str,
    case_link: str,
    court: str,
    plaintiff_id: int,
    respondent_id: int
):
    result = await session.execute(
        select(CourtCaseDB).where(CourtCaseDB.case_number == case_number)
    )
    existing_case = result.scalar_one_or_none()
    
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
        await session.flush()