from datetime import datetime
from typing import Optional

from app.models.squad import Squad, SquadMember
from factory import Faker, LazyFunction, RelatedFactoryList, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory


class SquadMemberFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SquadMember
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n)


class SquadFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Squad
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n)
    name = Faker("first_name")
    description = Faker("text")
    updated_at = LazyFunction(datetime.now)
    created_at = LazyFunction(datetime.now)
    deleted_at: Optional[datetime] = None

    owner = SubFactory("tests.factories.user.UserFactory")

    members = RelatedFactoryList(
        "tests.factories.squad.SquadMemberFactory",
        factory_related_name="member",
        size=2,
    )
