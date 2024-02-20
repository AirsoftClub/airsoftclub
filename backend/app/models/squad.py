from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.mixins import TimeTracked
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.file import SquadAvatarFile, SquadsPhotoFile
    from app.models.user import User


SquadMember = Table(
    "squad_members",
    Base.metadata,
    Column("squad_id", ForeignKey("squads.id")),
    Column("user_id", ForeignKey("users.id")),
)

SquadInvitations = Table(
    "squad_invitations",
    Base.metadata,
    Column("squad_id", ForeignKey("squads.id")),
    Column("user_id", ForeignKey("users.id")),
)

SquadApplications = Table(
    "squad_applications",
    Base.metadata,
    Column("squad_id", ForeignKey("squads.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Squad(Base, TimeTracked):
    __tablename__ = "squads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    avatar: Mapped["SquadAvatarFile"] = relationship(back_populates="squad")
    photos: Mapped[list["SquadsPhotoFile"]] = relationship(back_populates="squad")

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="owned_squads")

    members: Mapped[list["User"]] = relationship(
        secondary=SquadMember, back_populates="squads"
    )

    invitations: Mapped[list["User"]] = relationship(
        secondary=SquadInvitations, back_populates="squad_invitations"
    )

    applications: Mapped[list["User"]] = relationship(
        secondary=SquadApplications, back_populates="squad_applications"
    )

    def __repr__(self):
        return f"<Squad {self.id}>"
