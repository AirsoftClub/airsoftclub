import mock
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from tests.factories.user import UserFactory


def test_user_register(client: TestClient, db_session: Session):
    response = client.post(
        "/users/register",
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
        "/users/register",
        json={
            "email": user.email,
            "password": "password",
            "name": "name",
            "lastname": "lastname",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_user_can_login(client: TestClient, db_session: Session):
    user = UserFactory()

    response = client.post(
        "/users/login", json={"email": user.email, "password": "password"}
    )

    assert response.status_code == 200

    db_user = db_session.query(User).filter(User.email == user.email).first()

    assert db_user.token == response.json()["token"]


def test_user_cant_login_with_wrong_email(client: TestClient):
    response = client.post(
        "/users/login", json={"email": "wrong_email", "password": "password"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_user_cant_login_with_wrong_password(client: TestClient):
    user = UserFactory()

    response = client.post(
        "/users/login", json={"email": user.email, "password": "wrong_password"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_users(client: TestClient, db_session: Session, authenticate_user: User):
    user = UserFactory()

    response = client.get("/users")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": authenticate_user.id,
            "name": authenticate_user.name,
            "lastname": authenticate_user.lastname,
            "email": authenticate_user.email,
            "avatar": None,
        },
        {
            "id": user.id,
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "avatar": None,
        },
    ]


def test_get_users_unauthorized(client: TestClient):
    response = client.get("/users")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_users_me(client: TestClient, authenticate_user: User):
    response = client.get("/users/me")

    assert response.status_code == 200

    assert response.json() == {
        "id": authenticate_user.id,
        "name": authenticate_user.name,
        "lastname": authenticate_user.lastname,
        "email": authenticate_user.email,
        "avatar": None,
    }


def test_get_users_me_unauthorized(client: TestClient):
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_update_users_me(client: TestClient, authenticate_user: User):
    response = client.post(
        "/users/me",
        json={"name": "new_name", "lastname": "new_lastname"},
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": authenticate_user.id,
        "name": "new_name",
        "lastname": "new_lastname",
        "email": authenticate_user.email,
        "avatar": None,
    }


def test_update_users_me_unauthorized(client: TestClient):
    response = client.post(
        "/users/me",
        json={"name": "new_name", "lastname": "new_lastname"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@mock.patch("builtins.open", mock.mock_open(read_data="data"))
@mock.patch("pathlib.Path.mkdir", mock.Mock())
def test_update_users_me_avatar(client: TestClient, authenticate_user: User):
    response = client.post(
        "/users/me/avatar",
        files={"avatar": ("test.png", open("test.png", "rb"), "image/png")},
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": authenticate_user.id,
        "name": authenticate_user.name,
        "lastname": authenticate_user.lastname,
        "email": authenticate_user.email,
        "avatar": {"url": f"static/avatars/{authenticate_user.id}/test.png"},
    }


@mock.patch("builtins.open", mock.mock_open(read_data="data"))
def test_update_users_me_avatar_unauthorized(client: TestClient):
    response = client.post(
        "/users/me/avatar",
        files={"avatar": ("test.png", open("test.png", "rb"), "image/png")},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@mock.patch("builtins.open", mock.mock_open(read_data="data"))
def test_update_users_me_avatar_invalid_file_type(
    client: TestClient, authenticate_user: User
):
    response = client.post(
        "/users/me/avatar",
        files={"avatar": ("test.txt", open("test.txt", "rb"), "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}
