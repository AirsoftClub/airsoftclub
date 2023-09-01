from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, Double, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.user import User


fields_photos = Table(
    "fields_photos",
    Base.metadata,
    Column("field_id", Integer, ForeignKey("fields.id")),
    Column("file_id", Integer, ForeignKey("files.id")),
)


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    cords_x = Column(Double, nullable=True)
    cords_y = Column(Double, nullable=True)
    created_at = Column(String, nullable=True, default=datetime.utcnow)
    updated_at = Column(
        String, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="fields")

    avatar_id = Column(Integer, ForeignKey("files.id"))
    avatar: Mapped["File"] = relationship("File", uselist=False)

    photos: Mapped[list["File"]] = relationship("File", secondary=fields_photos)

    def __repr__(self):
        return f"<Field {self.name}>"
