from app.models.user import User
from app.repositories.bookings import BookingRepository
from app.repositories.games import GameRepository
from app.repositories.teams import TeamRepository
from app.schemas.bookings import BookingCreateRequest, BookingResponse
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()


@router.post("/", response_model=BookingResponse)
def book_game(
    create_request: BookingCreateRequest,
    current_user: User = Depends(get_current_user),
    booking_repository: BookingRepository = Depends(),
    game_repository: GameRepository = Depends(),
    team_repository: TeamRepository = Depends(),
):
    game = game_repository.get_game(create_request.game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if len(game.players) >= game.max_players:
        raise HTTPException(status_code=400, detail="Game is full")

    booking = booking_repository.get_player_booking_by_game_id(
        create_request.game_id, current_user.id
    )

    if booking:
        raise HTTPException(status_code=400, detail="Already booked")

    team_with_less_players = team_repository.get_team_with_less_players(
        create_request.game_id
    )

    if not team_with_less_players:
        raise HTTPException(status_code=400, detail="No teams available")

    return booking_repository.book_game(
        create_request.game_id, current_user.id, team_with_less_players.id
    )


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
