from typing import Optional

from app.schemas.files import AvatarResponse
from pydantic import BaseModel, ConfigDict


class FieldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    cords_x: int
    cords_y: int
    avatar: Optional[AvatarResponse] = None
