from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class BannedUsersDB(Base):
    __tablename__ = "banned_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    reason = Column(String(500), nullable=False)
    banned_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserDB", back_populates="bans")