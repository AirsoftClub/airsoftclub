from app.models.user import User
from fastapi.testclient import TestClient
from tests.factories.game import GameFactory


def test_book_game(client: TestClient, authenticate_user: User):
    game = GameFactory(bookings=[])
    data = {
        "game_id": game.id,
    }

    response = client.post("/bookings", json=data)

    assert response.status_code == 200, response.text

    booking = game.bookings[0]

    assert response.json() == {
        "game_id": game.id,
        "player_id": authenticate_user.id,
        "team_id": booking.team_id,
        "created_at": booking.created_at.isoformat(),
    }


def test_book_game_unauthorized(client: TestClient):
    data = {
        "game_id": 1,
    }

    response = client.post("/bookings", json=data)

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_book_game_game_not_found(client: TestClient, authenticate_user: User):
    data = {
        "game_id": 1,
    }

    response = client.post("/bookings", json=data)

    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Game not found"}


def test_book_game_game_full(client: TestClient, authenticate_user: User):
    game = GameFactory(max_players=1)
    data = {
        "game_id": game.id,
    }

    response = client.post("/bookings", json=data)

    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Game is full"}


def test_book_game_already_booked(client: TestClient, authenticate_user: User):
    game = GameFactory(bookings__player=authenticate_user)

    data = {
        "game_id": game.id,
    }

    response = client.post("/bookings", json=data)

    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Already booked"}


def test_book_game_no_teams_available(client: TestClient, authenticate_user: User):
    game = GameFactory(bookings=[], teams=[])
    data = {
        "game_id": game.id,
    }

    response = client.post("/bookings", json=data)

    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "No teams available"}


def test_leave_game(client: TestClient, authenticate_user: User):
    game = GameFactory(bookings__player=authenticate_user)

    response = client.delete(f"/bookings/{game.bookings[0].id}/")

    assert response.status_code == 204, response.text


def test_leave_game_unauthorized(client: TestClient):
    response = client.delete("/bookings/1/")

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_leave_game_booking_not_found(client: TestClient, authenticate_user: User):
    response = client.delete("/bookings/1/")

    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Booking not found"}


def test_leave_game_forbidden(client: TestClient, authenticate_user: User):
    game = GameFactory()

    response = client.delete(f"/bookings/{game.bookings[0].id}/")

    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Forbidden"}
