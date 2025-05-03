from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.association_tables import user_organisation


class OrganisationDB(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    inn = Column(String(12), nullable=True)
    name = Column(String(255), nullable=True)

    users = relationship(
        "UserDB", secondary=user_organisation, back_populates="organisations", passive_deletes=True
    )
    
    cases_as_plaintiff = relationship(
        "CourtCaseDB", foreign_keys="CourtCaseDB.plaintiff_id", back_populates="plaintiff"
    )
    cases_as_respondent = relationship(
        "CourtCaseDB", foreign_keys="CourtCaseDB.respondent_id", back_populates="respondent"
    )