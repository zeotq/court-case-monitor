from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.models.organisation import OrganisationCreate, OrganisationOut
from app.models.task import Task, TaskCreate

class UserBase(BaseModel):
    username: str
    email: EmailStr

class CourtsCreate(BaseModel):
    organisations: Optional[List[OrganisationCreate]] = []
    tasks: Optional[List[TaskCreate]] = []

class UserPublicFields(UserBase):
    id: int
    organisations: List[OrganisationOut] = []
    tasks: List[Task] = []
    class Config:
        from_attributes = True
        orm_mode = True
