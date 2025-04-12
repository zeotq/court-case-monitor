from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    class Config:
        from_attributes = True
