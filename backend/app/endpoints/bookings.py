from app.endpoints.games import get_current_game
from app.models.game import Game
from app.models.user import User
from app.repositories.bookings import BookingRepository
from app.repositories.games import GameRepository
from app.repositories.teams import TeamRepository
from app.schemas.bookings import BookingRequest, BookingResponse
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()


@router.post("/game/{game_id}", response_model=BookingResponse)
def book_game(
    payload: BookingRequest,
    game: Game = Depends(get_current_game),
    current_user: User = Depends(get_current_user),
    booking_repository: BookingRepository = Depends(),
    game_repository: GameRepository = Depends(),
    team_repository: TeamRepository = Depends(),
):
    if len(game.players) >= game.max_players:
        raise HTTPException(status_code=400, detail="Game is full")

    already_booked = booking_repository.get_player_booking_by_game_id(
        game.id, current_user.id
    )

    if already_booked:
        raise HTTPException(status_code=400, detail="Already booked")

    team = team_repository.get_by_name(game_id=game.id, name=payload.team_name)

    if not team:
        raise HTTPException(status_code=400, detail="No teams available")

    return booking_repository.book_game(game.id, current_user.id, team.id)


@router.delete("/{id}/", responses={HTTP_204_NO_CONTENT: {"model": None}})
def leave_game(
    id: int,
    current_user: User = Depends(get_current_user),
    booking_repository: BookingRepository = Depends(),
):
    booking = booking_repository.get_booking(id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.player_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    booking_repository.leave_game(id)

    return Response(status_code=HTTP_204_NO_CONTENT)
