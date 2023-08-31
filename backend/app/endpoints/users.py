import os

from app.core.database import get_db
from app.models.file import File
from app.repositories.users import UserRepository
from app.schemas.users import (
    UserAuthenticatedResponse,
    UserJWTPayload,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.security.auth import get_current_user, token_encode
from app.security.password import Hash
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    user_repository: UserRepository = Depends(UserRepository),
):
    return user_repository.get_all(db)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserRegisterRequest,
    db: Session = Depends(get_db),
    user_repository: UserRepository = Depends(UserRepository),
):
    user.password = Hash.bcrypt(user.password)
    user = user_repository.create(db, user)
    return user


@router.post("/login", response_model=UserAuthenticatedResponse)
def login(
    user: UserLoginRequest,
    db: Session = Depends(get_db),
    user_repository: UserRepository = Depends(UserRepository),
):
    db_user = user_repository.get_by_email(db, user.email)

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

    db.add(db_user)
    db.commit()

    return db_user


@router.get("/me", response_model=UserResponse)
def me(
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    user_repository: UserRepository = Depends(UserRepository),
):
    return user_repository.get_by_id(db, current_user.id)


@router.post("/me/avatar", response_model=UserResponse)
def me_avatar(
    avatar: UploadFile,
    current_user: UserJWTPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
    user_repository: UserRepository = Depends(UserRepository),
):
    if avatar.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    directory = os.path.join("static", "avatars", str(current_user.id))

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, avatar.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(avatar.file.read())

    user = user_repository.get_by_id(db, current_user.id)
    user.avatar = File(path=file_path)
    db.commit()
    db.refresh(user)

    return user
