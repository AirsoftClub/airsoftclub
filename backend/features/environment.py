from app.core.database import get_db
from app.models.base import Base
from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from main import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@fixture
def init_db(context):
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    context.session = SessionLocal()


@fixture
def app(context):
    context.app = create_app()
    context.app.dependency_overrides[get_db] = lambda: context.session


@fixture
def client(context):
    context.client = TestClient(context.app)


def before_scenario(context, scenario):
    use_fixture(init_db, context)
    use_fixture(app, context)
    use_fixture(client, context)
