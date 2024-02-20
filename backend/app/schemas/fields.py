from typing import Optional

from app.schemas.files import AvatarResponse
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.coordinate import Latitude, Longitude


class FieldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    latitude: Latitude | None = None
    longitude: Longitude | None = None
    avatar: Optional[AvatarResponse] = None


class FieldCreateSchema(BaseModel):
    name: str
    description: str | None = None
    longitude: Longitude | None = None
    latitude: Latitude | None = None


class FieldUpsertRequest(BaseModel):
    owner: EmailStr
    field: FieldCreateSchema
