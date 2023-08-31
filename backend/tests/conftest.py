from typing import Unpack

import pytest
from app.core.database import get_db
from app.models.base import Base
from fastapi.testclient import TestClient
from main import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from tests.factories.user_factory import UserFactory

from backend.app.schemas.users import UserJWTPayload
from backend.app.security.auth import token_encode

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app = create_app()
app.dependency_overrides[get_db] = override_get_db

test_client = TestClient(app)


@pytest.fixture
def db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def refresh_database():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    yield test_client


@pytest.fixture
def db_user(db: Session, **kwargs: Unpack[UserFactory]):
    user = UserFactory(**kwargs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def db_authorized_user(db: Session, **kwargs: Unpack[UserFactory]):
    user = UserFactory(**kwargs)
    db.add(user)
    db.commit()
    user.token = token_encode(
        UserJWTPayload(
            id=user.id,
            name=user.name,
            lastname=user.lastname,
            email=user.email,
        )
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
