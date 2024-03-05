from datetime import datetime

from app.core.database import get_db
from app.models.game import Booking
from fastapi import Depends
from sqlalchemy.orm import Session


class BookingRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_booking(self, id: int) -> Booking:
        return self.db.query(Booking).filter(Booking.id == id).first()

    def get_bookigns_by_game_id(self, game_id: int) -> list[Booking]:
        return self.db.query(Booking).filter(Booking.game_id == game_id).all()

    def get_player_booking_by_game_id(self, game_id: int, user_id: int) -> Booking:
        return (
            self.db.query(Booking)
            .filter(Booking.game_id == game_id, Booking.player_id == user_id)
            .first()
        )

    def book_game(self, game_id: int, user_id: int, team_id: int) -> Booking:
        booking = Booking(
            game_id=game_id,
            player_id=user_id,
            team_id=team_id,
            created_at=datetime.utcnow(),
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def leave_game(self, id: int) -> None:
        self.db.query(Booking).filter(Booking.id == id).delete()
        self.db.commit()
