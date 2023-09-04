from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.game import Game
    from app.models.user import User


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    game_id = Column(Integer, ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="teams")

    bookings: Mapped[list["Booking"]] = relationship(back_populates="team")

    players: AssociationProxy[list["User"]] = association_proxy("bookings", "player")

    def __repr__(self) -> str:
        return f"<Team {self.name}>"
