from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Party(BaseModel):
    name: Optional[str]
    inn: Optional[str]

    class Config:
        orm_mode = True


class CourtCase(BaseModel):
    date: datetime
    case_type: Optional[str]
    case_number: str
    case_link: Optional[str]
    court: Optional[str]
    plaintiff: Optional[Party]
    respondent: Optional[Party]

    class Config:
        orm_mode = True
