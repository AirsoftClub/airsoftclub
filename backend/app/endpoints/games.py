from app.core.database import get_db
from app.repositories.games import GameRepository
from app.schemas.bookings import BookingResponse
from app.schemas.games import GameResponse
from app.schemas.teams import TeamResponse
from app.schemas.users import UserJWTPayload
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=list[GameResponse])
def get_joinable_games(
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    games_repository: GameRepository = Depends(GameRepository),
) -> list[GameResponse]:
    return games_repository.get_joinable_games(db)


@router.get("/{id}", response_model=GameResponse)
def get_game(
    id: int,
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    games_repository: GameRepository = Depends(GameRepository),
) -> GameResponse:
    game = games_repository.get_game(db, id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.get("/{id}/bookings", response_model=list[BookingResponse])
def get_game_bookings(
    id: int,
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    games_repository: GameRepository = Depends(GameRepository),
) -> list[BookingResponse]:
    return games_repository.get_game_bookings(db, id)


@router.get("/{id}/teams", response_model=list[TeamResponse])
def get_game_teams(
    id: int,
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    games_repository: GameRepository = Depends(GameRepository),
) -> list[TeamResponse]:
    return games_repository.get_game_teams(db, id)
