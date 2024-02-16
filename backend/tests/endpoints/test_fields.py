from unittest import mock

from app.models.user import User
from fastapi.testclient import TestClient
from tests.factories.field import FieldFactory


def test_get_fields(client: TestClient, authenticate_user: User):
    fields = FieldFactory.create_batch(2)

    response = client.get("/fields")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": fields[0].id,
            "name": fields[0].name,
            "description": fields[0].description,
            "cords_x": fields[0].cords_x,
            "cords_y": fields[0].cords_y,
            "avatar": fields[0].avatar,
        },
        {
            "id": fields[1].id,
            "name": fields[1].name,
            "description": fields[1].description,
            "cords_x": fields[1].cords_x,
            "cords_y": fields[1].cords_y,
            "avatar": fields[1].avatar,
        },
    ]


def test_get_fields_unauthorized(client: TestClient):
    response = client.get("/fields")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_field(client: TestClient, authenticate_user: User):
    field = FieldFactory()

    response = client.get(f"/fields/{field.id}")

    assert response.status_code == 200

    assert response.json() == {
        "id": field.id,
        "name": field.name,
        "description": field.description,
        "cords_x": field.cords_x,
        "cords_y": field.cords_y,
        "avatar": field.avatar,
    }


def test_get_field_unauthorized(client: TestClient):
    response = client.get("/fields/1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_field_not_found(client: TestClient, authenticate_user: User):
    response = client.get("/fields/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Field not found"}


@mock.patch("builtins.open", mock.mock_open(read_data=b"image"))
@mock.patch("pathlib.Path.mkdir", mock.Mock())
def test_upload_avatar(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/avatar",
        files={"avatar": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": field.id,
        "name": field.name,
        "description": field.description,
        "cords_x": field.cords_x,
        "cords_y": field.cords_y,
        "avatar": response.json()["avatar"],
    }


def test_upload_avatar_unauthorized(client: TestClient):
    response = client.post(
        "/fields/1/avatar",
        files={"avatar": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_upload_avatar_field_not_found(client: TestClient, authenticate_user: User):
    response = client.post(
        "/fields/1/avatar",
        files={"avatar": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Field not found"}


def test_upload_avatar_not_owner(client: TestClient, authenticate_user: User):
    field = FieldFactory()

    response = client.post(
        f"/fields/{field.id}/avatar",
        files={"avatar": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not the owner of this field"}


def test_upload_avatar_invalid_file_type(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/avatar",
        files={"avatar": ("avatar.txt", b"image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}


@mock.patch("builtins.open", mock.mock_open(read_data=b"image"))
@mock.patch("pathlib.Path.mkdir", mock.Mock())
def test_upload_photos(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/photos",
        files={"photos": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "url": f"static/fields/{field.id}/photos/avatar.png",
        }
    ]


def test_upload_photos_unauthorized(client: TestClient):
    response = client.post(
        "/fields/1/photos",
        files={"photos": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_upload_photos_field_not_found(client: TestClient, authenticate_user: User):
    response = client.post(
        "/fields/1/photos",
        files={"photos": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Field not found"}


def test_upload_photos_not_owner(client: TestClient, authenticate_user: User):
    field = FieldFactory()

    response = client.post(
        f"/fields/{field.id}/photos",
        files={"photos": ("avatar.png", b"image", "image/png")},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not the owner of this field"}


def test_upload_photos_invalid_file_type(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/photos",
        files={"photos": ("avatar.txt", b"image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}
