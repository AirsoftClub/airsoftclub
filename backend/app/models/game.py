from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.booking import Booking
from app.models.mixins import TimeTracked
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.field import Field
    from app.models.file import GameLogoFile, GamePhotosFile
    from app.models.team import Team
    from app.models.user import User


class Game(Base, TimeTracked):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    max_players = Column(Integer)
    played_at = Column(DateTime)

    field_id = Column(Integer, ForeignKey("fields.id"))
    field: Mapped["Field"] = relationship(back_populates="games")

    teams: Mapped[list["Team"]] = relationship(back_populates="game")

    bookings: Mapped[list["Booking"]] = relationship(back_populates="game")

    players: AssociationProxy[list["User"]] = association_proxy("bookings", "player")

    logo: Mapped["GameLogoFile"] = relationship(
        back_populates="game",
        primaryjoin="Game.id == foreign(GameLogoFile.object_id)",
        uselist=False,
    )
    photos: Mapped[list["GamePhotosFile"]] = relationship(
        back_populates="game",
        primaryjoin="Game.id == foreign(GamePhotosFile.object_id)",
        uselist=True,
    )

    def __repr__(self) -> str:
        return f"<Game {self.name}>"
