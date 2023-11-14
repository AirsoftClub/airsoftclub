from pydantic import BaseModel, ConfigDict


class AvatarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str


class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str
