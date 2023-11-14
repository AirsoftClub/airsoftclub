from fastapi import APIRouter

from app.endpoints import auth, bookings, fields, games, squads, teams, users

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(fields.router, prefix="/fields", tags=["fields"])
router.include_router(games.router, prefix="/games", tags=["games"])
router.include_router(teams.router, prefix="/teams", tags=["teams"])
router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(squads.router, prefix="/squads", tags=["squads"])
