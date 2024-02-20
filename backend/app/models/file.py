from app.models.base import Base
from app.models.field import Field
from app.models.mixins import TimeTracked
from app.models.squad import Squad
from app.models.user import User
from sqlalchemy.orm import Mapped, mapped_column, relationship


class File(Base, TimeTracked):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str]

    type: Mapped[str]
    object_id: Mapped[int]

    __mapper_args__ = {"polymorphic_identity": "file", "polymorphic_on": "type"}

    @property
    def url(self):
        return f"{self.path}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


class FieldPhotoFile(File):
    __mapper_args__ = {"polymorphic_identity": "field_photo_file"}

    field = relationship(
        Field,
        primaryjoin="Field.id==foreign(File.object_id)",
        back_populates="photos",
        uselist=False,
    )


class FieldAvatarFile(File):
    __mapper_args__ = {"polymorphic_identity": "field_avatar_file"}

    field = relationship(
        Field,
        primaryjoin="Field.id==foreign(File.object_id)",
        back_populates="avatar",
        uselist=False,
    )


class SquadsPhotoFile(File):
    __mapper_args__ = {"polymorphic_identity": "squad_photo_file"}

    squad = relationship(
        Squad,
        primaryjoin="Squad.id==foreign(File.object_id)",
        back_populates="photos",
        uselist=False,
    )


class SquadAvatarFile(File):
    __mapper_args__ = {"polymorphic_identity": "squad_avatar_file"}

    squad = relationship(
        Squad,
        primaryjoin="Squad.id==foreign(File.object_id)",
        back_populates="avatar",
        uselist=False,
    )


class UserPhotoFile(File):
    __mapper_args__ = {"polymorphic_identity": "user_photo_file"}

    user = relationship(
        User,
        primaryjoin="User.id==foreign(File.object_id)",
        back_populates="photos",
        uselist=False,
    )


class UserAvatarFile(File):
    __mapper_args__ = {"polymorphic_identity": "user_avatar_file"}

    user: Mapped["User"] = relationship(back_populates="avatar")
