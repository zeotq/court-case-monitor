from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.association_tables import user_organisation


class OrganisationDB(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    inn = Column(String, unique=True, nullable=False)
    ogrn = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    users = relationship(
        "UserDB", secondary=user_organisation, back_populates="organisations"
    )
