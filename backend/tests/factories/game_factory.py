from datetime import datetime

import factory
from app.models.game import Game


class GameFactory(factory.Factory):
    class Meta:
        model = Game

    id: int
    name = factory.Faker("first_name")
    description = factory.Faker("text")
    max_players = factory.Faker("pyint")
    played_at = factory.LazyFunction(datetime.now)
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
