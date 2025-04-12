from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

user_organisation = Table(
    "user_organisation",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("organisation_id", Integer, ForeignKey("organisations.id"), primary_key=True),
)
