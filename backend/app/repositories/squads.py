import datetime
from pathlib import Path

from app.core.database import get_db
from app.models.file import SquadLogoFile
from app.models.squad import Squad
from app.models.user import User
from app.schemas.squads import SquadUpdateRequest
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session


class SquadRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_squads(self) -> list[Squad]:
        return self.db.query(Squad).filter(Squad.deleted_at.is_(None)).all()

    def get_squad(self, id: int) -> Squad:
        return (
            self.db.query(Squad)
            .filter(Squad.id == id)
            .filter(Squad.deleted_at.is_(None))
            .first()
        )

    def get_count_by_name(self, name: str) -> int:
        return self.db.query(Squad).filter(Squad.name == name).count()

    def get_count_by_owner(self, owner_id: str) -> int:
        return (
            self.db.query(Squad)
            .filter(Squad.owner.has(id=owner_id))
            .filter(Squad.deleted_at.is_(None))
            .count()
        )

    def upsert_squad(self, squad: Squad) -> Squad:
        self.db.add(squad)
        self.db.commit()
        self.db.refresh(squad)
        return squad

    def update_squad(self, squad: Squad, payload: SquadUpdateRequest):
        if payload.name:
            squad.name = payload.name
        if payload.description:
            squad.description = payload.description
        self.db.add(squad)
        self.db.commit()

        return squad

    def add_squad_photos(
        self, squad: Squad, photos: list[UploadFile]
    ) -> list[SquadLogoFile]:
        directory = Path(f"static/squads/{squad.id}/photos")

        if not directory.exists():
            directory.mkdir(parents=True)

        for photo in photos:
            path = directory / str(photo.filename)
            with path.open("wb") as buffer:
                buffer.write(photo.file.read())
            squad.photos.append(SquadLogoFile(path=path.as_posix()))

        self.db.commit()
        self.db.refresh(squad)
        return squad.photos

    def add_squad_logo(self, squad: Squad, logo: UploadFile) -> SquadLogoFile:
        directory = Path(f"static/squads/{squad.id}/logo")

        if not directory.exists():
            directory.mkdir(parents=True)

        path = directory / str(logo.filename)
        with path.open("wb") as buffer:
            buffer.write(logo.file.read())

        squad.logo = SquadLogoFile(path=path.as_posix())
        squad = self.upsert_squad(squad)
        return squad.logo

    def invite_user(self, squad: Squad, user: User) -> None:
        squad.invitations.append(user)
        self.db.add(squad)
        self.db.commit()

    def apply_to_squad(self, squad: Squad, user: User) -> None:
        squad.applications.append(user)
        self.db.add(squad)
        self.db.commit()

    def accept_user(self, squad: Squad, user: User) -> None:
        if user in squad.invitations:
            # Remove invitations for this user
            squad.invitations.remove(user)

        if user in squad.applications:
            # Remove applications for this user
            squad.applications.remove(user)

        squad.members.append(user)
        self.db.add(squad)
        self.db.commit()

    def decline_user(self, squad: Squad, user: User) -> None:
        if user in squad.invitations:
            # Remove invitations for this user
            squad.invitations.remove(user)

        if user in squad.applications:
            # Remove applications for this user
            squad.applications.remove(user)
        self.db.add(squad)
        self.db.commit()

    def delete_squad(self, squad: Squad) -> Squad:
        squad.deleted_at = datetime.datetime.now(datetime.UTC)
        return self.upsert_squad(squad)

    def touch(self, squad: Squad) -> None:
        self.db.add(squad)
        self.db.commit()
