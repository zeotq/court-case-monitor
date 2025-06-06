from pydantic import BaseModel
from typing import List, Optional


class Side(BaseModel):
    Name: Optional[str] = None
    Type: Optional[int] = None
    Inn: Optional[str] = None
    ExactMatch: Optional[bool] = None

class Judge(BaseModel):
    JudgeId: Optional[str] = None
    Type: Optional[int] = None

class SearchRequestData(BaseModel):
    Page: Optional[int] = None
    Count: Optional[int] = None
    CaseType: Optional[str] = None
    Courts: Optional[List[str]] = None
    DateFrom: Optional[str] = None
    DateTo: Optional[str] = None
    Sides: Optional[List[Side]] = None
    Judges: Optional[List[Judge]] = None
    CaseNumbers: Optional[List[str]] = None
    WithVKSInstances: Optional[bool] = None
