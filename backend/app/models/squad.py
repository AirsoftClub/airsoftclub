from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.mixins import TimeTracked
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.user import User


squads_photos = Table(
    "squads_photos",
    Base.metadata,
    Column("squad_id", Integer, ForeignKey("squads.id")),
    Column("file_id", Integer, ForeignKey("files.id")),
)

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

    avatar_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"))
    avatar: Mapped["File"] = relationship("File")

    photos: Mapped[list["File"]] = relationship(secondary=squads_photos)

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
