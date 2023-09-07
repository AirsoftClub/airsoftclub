from app.models.user import User
from fastapi.testclient import TestClient
from tests.factories.game import GameFactory


def test_get_joinable_games(client: TestClient, authenticate_user: User):
    games = GameFactory.create_batch(2)

    response = client.get("/games")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": games[0].id,
            "name": games[0].name,
            "description": games[0].description,
            "played_at": games[0].played_at.isoformat(),
            "created_at": games[0].created_at.isoformat(),
        },
        {
            "id": games[1].id,
            "name": games[1].name,
            "description": games[1].description,
            "played_at": games[1].played_at.isoformat(),
            "created_at": games[1].created_at.isoformat(),
        },
    ]


def test_get_joinable_games_unauthorized(client: TestClient):
    response = client.get("/games")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_game(client: TestClient, authenticate_user: User):
    game = GameFactory()

    response = client.get(f"/games/{game.id}")

    assert response.status_code == 200

    assert response.json() == {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "played_at": game.played_at.isoformat(),
        "created_at": game.created_at.isoformat(),
    }


def test_get_game_unauthorized(client: TestClient):
    response = client.get("/games/1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_game_not_found(client: TestClient, authenticate_user: User):
    response = client.get("/games/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}


def test_get_game_bookings(client: TestClient, authenticate_user: User):
    game = GameFactory()

    response = client.get(f"/games/{game.id}/bookings")

    assert response.status_code == 200

    assert response.json() == [
        {
            "game_id": game.bookings[0].game_id,
            "player_id": game.bookings[0].player_id,
            "team_id": game.bookings[0].team_id,
            "created_at": game.bookings[0].created_at.isoformat(),
        },
        {
            "game_id": game.bookings[1].game_id,
            "player_id": game.bookings[1].player_id,
            "team_id": game.bookings[1].team_id,
            "created_at": game.bookings[1].created_at.isoformat(),
        },
    ]


def test_get_game_bookings_unauthorized(client: TestClient):
    response = client.get("/games/1/bookings")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_game_bookings_not_found(client: TestClient, authenticate_user: User):
    response = client.get("/games/1/bookings")

    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}


def test_get_game_teams(client: TestClient, authenticate_user: User):
    game = GameFactory()

    response = client.get(f"/games/{game.id}/teams")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": game.teams[0].id,
            "name": game.teams[0].name,
            "created_at": game.teams[0].created_at.isoformat(),
            "updated_at": game.teams[0].updated_at.isoformat(),
        },
        {
            "id": game.teams[1].id,
            "name": game.teams[1].name,
            "created_at": game.teams[1].created_at.isoformat(),
            "updated_at": game.teams[1].updated_at.isoformat(),
        },
    ]


def test_get_game_teams_unauthorized(client: TestClient):
    response = client.get("/games/1/teams")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_game_teams_not_found(client: TestClient, authenticate_user: User):
    response = client.get("/games/1/teams")

    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}
