from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.file import File
from app.models.squad import Squad


class SquadRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_squads(self) -> List[Squad]:
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

    def upsert_squad(self, squad: Squad) -> Squad:
        self.db.add(squad)
        self.db.commit()
        self.db.refresh(squad)
        return squad

    def add_squad_photos(self, squad: Squad, photos: List[UploadFile]) -> List[File]:
        directory = Path(f"static/squads/{squad.id}/photos")

        if not directory.exists():
            directory.mkdir(parents=True)

        for photo in photos:
            path = directory / str(photo.filename)
            with path.open("wb") as buffer:
                buffer.write(photo.file.read())
            squad.photos.append(File(path=path.as_posix()))

        self.db.commit()
        self.db.refresh(squad)
        return squad.photos

    def add_squad_avatar(self, squad: Squad, avatar: UploadFile) -> File:
        directory = Path(f"static/squads/{squad.id}/avatar")

        if not directory.exists():
            directory.mkdir(parents=True)

        path = directory / str(avatar.filename)
        with path.open("wb") as buffer:
            buffer.write(avatar.file.read())

        squad.avatar = File(path=path.as_posix())
        squad = self.upsert_squad(squad)
        return squad.avatar

    def delete_squad(self, squad: Squad) -> Squad:
        squad.deleted_at = datetime.utcnow()
        return self.upsert_squad(squad)
