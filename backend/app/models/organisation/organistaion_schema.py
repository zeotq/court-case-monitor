from pydantic import BaseModel


class OrganisationBase(BaseModel):
    inn: str
    ogrn: str
    name: str

class OrganisationCreate(OrganisationBase):
    pass

class OrganisationOut(OrganisationBase):
    id: int
    class Config:
        from_attributes = True
