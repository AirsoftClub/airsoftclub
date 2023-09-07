from datetime import datetime

from app.models.user import User
from app.security.password import Hash
from factory import Faker, LazyFunction, Sequence
from factory.alchemy import SQLAlchemyModelFactory


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n)
    email = Sequence(lambda n: f"email{n}@test.com")
    name = Faker("first_name")
    lastname = Faker("last_name")
    password = Hash.bcrypt("password")
    token = None
    avatar_id = None
    avatar = None
    created_at = LazyFunction(datetime.now)
    updated_at = LazyFunction(datetime.now)
