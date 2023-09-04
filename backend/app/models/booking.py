from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.team import Team
    from app.models.user import User


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    game_id = Column(Integer, ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="bookings")

    player_id = Column(Integer, ForeignKey("users.id"))
    player: Mapped["User"] = relationship(back_populates="bookings")

    team_id = Column(Integer, ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship()
