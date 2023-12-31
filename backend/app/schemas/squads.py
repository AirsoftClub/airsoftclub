from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.files import AvatarResponse
from app.schemas.users import UserResponse


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
