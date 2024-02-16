from datetime import datetime

from app.models.game import Game
from factory import Faker, LazyFunction, RelatedFactoryList, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory


class GameFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Game
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n)
    name = Faker("first_name")
    description = Faker("text")
    max_players = 100
    played_at = LazyFunction(datetime.now)
    created_at = LazyFunction(datetime.now)
    updated_at = LazyFunction(datetime.now)

    field = SubFactory("tests.factories.field.FieldFactory")

    bookings = RelatedFactoryList(
        "tests.factories.booking.BookingFactory",
        size=2,
        factory_related_name="game",
    )

    teams = RelatedFactoryList(
        "tests.factories.team.TeamFactory", size=2, factory_related_name="game"
    )
