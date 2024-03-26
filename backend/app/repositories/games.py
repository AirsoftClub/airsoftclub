from datetime import datetime

from app.core.database import get_db
from app.models.field import Field
from app.models.game import Game
from app.models.team import Team
from app.schemas.games import CreateGameRequest
from fastapi import Depends
from sqlalchemy.orm import Session


class GameRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_joinable_games(self) -> list[Game]:
        return self.db.query(Game).filter(Game.played_at > datetime.utcnow()).all()

    def get_game(self, game_id: int) -> Game:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def create(self, payload: CreateGameRequest, field: Field) -> Game:
        teams = [
            Team(name=name, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            for name in payload.teams
        ]
        game = Game(
            **payload.model_dump(exclude=["teams"]),
            teams=teams,
            field=field,
            created_at=datetime.utcnow(),
        )

        self.db.add(game)
        self.db.commit()

        return game
