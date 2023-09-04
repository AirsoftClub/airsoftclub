from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    played_at: datetime
    created_at: datetime
