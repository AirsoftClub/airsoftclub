import factory
from app.models.booking import Booking


class BookingFactory(factory.Factory):
    class Meta:
        model = Booking

    id: int

    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")
    game_id: int
    player_id: int
    team_id: int
