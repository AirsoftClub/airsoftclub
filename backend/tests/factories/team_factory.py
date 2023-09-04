from datetime import datetime

import factory
from app.models.team import Team


class TeamFactory(factory.Factory):
    class Meta:
        model = Team

    id: int
    name = factory.Faker("first_name")
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    game_id: int
