from app.endpoints.fields import get_owned_field
from app.models.field import Field
from app.models.game import Game
from app.models.user import User
from app.repositories.games import GameRepository
from app.schemas.bookings import BookingResponse
from app.schemas.games import CreateGameRequest, GameResponse
from app.schemas.teams import TeamResponse
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(dependencies=[Depends(get_current_user)])


def get_current_game(
    game_id: int,
    game_repository: GameRepository = Depends(),
) -> Game:
    """
    Returns game for the passed game_id
    Raises 404 if game not found
    """
    game = game_repository.get_game(game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


def get_owned_game(
    game: Game = Depends(get_current_user),
    current_user: User = Depends(get_current_user),
) -> Game:
    if current_user != game.field.owner:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this game"
        )

    return game


@router.post("/field/{field_id}/", response_model=GameResponse)
def create_game(
    payload: CreateGameRequest,
    field: Field = Depends(get_owned_field),
    game_repository: GameRepository = Depends(),
):
    return game_repository.create(payload, field)


@router.get("/", response_model=list[GameResponse])
def get_joinable_games(
    game_repository: GameRepository = Depends(),
) -> list[GameResponse]:
    return game_repository.get_joinable_games()


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game: Game = Depends(get_current_game)) -> GameResponse:
    return game


@router.get("/{game_id}/bookings", response_model=list[BookingResponse])
def get_game_bookings(
    accepted: bool,
    game: Game = Depends(get_owned_game),
) -> list[BookingResponse]:
    if accepted:
        return game.accepted_bookings
    return game.pending_bookings


@router.get("/{game_id}/teams", response_model=list[TeamResponse])
def get_game_teams(game: Game = Depends(get_current_game)) -> list[TeamResponse]:
    return game.teams
