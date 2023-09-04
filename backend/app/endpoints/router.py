from app.endpoints import bookings, fields, games, teams, users
from fastapi import APIRouter

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(fields.router, prefix="/fields", tags=["fields"])
router.include_router(games.router, prefix="/games", tags=["games"])
router.include_router(teams.router, prefix="/teams", tags=["teams"])
router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
