from typing import Optional

from app.schemas.files import AvatarResponse
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lastname: str
    email: str
    avatar: Optional[AvatarResponse] = None


class TokenFamilyResponse(BaseModel):
    token: str
    refresh_token: str


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str
    lastname: str
    password: str


class UserUpdateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    lastname: str


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str


class UserJWTPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    iat: int
    exp: int
    nbf: int
    iss: str
    aud: str
