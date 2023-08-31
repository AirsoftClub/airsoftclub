from app.endpoints import users
from fastapi import APIRouter

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
