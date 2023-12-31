from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.booking import Booking
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.field import Field
    from app.models.team import Team
    from app.models.user import User


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    max_players = Column(Integer)
    played_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    field_id = Column(Integer, ForeignKey("fields.id"))
    field: Mapped["Field"] = relationship(back_populates="games")

    teams: Mapped[list["Team"]] = relationship(back_populates="game")

    bookings: Mapped[list["Booking"]] = relationship(back_populates="game")

    players: AssociationProxy[list["User"]] = association_proxy("bookings", "player")

    def __repr__(self) -> str:
        return f"<Game {self.name}>"
