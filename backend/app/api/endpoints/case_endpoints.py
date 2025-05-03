from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime

from app.models.arbitr import SearchRequestData
from app.models.case import CourtCaseDB


async def search_case_in_db(
    request: SearchRequestData,
    session: AsyncSession,
):
    try:
        stmt = select(CourtCaseDB).options(
            joinedload(CourtCaseDB.plaintiff),
            joinedload(CourtCaseDB.respondent)
        )

        filters = []

        if request.Courts:
            filters.append(CourtCaseDB.court.in_(request.Courts))

        if request.Judges:
            filters.append(CourtCaseDB.judge.in_(map(lambda a: a.JudgeId, request.Judges)))

        if request.DateFrom:
            date_from = datetime.strptime(request.DateFrom, "%Y-%m-%d").date()
            filters.append(CourtCaseDB.date >= date_from)

        if request.DateTo:
            date_to = datetime.strptime(request.DateTo, "%Y-%m-%d").date()
            filters.append(CourtCaseDB.date <= date_to)

        if request.CaseNumbers:
            filters.append(CourtCaseDB.case_number.in_(request.CaseNumbers))

        if filters:
            stmt = stmt.filter(*filters)

        result = await session.execute(stmt)
        cases = result.unique().scalars().all()

        if request.Sides:
            sides_filtered = []
            for case in cases:
                for side in request.Sides:
                    match = False
                    if side.Name:
                        match |= (case.plaintiff and case.plaintiff.name == side.Name) or \
                                 (case.respondent and case.respondent.name == side.Name)
                    if side.Inn:
                        match |= (case.plaintiff and case.plaintiff.inn == side.Inn) or \
                                 (case.respondent and case.respondent.inn == side.Inn)
                    if match:
                        sides_filtered.append(case)
                        break
            cases = sides_filtered

        cases_data = []
        for case in cases:
            cases_data.append({
                "id": case.id,
                "date": case.date.isoformat(),
                "case_number": case.case_number,
                "case_link": case.case_link,
                "court": case.court,
                "judge": case.judge,
                "plaintiff": {
                    "name": case.plaintiff.name if case.plaintiff else None,
                    "inn": case.plaintiff.inn if case.plaintiff else None
                } if case.plaintiff else None,
                "respondent": {
                    "name": case.respondent.name if case.respondent else None,
                    "inn": case.respondent.inn if case.respondent else None
                } if case.respondent else None
            })

        return JSONResponse(content={"cases": cases_data}, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
