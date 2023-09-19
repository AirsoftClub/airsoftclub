import secrets

from app.models.file import File
from app.repositories.users import UserRepository
from app.schemas.auth import GoogleTokenRequest, RefreshTokenRequest
from app.schemas.users import (
    TokenFamilyResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.security.auth import (
    generate_token_family_from_refresh,
    generate_token_family_from_user,
    get_google_user_data,
)
from app.security.password import Hash
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(
    user: UserRegisterRequest,
    user_repository: UserRepository = Depends(),
):
    if user_repository.get_by_email(user.email) is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = Hash.bcrypt(user.password)

    return user_repository.create(user)


@router.post("/login", response_model=TokenFamilyResponse)
def login(
    user: UserLoginRequest,
    user_repository: UserRepository = Depends(),
):
    db_user = user_repository.get_by_email(user.email)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not Hash.verify(user.password, db_user.password):
        raise HTTPException(status_code=404, detail="User not found")

    return generate_token_family_from_user(db_user.id)


@router.post("/refresh", response_model=TokenFamilyResponse)
def refresh(request: RefreshTokenRequest):
    return generate_token_family_from_refresh(request.refresh_token)


@router.post("/google/login", response_model=TokenFamilyResponse)
def google_login(
    google_token: GoogleTokenRequest, user_repository: UserRepository = Depends()
):
    user_data = get_google_user_data(google_token.token)

    if not user_data.email_verified:
        raise HTTPException(status_code=401, detail="Email not verified")

    user = user_repository.get_by_email(user_data.email)

    if not user:
        user = user_repository.create(
            UserRegisterRequest(
                name=user_data.given_name,
                lastname=user_data.family_name,
                email=user_data.email,
                password=secrets.token_urlsafe(),
            )
        )

    user.avatar = File(path=user_data.picture)
    user_repository.update(user)

    return generate_token_family_from_user(user.id)
