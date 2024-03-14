from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.mixins import TimeTracked
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.file import SquadLogoFile, SquadPhotosFile
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

    logo: Mapped["SquadLogoFile"] = relationship(
        back_populates="squad",
        primaryjoin="Squad.id == foreign(SquadLogoFile.object_id)",
        uselist=False,
    )
    photos: Mapped[list["SquadPhotosFile"]] = relationship(
        back_populates="squad",
        primaryjoin="Squad.id == foreign(SquadPhotosFile.object_id)",
        uselist=True,
    )

    def __repr__(self):
        return f"<Squad {self.id}>"
