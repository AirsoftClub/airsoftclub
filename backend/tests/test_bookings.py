from datetime import datetime, timedelta

import pytest
from app.models.booking import Booking
from app.models.game import Game
from app.models.team import Team
from app.models.user import User
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.factories.game_factory import GameFactory
from tests.factories.team_factory import TeamFactory


@pytest.mark.usefixtures("refresh_database")
def test_user_can_book_game(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    game: Game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    teams: list[Team] = TeamFactory.create_batch(2)
    [game.teams.append(team) for team in teams]
    db.add(game)
    db.commit()
    db.refresh(game)

    assert len(game.teams) == 2

    response = client.post(
        "/bookings/",
        json={"game_id": game.id},
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 200, response.text

    booking = (
        db.query(Booking)
        .filter(Booking.game_id == game.id, Booking.player_id == db_authorized_user.id)
        .first()
    )

    assert booking is not None, response.text


def test_book_game_unauthorized(client: TestClient) -> None:
    response = client.post("/bookings/", json={"game_id": 1})
    assert response.status_code == 401


def test_book_game_not_found(client: TestClient, db_authorized_user: User) -> None:
    response = client.post(
        "/bookings/",
        json={"game_id": 1},
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 404


@pytest.mark.usefixtures("refresh_database")
def test_book_game_already_booked(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    game: Game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    teams: list[Team] = TeamFactory.create_batch(2)
    [game.teams.append(team) for team in teams]
    db.add(game)
    db.commit()
    db.refresh(game)

    assert len(game.teams) == 2

    booking = Booking(game_id=game.id, player_id=db_authorized_user.id)
    db.add(booking)
    db.commit()
    db.refresh(booking)

    response = client.post(
        "/bookings/",
        json={"game_id": game.id},
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 400, response.text

    booking = (
        db.query(Booking)
        .filter(Booking.game_id == game.id, Booking.player_id == db_authorized_user.id)
        .first()
    )

    assert booking is not None, response.text


@pytest.mark.usefixtures("refresh_database")
def test_book_game_has_no_teams_availables(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    game: Game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    db.add(game)
    db.commit()
    db.refresh(game)

    response = client.post(
        "/bookings/",
        json={"game_id": game.id},
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 400, response.text


@pytest.mark.usefixtures("refresh_database")
def test_user_can_leave_game(
    client: TestClient, db: Session, db_authorized_user: User
) -> None:
    game = GameFactory(played_at=datetime.utcnow() + timedelta(days=1))
    db.add(game)
    db.commit()
    db.refresh(game)

    booking = Booking(game_id=game.id, player_id=db_authorized_user.id)
    db.add(booking)
    db.commit()
    db.refresh(booking)

    response = client.delete(
        f"/bookings/{booking.id}/",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 204

    booking = db.query(Booking).filter(Booking.id == booking.id).first()

    assert booking is None
