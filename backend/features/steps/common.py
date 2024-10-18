import yaml
from app.repositories import UserRepository
from app.security.auth import get_current_user
from behave import fixture, step, use_fixture
from deepdiff import DeepDiff
from freezegun import freeze_time


@fixture
def set_freeze_time(context, date):
    with freeze_time(date):
        yield


@step("I do a {verb} request to {url} with the following data")
def request_with_json(context, verb, url):
    json = yaml.safe_load(context.text)
    context.response = getattr(context.client, verb.lower())(
        f"http://localhost{url}", json=json
    )


@step("I do a {verb} request to {url}")
def request(context, verb, url):
    context.response = getattr(context.client, verb.lower())(f"http://localhost{url}")


@step("I get a {status_code:d} response")
def check_response_code(context, status_code):
    actual = context.response.status_code

    assert (
        actual == status_code
    ), f"Expected: {status_code}, Actual: {actual}: {context.response.json()}"


@step("The response JSON is")
def check_response_json(context):
    actual = context.response.json()
    expected = yaml.safe_load(context.text)

    diff = DeepDiff(actual, expected)
    assert not diff, diff.pretty()


@step("I'm logged with the user {email}")
def login_user(context, email):
    user = UserRepository(context.session).get_by_email(email)

    if not user:
        raise ValueError(f"User not found with {email}")

    context.app.dependency_overrides[get_current_user] = lambda: user
    context.current_user = user


@step("The user {email} is an admin")
def set_admin(context, email):
    user = UserRepository(context.session).get_by_email(email)

    if not user:
        raise ValueError(f"User not found with {email}")

    user.is_admin = True
    context.session.add(user)
    context.session.commit()


@step("The following user exists")
def create_user(context):
    request_with_json(context, "post", "/auth/register")
    check_response_code(context, 200)


@step("I create and login the following user")
def create_and_login_user(context):
    create_user(context)
    login_user(context, context.response.json()["email"])


@step("The date is {date}")
def _set_freeze_time(context, date):
    use_fixture(set_freeze_time, context, date)
