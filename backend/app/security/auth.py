from typing import Annotated

import jwt
from app.core.settings import settings
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas.users import UserJWTPayload
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: UserRepository = Depends(),
) -> User:
    try:
        payload = token_decode(token)
        user = user_repository.get_by_id(payload.id)

        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")


def token_encode(payload: UserJWTPayload) -> str:
    return jwt.encode(payload.model_dump(), settings.app_secret, algorithm="HS256")


def token_decode(token: str) -> UserJWTPayload:
    payload = jwt.decode(token, settings.app_secret, algorithms=["HS256"])
    return UserJWTPayload(**payload)
