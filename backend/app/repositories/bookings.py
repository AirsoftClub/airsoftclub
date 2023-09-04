from app.models.game import Booking
from sqlalchemy.orm import Session


class BookingRepository:
    def get_bookigns_by_game_id(self, db: Session, game_id: int) -> list[Booking]:
        return db.query(Booking).filter(Booking.game_id == game_id).all()

    def get_player_booking_by_game_id(
        self, db: Session, game_id: int, user_id: int
    ) -> Booking:
        return (
            db.query(Booking)
            .filter(Booking.game_id == game_id, Booking.player_id == user_id)
            .first()
        )

    def book_game(
        self, db: Session, game_id: int, user_id: int, team_id: int
    ) -> Booking:
        booking = Booking(game_id=game_id, player_id=user_id, team_id=team_id)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    def leave_game(self, db: Session, id: int) -> None:
        db.query(Booking).filter(Booking.id == id).delete()
        db.commit()
