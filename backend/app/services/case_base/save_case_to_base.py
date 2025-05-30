from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import ValidationError

from app.models.organisation import OrganisationDB
from app.models.case import CourtCaseDB
from app.models.case import CourtCase

from .courts_mapping import get_service_name


async def save_cases_to_db(session: AsyncSession, cases_data: list[dict]) -> None:
    case_data: dict

    async with session.begin():
        for case_data in cases_data:
            try:
                validated_case = CourtCase(**case_data)
            except ValidationError as e:
                print("Case skipped due to validation error:", e)
                continue

            case_date = validated_case.date

            plaintiff = await process_organisation(
                session,
                validated_case.plaintiff.inn if validated_case.plaintiff else None,
                validated_case.plaintiff.name if validated_case.plaintiff else None,
            )
            
            respondent = await process_organisation(
                session,
                validated_case.respondent.inn if validated_case.respondent else None,
                validated_case.respondent.name if validated_case.respondent else None,
            )

            await process_court_case(
                session,
                case_date,
                validated_case.case_type,
                validated_case.case_number,
                validated_case.case_link,
                validated_case.court,
                validated_case.judge,
                plaintiff.id if plaintiff else None,
                respondent.id if respondent else None,
            )


async def process_organisation(
    session: AsyncSession, 
    inn: str, 
    name: str
) -> OrganisationDB:
    if not inn and not name:
        return None
    
    org = None

    if inn:
        result = await session.execute(
            select(OrganisationDB).where(OrganisationDB.inn == inn)
        )
        org = result.scalar_one_or_none()
    elif name:
        result = await session.execute(
            select(OrganisationDB).where(OrganisationDB.name == name)
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
    case_type: str,
    case_number: str,
    case_link: str,
    court: str,
    judge: str,
    plaintiff_id: int,
    respondent_id: int
):
    result = await session.execute(
        select(CourtCaseDB).where(CourtCaseDB.case_number == case_number)
    )
    existing_case = result.scalar_one_or_none()
    
    if existing_case:
        if date is not None:
            existing_case.date = date
        if case_type:
            existing_case.case_type = case_type
        if case_link:
            existing_case.case_link = case_link
        if court:
            existing_case.court = get_service_name(court)
        if judge:
            existing_case.judge = judge
        if plaintiff_id:
            existing_case.plaintiff_id = plaintiff_id
        if respondent_id:
            existing_case.respondent_id = respondent_id
        session.add(existing_case)
    else:
        new_case = CourtCaseDB(
            date=date,
            case_type=case_type,
            case_number=case_number,
            case_link=case_link,
            court=get_service_name(court),
            judge=judge,
            plaintiff_id=plaintiff_id,
            respondent_id=respondent_id
        )
        session.add(new_case)

    await session.flush()