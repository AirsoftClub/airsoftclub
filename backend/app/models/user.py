from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.field import Field
    from app.models.file import File


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

    fields: Mapped["Field"] = relationship("Field", back_populates="owner")

    def __repr__(self):
        return f"<User {self.id}>"
