from app.models.base import Base
from app.models.booking import Booking
from app.models.field import Field
from app.models.game import Game
from app.models.mixins import TimeTracked
from app.models.squad import Squad
from app.models.user import User
from sqlalchemy import ForeignKey, ForeignKeyConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class File(Base, TimeTracked):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str]

    type: Mapped[str]
    object_id: Mapped[int]

    __mapper_args__ = {"polymorphic_identity": "file", "polymorphic_on": "type"}
    # TODO: Probably not the best way to do this
    __table_args__ = (
        ForeignKeyConstraint(["object_id"], ["bookings.id"]),
        ForeignKeyConstraint(["object_id"], ["fields.id"]),
        ForeignKeyConstraint(["object_id"], ["games.id"]),
        ForeignKeyConstraint(["object_id"], ["squads.id"]),
        ForeignKeyConstraint(["object_id"], ["users.id"]),
    )

    @property
    def url(self):
        return f"{self.path}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


# TODO: too many repeated code
class BookingConfirmationFile(File):
    __mapper_args__ = {"polymorphic_identity": "booking_confirmation_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        use_existing_column=True,
    )
    booking = relationship(
        Booking,
        primaryjoin="Booking.id == foreign(BookingConfirmationFile.object_id)",
        foreign_keys=[object_id],
        back_populates="confirmation",
        uselist=False,
    )


class FieldPhotosFile(File):
    __mapper_args__ = {"polymorphic_identity": "field_photos_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("fields.id"),
        nullable=False,
        use_existing_column=True,
    )
    field = relationship(
        Field,
        primaryjoin="Field.id == foreign(FieldPhotosFile.object_id)",
        foreign_keys=[object_id],
        back_populates="photos",
        uselist=False,
    )


class FieldLogoFile(File):
    __mapper_args__ = {"polymorphic_identity": "field_logo_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("fields.id"),
        nullable=False,
        use_existing_column=True,
    )
    field = relationship(
        Field,
        primaryjoin="Field.id == foreign(FieldLogoFile.object_id)",
        foreign_keys=[object_id],
        back_populates="logo",
        uselist=False,
    )


class GamePhotosFile(File):
    __mapper_args__ = {"polymorphic_identity": "game_photos_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("games.id"),
        nullable=False,
        use_existing_column=True,
    )

    game = relationship(
        Game,
        primaryjoin="Game.id == foreign(GamePhotosFile.object_id)",
        foreign_keys=[object_id],
        back_populates="photos",
        uselist=False,
    )


class GameLogoFile(File):
    __mapper_args__ = {"polymorphic_identity": "game_logo_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("games.id"),
        nullable=False,
        use_existing_column=True,
    )

    game = relationship(
        Game,
        primaryjoin="Game.id == foreign(GameLogoFile.object_id)",
        foreign_keys=[object_id],
        back_populates="logo",
        uselist=False,
    )


class SquadPhotosFile(File):
    __mapper_args__ = {"polymorphic_identity": "squad_photos_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("squads.id"),
        nullable=False,
        use_existing_column=True,
    )
    squad = relationship(
        Squad,
        primaryjoin="Squad.id == foreign(SquadPhotosFile.object_id)",
        foreign_keys=[object_id],
        back_populates="photos",
        uselist=False,
    )


class SquadLogoFile(File):
    __mapper_args__ = {"polymorphic_identity": "squad_logo_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("squads.id"),
        nullable=False,
        use_existing_column=True,
    )
    squad = relationship(
        Squad,
        primaryjoin="Squad.id == foreign(SquadLogoFile.object_id)",
        foreign_keys=[object_id],
        back_populates="logo",
        uselist=False,
    )


class UserPhotosFile(File):
    __mapper_args__ = {"polymorphic_identity": "user_photos_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        use_existing_column=True,
    )
    user = relationship(
        User,
        primaryjoin="User.id == foreign(UserPhotosFile.object_id)",
        foreign_keys=[object_id],
        back_populates="photos",
        uselist=False,
    )


class UserAvatarFile(File):
    __mapper_args__ = {"polymorphic_identity": "user_avatar_file"}

    object_id = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        use_existing_column=True,
    )
    user = relationship(
        User,
        primaryjoin="User.id == foreign(UserAvatarFile.object_id)",
        foreign_keys=[object_id],
        back_populates="avatar",
        uselist=False,
    )
