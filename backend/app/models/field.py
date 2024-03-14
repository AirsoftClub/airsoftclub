from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.mixins import TimeTracked
from sqlalchemy import Column, Double, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.file import FieldAvatarFile, FieldPhotoFile
    from app.models.game import Game
    from app.models.user import User


class Field(Base, TimeTracked):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    latitude = Column(Double, nullable=True)
    longitude = Column(Double, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="fields")

    avatar: Mapped["FieldAvatarFile"] = relationship(back_populates="field")
    photos: Mapped[list["FieldPhotoFile"]] = relationship(back_populates="field")

    games: Mapped[list["Game"]] = relationship(
        back_populates="field",
    )

    def __repr__(self):
        return f"<Field {self.name}>"
