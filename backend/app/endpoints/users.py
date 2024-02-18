from pathlib import Path

from app.models.file import File
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas.squads import SquadResponse
from app.schemas.users import UserResponse, UserUpdateRequest
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, UploadFile

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return user_repository.get_all()


@router.get("/me", response_model=UserResponse)
def me(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return current_user


@router.get("/me/squads", response_model=list[SquadResponse])
def my_squads(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return current_user.squads


@router.get("/me/invites", response_model=list[SquadResponse])
def my_invites(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return current_user.squad_invitations


@router.get("/me/applies", response_model=list[SquadResponse])
def my_applies(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return current_user.squad_applications


@router.post("/me", response_model=UserResponse)
def update_me(
    payload: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    return user_repository.update(current_user, payload)


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

    # TODO: Fix this
    return user_repository.update(user)
