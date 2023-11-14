from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.user import User


squads_photos = Table(
    "squads_photos",
    Base.metadata,
    Column("squad_id", Integer, ForeignKey("squads.id")),
    Column("file_id", Integer, ForeignKey("files.id")),
)


class SquadMember(Base):
    __tablename__ = "squads_members"

    id = Column(Integer, primary_key=True, index=True)

    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="CASCADE"))
    squad: Mapped["Squad"] = relationship(backref="squads_members")

    member_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    member: Mapped["User"] = relationship(backref="squads_members")

    def __repr__(self):
        return f"<SquadMember {self.id}>"


class SquadInvitation(Base):
    __tablename__ = "squads_invitations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="invitations")

    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="CASCADE"))
    squad: Mapped["Squad"] = relationship("Squad", back_populates="invitations")

    def __repr__(self):
        return f"<SquadInvitation {self.id}>"


class SquadApply(Base):
    __tablename__ = "squads_applies"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="applies")

    squad_id = Column(Integer, ForeignKey("squads.id", ondelete="CASCADE"))
    squad: Mapped["Squad"] = relationship("Squad", back_populates="applies")

    def __repr__(self):
        return f"<SquadApply {self.id}>"


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

    members: AssociationProxy[List["User"]] = association_proxy(
        "squads_members", "member"
    )

    invitations: Mapped[List["SquadInvitation"]] = relationship(back_populates="squad")

    applies: Mapped[List["SquadApply"]] = relationship(back_populates="squad")

    def __repr__(self):
        return f"<Squad {self.id}>"
