import pytest
from app.models.user import User
from app.security.password import Hash
from fastapi.testclient import TestClient


@pytest.mark.usefixtures("refresh_database")
def test_user_can_register(client: TestClient):
    response = client.post(
        "/users/register/",
        json={
            "name": "John",
            "lastname": "Doe",
            "email": "john@doe.com",
            "password": "password",
        },
    )
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("refresh_database")
@pytest.mark.parametrize(
    "db_user", [{"password": Hash.bcrypt("password")}], indirect=True
)
def test_user_can_login(client: TestClient, db_user: User):
    response = client.post(
        "/users/login/", json={"email": db_user.email, "password": "password"}
    )
    assert response.status_code == 200, response.text
    assert response.json()["token"] is not None, response.text


@pytest.mark.usefixtures("refresh_database")
@pytest.mark.parametrize(
    "db_user", [{"password": Hash.bcrypt("password")}], indirect=True
)
def test_user_login_404_when_incorrect_password(client: TestClient, db_user: User):
    response = client.post(
        "/users/login/", json={"email": db_user.email, "password": "incorrect"}
    )
    assert response.status_code == 404, response.text


def test_user_login_404_when_user_dont_exists(client: TestClient):
    response = client.post(
        "/users/login/", json={"email": "fake@email.com", "password": "password"}
    )
    assert response.status_code == 404, response.text


def test_invalid_token_401(client: TestClient):
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {'fake_token'}"}
    )
    assert response.status_code == 401, response.text


def test_get_users_requires_authorization(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 401, response.text


@pytest.mark.usefixtures("refresh_database")
def test_get_users(client: TestClient, db_authorized_user: User):
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {db_authorized_user.token}"}
    )
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1, response.text


@pytest.mark.usefixtures("refresh_database")
def test_get_user_by_id(client: TestClient, db_authorized_user: User):
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["id"] == db_authorized_user.id, response.text
