from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, Double, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.game import Game
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
    owner: Mapped["User"] = relationship(back_populates="fields")

    avatar_id = Column(Integer, ForeignKey("files.id"))
    avatar: Mapped["File"] = relationship()

    photos: Mapped[list["File"]] = relationship(secondary=fields_photos)

    games: Mapped[list["Game"]] = relationship(
        back_populates="field",
    )

    def __repr__(self):
        return f"<Field {self.name}>"
