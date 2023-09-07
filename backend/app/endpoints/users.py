from pathlib import Path

from app.models.file import File
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas.users import (
    UserAuthenticatedResponse,
    UserJWTPayload,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    UserUpdateRequest,
)
from app.security.auth import get_current_user, token_encode
from app.security.password import Hash
from fastapi import APIRouter, Depends, HTTPException, UploadFile

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return user_repository.get_all()


@router.post("/register", response_model=UserResponse)
def register(
    user: UserRegisterRequest,
    user_repository: UserRepository = Depends(),
):
    if user_repository.get_by_email(user.email) is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = Hash.bcrypt(user.password)

    return user_repository.create(user)


@router.post("/login", response_model=UserAuthenticatedResponse)
def login(
    user: UserLoginRequest,
    user_repository: UserRepository = Depends(),
):
    db_user = user_repository.get_by_email(user.email)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not Hash.verify(user.password, db_user.password):
        raise HTTPException(status_code=404, detail="User not found")

    db_user.token = token_encode(
        UserJWTPayload(
            id=db_user.id,
            name=db_user.name,
            lastname=db_user.lastname,
            email=db_user.email,
        )
    )

    return user_repository.update(db_user)


@router.get("/me", response_model=UserResponse)
def me(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return current_user


@router.post("/me", response_model=UserResponse)
def update_me(
    user: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    current_user.name = user.name
    current_user.lastname = user.lastname

    return user_repository.update(current_user)


@router.post("/me/avatar", response_model=UserResponse)
def me_avatar(
    avatar: UploadFile,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    if avatar.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    directory = Path("static/avatars") / str(current_user.id)

    if not directory.exists():
        directory.mkdir(parents=True)

    file_path = directory / str(avatar.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(avatar.file.read())

    user = user_repository.get_by_id(current_user.id)
    user.avatar = File(path=file_path.as_posix())

    return user_repository.update(user)
