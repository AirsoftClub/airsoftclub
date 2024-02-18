from typing import Optional

from app.schemas.files import AvatarResponse
from app.schemas.users import UserResponse
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SquadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    avatar: Optional[AvatarResponse]
    owner: UserResponse


class SquadUpsertRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(max_length=200)


class SquadUpdateRequest(BaseModel):
    name: str | None = Field(min_length=3, max_length=50, default=None)
    description: str | None = Field(max_length=200, default=None)


class SquadInvitationRequest(BaseModel):
    email: EmailStr


class SquadReplyRequest(BaseModel):
    accept: bool
