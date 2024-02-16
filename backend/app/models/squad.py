from datetime import datetime
from typing import TYPE_CHECKING, List

from app.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
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


class Squad(Base):
    __tablename__ = "squads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)

    avatar_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"))
    avatar: Mapped["File"] = relationship("File")

    photos: Mapped[List["File"]] = relationship(secondary=squads_photos)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="owned_squads")

    members: Mapped[List["User"]] = relationship(
        secondary=SquadMember, back_populates="squads"
    )

    invitations: Mapped[List["User"]] = relationship(
        secondary=SquadInvitations, back_populates="squad_invitations"
    )

    applications: Mapped[List["User"]] = relationship(
        secondary=SquadApplications, back_populates="squad_applications"
    )

    def __repr__(self):
        return f"<Squad {self.id}>"
