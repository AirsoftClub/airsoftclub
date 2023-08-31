from datetime import datetime

import factory
from app.models.user import User
from app.security.password import Hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id: int
    email = factory.Sequence(lambda n: f"email{n}@test.com")
    name = factory.Faker("first_name")
    lastname = factory.Faker("last_name")
    password = Hash.bcrypt("password")
    token = None
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
