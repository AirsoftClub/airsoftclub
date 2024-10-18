from datetime import datetime
from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, ConfigDict, PositiveInt

Teams = Annotated[list[str], MinLen(2)]


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    played_at: datetime
    created_at: datetime


class CreateGameRequest(BaseModel):
    name: str
    description: str = None
    max_players: PositiveInt
    played_at: datetime
    teams: Teams
