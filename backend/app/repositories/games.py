from datetime import datetime

from app.models.booking import Booking
from app.models.game import Game
from app.models.team import Team
from sqlalchemy.orm import Session


class GameRepository:
    def get_joinable_games(self, db: Session) -> list[Game]:
        return db.query(Game).filter(Game.played_at > datetime.utcnow()).all()

    def get_game(self, db: Session, id: int) -> Game:
        return db.query(Game).filter(Game.id == id).first()

    def get_game_bookings(self, db: Session, id: int) -> list[Booking]:
        game = self.get_game(db, id)
        return game.bookings

    def get_game_teams(self, db: Session, id: int) -> list[Team]:
        game = self.get_game(db, id)
        return game.teams
