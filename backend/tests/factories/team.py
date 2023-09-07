from datetime import datetime

import factory
from app.models.team import Team


class TeamFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Team
        sqlalchemy_session_persistence = "commit"

    id: factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
