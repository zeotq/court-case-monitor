from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.association_tables import user_organisation

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    organisations = relationship(
        "OrganisationDB", secondary=user_organisation, back_populates="users"
    )
    tasks = relationship("TaskDB", back_populates="user", cascade="all, delete")
