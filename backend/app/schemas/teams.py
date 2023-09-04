from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
    updated_at: datetime
