from datetime import datetime

import factory
from app.models.field import Field


class FieldFactory(factory.Factory):
    class Meta:
        model = Field

    id: int
    name = factory.Faker("name")
    description = factory.Faker("text")
    cords_x = factory.Faker("pyint")
    cords_y = factory.Faker("pyint")
    avatar_id = None
    owner_id = None
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
