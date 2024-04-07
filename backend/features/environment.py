from urllib.parse import urlparse

from app.core.database import get_db
from app.core.settings import Settings
from app.models.base import Base
from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from main import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@fixture
def engine(context):
    """
    Fixture function to create a SQLAlchemy engine for testing.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This fixture directly modifies the context by adding an SQLAlchemy engine object.
    """
    test_db_name = "airsoftclub_back_test"
    db_settings = Settings()
    db_url = urlparse(str(db_settings.database_url))
    context.engine = create_engine(
        db_url._replace(path=f"/{test_db_name}").geturl(),
    )


@fixture
def session(context):
    """
    Fixture function to create a SQLAlchemy session for testing.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This fixture directly modifies the context by adding a SQLAlchemy session object.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=context.engine)
    context.session = SessionLocal()


@fixture
def reset_db(context):
    """
    Fixture function to reset the test database schema.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This fixture directly modifies the test database schema.
    """
    Base.metadata.drop_all(bind=context.engine)
    Base.metadata.create_all(bind=context.engine)


def before_all(context):
    """
    Before all tests, setup the SQLAlchemy engine fixture.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This function sets up the SQLAlchemy engine fixture.
    """
    use_fixture(engine, context)


def after_all(context):
    """
    After all tests, dispose of the SQLAlchemy engine.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This function disposes of the SQLAlchemy engine.
    """
    use_fixture(reset_db, context)
    context.engine.dispose()


def before_scenario(context, _):
    """
    Before each scenario, setup the SQLAlchemy session and FastAPI app fixture.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This function sets up the SQLAlchemy session and FastAPI app fixture.
    """
    use_fixture(session, context)
    use_fixture(reset_db, context)
    context.app = create_app()
    context.app.dependency_overrides[get_db] = lambda: context.session
    context.client = TestClient(context.app)


def after_scenario(context, _):
    """
    After each scenario, close the SQLAlchemy session.

    Args:
        context (Context): Behave context object.

    Returns:
        None: This function closes the SQLAlchemy session.
    """
    context.session.close_all()
