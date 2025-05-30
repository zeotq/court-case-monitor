from pydantic import BaseModel, field_validator
from pydantic.types import StringConstraints
from typing import Optional, Annotated
from datetime import datetime


class Party(BaseModel):
    name: Optional[Annotated[str, StringConstraints(max_length=255)]] = None
    inn: Optional[Annotated[str, StringConstraints(max_length=12)]] = None

    class Config:
        orm_mode = True


class CourtCase(BaseModel):
    date: datetime
    case_type: Optional[Annotated[str, StringConstraints(max_length=32)]] = None
    case_number: Annotated[str, StringConstraints(max_length=50)] = None
    case_link: Optional[Annotated[str, StringConstraints(max_length=512)]] = None
    court: Optional[Annotated[str, StringConstraints(max_length=64)]] = None
    judge: Optional[Annotated[str, StringConstraints(max_length=64)]] = None
    plaintiff: Optional[Party] = None
    respondent: Optional[Party] = None

    @field_validator("date", mode="before")
    @classmethod
    def parse_custom_date(cls, v):
        if isinstance(v, datetime):
            return v
        try:
            return datetime.strptime(v, "%d.%m.%Y %H:%M:%S")
        except (ValueError, TypeError):
            return datetime(1970, 1, 1, 0, 0, 0)

    class Config:
        orm_mode = True
