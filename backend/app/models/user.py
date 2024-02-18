from typing import TYPE_CHECKING, List

from app.models.base import Base
from app.models.mixins import TimeTracked
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.field import Field
    from app.models.file import File
    from app.models.game import Game
    from app.models.squad import Squad


class User(Base, TimeTracked):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    avatar_id = Column(
        Integer,
        ForeignKey("files.id"),
        nullable=True,
    )
    avatar: Mapped["File"] = relationship()

    fields: Mapped["Field"] = relationship("Field", back_populates="owner")

    bookings: Mapped[list["Booking"]] = relationship(back_populates="player")

    games: AssociationProxy[list["Game"]] = association_proxy("bookings", "game")

    owned_squads: Mapped[List["Squad"]] = relationship(back_populates="owner")

    squads: Mapped[list["Squad"]] = relationship(
        secondary="squad_members", back_populates="members"
    )

    squad_invitations: Mapped[list["Squad"]] = relationship(
        secondary="squad_invitations", back_populates="invitations"
    )

    squad_applications: Mapped[list["Squad"]] = relationship(
        secondary="squad_applications", back_populates="applications"
    )

    def __repr__(self):
        return f"<User {self.id}>"
