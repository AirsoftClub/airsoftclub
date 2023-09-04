from app.models.booking import Booking
from app.models.team import Team
from sqlalchemy import func
from sqlalchemy.orm import Session


class TeamRepository:
    def get_teams_by_game_id(self, db: Session, game_id: int) -> list[Team]:
        return db.query(Team).filter(Team.game_id == game_id).all()

    def get_team_with_less_players(self, db: Session, game_id: int) -> Team | None:
        return (
            db.query(Team)
            .outerjoin(Booking)
            .filter(Team.game_id == game_id)
            .group_by(Team.id)
            .order_by(func.count(Booking.id).label("bookings_count"))
            .first()
        )
