from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.association_tables import user_organisation


class CourtCaseDB(Base):
    __tablename__ = "court_cases"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    case_number = Column(String(50), nullable=False, unique=True)
    case_link = Column(String(512))
    court = Column(String(255))
    

    plaintiff_id = Column(Integer, ForeignKey('organisations.id'), nullable=True, index=True)
    respondent_id = Column(Integer, ForeignKey('organisations.id'), nullable=True, index=True)


    plaintiff = relationship(
        "OrganisationDB", foreign_keys=[plaintiff_id], back_populates="cases_as_plaintiff"
    )
    respondent = relationship(
        "OrganisationDB", foreign_keys=[respondent_id], back_populates="cases_as_respondent"
    )