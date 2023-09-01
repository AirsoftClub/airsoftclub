from app.endpoints import fields, users
from fastapi import APIRouter

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(fields.router, prefix="/fields", tags=["fields"])
