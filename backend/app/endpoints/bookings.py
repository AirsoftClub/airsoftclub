from app.core.database import get_db
from app.repositories.bookings import BookingRepository
from app.repositories.games import GameRepository
from app.repositories.teams import TeamRepository
from app.schemas.bookings import BookingCreateRequest, BookingResponse
from app.schemas.users import UserJWTPayload
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()


@router.post("/", response_model=BookingResponse)
def book_game(
    create_request: BookingCreateRequest,
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    booking_repository: BookingRepository = Depends(BookingRepository),
    game_repository: GameRepository = Depends(GameRepository),
    team_repository: TeamRepository = Depends(TeamRepository),
):
    game = game_repository.get_game(db, create_request.game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    booking = booking_repository.get_player_booking_by_game_id(
        db, create_request.game_id, current_user.id
    )

    if booking:
        raise HTTPException(status_code=400, detail="Already booked")

    team_with_less_players = team_repository.get_team_with_less_players(
        db, create_request.game_id
    )

    if not team_with_less_players:
        raise HTTPException(status_code=400, detail="No teams available")

    return booking_repository.book_game(
        db, create_request.game_id, current_user.id, team_with_less_players.id
    )


@router.delete("/{id}/", responses={HTTP_204_NO_CONTENT: {"model": None}})
def leave_game(
    id: int,
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    booking_repository: BookingRepository = Depends(BookingRepository),
):
    booking_repository.leave_game(db, id)
    return Response(status_code=HTTP_204_NO_CONTENT)
