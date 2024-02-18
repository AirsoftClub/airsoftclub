from unittest import mock

from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from tests.factories.google_token import GoogleTokenFactory
from tests.factories.user import UserFactory


def test_user_register(client: TestClient, db_session: Session):
    response = client.post(
        "/auth/register",
        json={
            "email": "email@test.com",
            "password": "password",
            "name": "name",
            "lastname": "lastname",
        },
    )

    assert response.status_code == 200

    user = db_session.query(User).filter(User.email == "email@test.com").first()

    assert user is not None


def test_user_register_with_existing_email(client: TestClient):
    user = UserFactory()

    response = client.post(
        "/auth/register",
        json={
            "email": user.email,
            "password": "password",
            "name": "name",
            "lastname": "lastname",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_user_can_login(client: TestClient):
    user = UserFactory()

    response = client.post(
        "/auth/login", json={"email": user.email, "password": "password"}
    )

    assert response.status_code == 200


def test_user_cant_login_with_wrong_email(client: TestClient):
    response = client.post(
        "/auth/login", json={"email": "foo@faa.com", "password": "password"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_user_cant_login_with_wrong_password(client: TestClient):
    user = UserFactory()

    response = client.post(
        "/auth/login", json={"email": user.email, "password": "wrong_password"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


@mock.patch(
    "app.endpoints.auth.get_google_user_data",
    mock.MagicMock(return_value=GoogleTokenFactory.create()),
)
def test_google_login(client: TestClient):
    response = client.post(
        "/auth/google/login",
        json={"token": "token"},
    )

    assert response.status_code == 200


@mock.patch(
    "app.endpoints.auth.get_google_user_data",
    mock.MagicMock(return_value=GoogleTokenFactory.create(email_verified=False)),
)
def test_google_login_email_not_verified(client: TestClient):
    response = client.post(
        "/auth/google/login",
        json={"token": "token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Email not verified"}


def test_google_login_with_wrong_token(client: TestClient):
    response = client.post(
        "/auth/google/login",
        json={"token": "wrong_token"},
    )

    assert response.status_code == 401


def test_refresh_token(client: TestClient, db_session: Session):
    user = UserFactory()

    response = client.post(
        "/auth/login", json={"email": user.email, "password": "password"}
    )

    assert response.status_code == 200

    refresh_token = response.json()["refresh_token"]

    print(refresh_token)

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
