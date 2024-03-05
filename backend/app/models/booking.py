from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.mixins import TimeTracked
from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.team import Team
    from app.models.user import User


class Booking(Base, TimeTracked):  # TODO: add invoice files
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    game_id = Column(Integer, ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="bookings")

    player_id = Column(Integer, ForeignKey("users.id"))
    player: Mapped["User"] = relationship(back_populates="bookings")

    team_id = Column(Integer, ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship()

    accepted = Column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<Booking {self.id}>"
