from app.models.booking import Booking
from factory import Faker, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory


class BookingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Booking
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n)

    created_at = Faker("date_time")
    updated_at = Faker("date_time")

    game = SubFactory("tests.factories.game.GameFactory")

    player = SubFactory("tests.factories.user.UserFactory")

    team = SubFactory("tests.factories.team.TeamFactory")
