from datetime import datetime, timedelta

import pytest
from app.models.booking import Booking
from app.models.game import Game
from app.models.team import Team
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.factories.booking_factory import BookingFactory
from tests.factories.game_factory import GameFactory
from tests.factories.team_factory import TeamFactory


@pytest.mark.usefixtures("refresh_database")
def test_get_joinable_games(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    games = GameFactory.create_batch(
        10, played_at=datetime.utcnow() + timedelta(days=1)
    )

    db.add_all(games)
    db.commit()

    response = client.get(
        "/games/", headers={"Authorization": f"Bearer {db_authorized_user.token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == len(games)


def test_get_joinable_games_unauthorized(client: TestClient) -> None:
    response = client.get("/games/")
    assert response.status_code == 401


@pytest.mark.usefixtures("refresh_database")
def test_get_game(client: TestClient, db: Session, db_authorized_user: User) -> None:
    game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    db.add(game)
    db.commit()
    db.refresh(game)

    response = client.get(
        f"/games/{game.id}/",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["id"] == game.id, response.text


def test_get_game_unauthorized(client: TestClient) -> None:
    response = client.get("/games/1/")
    assert response.status_code == 401


def test_get_game_not_found(client: TestClient, db_authorized_user: User) -> None:
    response = client.get(
        "/games/1/", headers={"Authorization": f"Bearer {db_authorized_user.token}"}
    )
    assert response.status_code == 404


@pytest.mark.usefixtures("refresh_database")
def test_get_game_bookings(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    game: Game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    team: Team = TeamFactory.create()
    booking: Booking = BookingFactory.create(
        game_id=game.id, player_id=db_authorized_user.id, team_id=1
    )
    game.teams.append(team)
    game.bookings.append(booking)
    db.add(game)
    db.commit()
    db.refresh(game)

    response = client.get(
        f"/games/{game.id}/bookings/",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1, response.text


def test_get_game_bookings_unauthorized(client: TestClient, db: Session) -> None:
    response = client.get("/games/1/bookings/")
    assert response.status_code == 401


@pytest.mark.usefixtures("refresh_database")
def test_get_game_teams(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    game: Game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    team: Team = TeamFactory.create()
    game.teams.append(team)
    db.add(game)
    db.commit()
    db.refresh(game)

    response = client.get(
        f"/games/{game.id}/teams/",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1, response.text


def get_game_teams_unauthorized(client: TestClient) -> None:
    response = client.get("/games/1/teams/")
    assert response.status_code == 401
