from factory.alchemy import SQLAlchemyModelFactory
from tests.factories.booking import BookingFactory
from tests.factories.field import FieldFactory
from tests.factories.game import GameFactory
from tests.factories.squad import SquadFactory
from tests.factories.team import TeamFactory
from tests.factories.user import UserFactory

sqlalchemy_factories: list[SQLAlchemyModelFactory] = [
    BookingFactory,
    FieldFactory,
    GameFactory,
    TeamFactory,
    UserFactory,
    SquadFactory,
]

__all__ = [
    "BookingFactory",
    "FieldFactory",
    "GameFactory",
    "TeamFactory",
    "UserFactory",
    "SquadFactory",
]
