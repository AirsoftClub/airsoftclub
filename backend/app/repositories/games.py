from datetime import datetime

from app.core.database import get_db
from app.models.booking import Booking
from app.models.game import Game
from app.models.team import Team
from fastapi import Depends
from sqlalchemy.orm import Session


class GameRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_joinable_games(self) -> list[Game]:
        return self.db.query(Game).filter(Game.played_at > datetime.utcnow()).all()

    def get_game(self, id: int) -> Game:
        return self.db.query(Game).filter(Game.id == id).first()

    def get_game_bookings(self, id: int) -> list[Booking]:
        game = self.get_game(id)
        return game.bookings

    def get_game_teams(self, id: int) -> list[Team]:
        game = self.get_game(id)
        return game.teams
