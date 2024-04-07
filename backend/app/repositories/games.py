import datetime

from app.core.database import get_db
from app.models.game import Game
from fastapi import Depends
from sqlalchemy.orm import Session


class GameRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_joinable_games(self) -> list[Game]:
        return (
            self.db.query(Game)
            .filter(Game.played_at > datetime.datetime.now(datetime.UTC))
            .all()
        )

    def get_game(self, id: int) -> Game:
        return self.db.query(Game).filter(Game.id == id).first()
