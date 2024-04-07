import calendar
import datetime
from typing import Annotated

import jwt
from app.core.settings import settings
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas.auth import GoogleDecodedJWT
from app.schemas.users import UserJWTPayload
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


TOKEN_EXPIRATION = 15
REFRESH_TOKEN_EXPIRATION = 60


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


def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return current_user


def token_encode(payload: UserJWTPayload) -> str:
    return jwt.encode(payload.model_dump(), settings.app_secret, algorithm="HS256")


def token_decode(token: str) -> UserJWTPayload:
    payload = jwt.decode(
        token,
        settings.app_secret,
        algorithms=["HS256"],
        audience=settings.app_url,
        issuer=settings.app_url,
        verify=True,
    )
    return UserJWTPayload(**payload)


def generate_token_from_refresh(token: str, expiration: int) -> str:
    payload = token_decode(token)

    exp = calendar.timegm(
        (
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expiration)
        ).timetuple()
    )
    now = calendar.timegm(datetime.datetime.now(datetime.UTC).timetuple())

    payload.exp = exp
    payload.iat = now
    payload.nbf = now

    return token_encode(payload)


def generate_token_family_from_refresh(token: str) -> dict[str, str]:
    token = generate_token_from_refresh(token, TOKEN_EXPIRATION)
    refresh_token = generate_token_from_refresh(token, REFRESH_TOKEN_EXPIRATION)

    return {"token": token, "refresh_token": refresh_token}


def generate_token_from_user(user_id: int, expiration: int) -> str:
    exp = calendar.timegm(
        (
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expiration)
        ).timetuple()
    )
    now = calendar.timegm(datetime.datetime.now(datetime.UTC).timetuple())

    return token_encode(
        UserJWTPayload(
            id=user_id,
            iss=settings.app_url,
            aud=settings.app_url,
            exp=exp,
            nbf=now,
            iat=now,
        )
    )


def generate_token_family_from_user(user_id: int) -> dict[str, str]:
    token = generate_token_from_user(user_id, TOKEN_EXPIRATION)
    refresh_token = generate_token_from_user(user_id, REFRESH_TOKEN_EXPIRATION)

    return {"token": token, "refresh_token": refresh_token}


def get_google_user_data(token: str) -> GoogleDecodedJWT:
    try:
        url = "https://www.googleapis.com/oauth2/v2/certs"
        jwk_client = jwt.PyJWKClient(url, cache_keys=True)
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.google_client_id,
        )
        return GoogleDecodedJWT(**payload)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
