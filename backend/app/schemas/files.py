from pydantic import BaseModel, ConfigDict


class AvatarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str


class FieldPhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str
