from app.core.database import get_db
from app.models.booking import Booking
from app.models.team import Team
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session


class TeamRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_teams_by_game_id(self, game_id: int) -> list[Team]:
        return self.db.query(Team).filter(Team.game_id == game_id).all()

    def get_team_with_less_players(self, game_id: int) -> Team | None:
        return (
            self.db.query(Team)
            .outerjoin(Booking)
            .filter(Team.game_id == game_id)
            .group_by(Team.id)
            .order_by(func.count(Booking.id).label("bookings_count"))
            .first()
        )
