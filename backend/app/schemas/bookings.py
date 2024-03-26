from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    game_id: int
    player_id: int
    team_id: int
    created_at: datetime


class BookingRequest(BaseModel):
    team_name: str
