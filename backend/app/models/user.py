from datetime import datetime

from app.models.base import Base
from app.models.file import File
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    avatar_id = Column(
        Integer,
        ForeignKey("files.id"),
        nullable=True,
    )
    avatar: Mapped["File"] = relationship("File", uselist=False)

    def __repr__(self):
        return f"<User {self.id}>"
