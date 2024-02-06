from app.models.user import User
from fastapi.testclient import TestClient
from tests.factories.squad import SquadFactory


def test_get_squads(client: TestClient, authenticate_user: User):
    SquadFactory.create_batch(10)

    response = client.get("/squads")

    assert response.status_code == 200

    assert len(response.json()) == 10


def test_get_squads_unauthorized(client: TestClient):
    response = client.get("/squads")

    assert response.status_code == 401


def test_get_squad(client: TestClient, authenticate_user: User):
    squad = SquadFactory.create()

    response = client.get(f"/squads/{squad.id}")

    assert response.status_code == 200

    assert response.json()["id"] == squad.id


def test_get_squad_not_found(client: TestClient, authenticate_user: User):
    response = client.get("/squads/1")

    assert response.status_code == 404


def test_get_squad_unauthorized(client: TestClient):
    squad = SquadFactory.create()

    response = client.get(f"/squads/{squad.id}")

    assert response.status_code == 401


def test_get_squad_members(client: TestClient, authenticate_user: User):
    squad = SquadFactory(members=[authenticate_user])

    response = client.get(f"/squads/{squad.id}/members")

    assert response.status_code == 200

    assert len(response.json()) == 1
