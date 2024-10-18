from datetime import datetime

from app.models.field import Field
from factory import Faker, LazyFunction, Sequence
from factory.alchemy import SQLAlchemyModelFactory


class FieldFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Field
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n)
    name = Faker("name")
    description = Faker("text")
    latitude = Faker("latitude")
    longitude = Faker("longitude")
    owner_id = None
    created_at = LazyFunction(datetime.now)
    updated_at = LazyFunction(datetime.now)
