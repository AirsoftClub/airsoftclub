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
            "latitude": fields[0].latitude,
            "longitude": fields[0].longitude,
            "logo": fields[0].logo,
        },
        {
            "id": fields[1].id,
            "name": fields[1].name,
            "description": fields[1].description,
            "latitude": fields[1].latitude,
            "longitude": fields[1].longitude,
            "logo": fields[1].logo,
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
        "latitude": field.latitude,
        "longitude": field.longitude,
        "logo": field.logo,
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
def test_upload_logo(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/logo",
        files={"logo": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": field.id,
        "name": field.name,
        "description": field.description,
        "latitude": field.latitude,
        "longitude": field.longitude,
        "logo": response.json()["logo"],
    }


def test_upload_logo_unauthorized(client: TestClient):
    response = client.post(
        "/fields/1/logo",
        files={"logo": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_upload_logo_field_not_found(client: TestClient, authenticate_user: User):
    response = client.post(
        "/fields/1/logo",
        files={"logo": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Field not found"}


def test_upload_logo_not_owner(client: TestClient, authenticate_user: User):
    field = FieldFactory()

    response = client.post(
        f"/fields/{field.id}/logo",
        files={"logo": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not the owner of this field"}


def test_upload_logo_invalid_file_type(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/logo",
        files={"logo": ("logo.txt", b"image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}


@mock.patch("builtins.open", mock.mock_open(read_data=b"image"))
@mock.patch("pathlib.Path.mkdir", mock.Mock())
def test_upload_photos(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/photos",
        files={"photos": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "url": f"static/fields/{field.id}/photos/logo.png",
        }
    ]


def test_upload_photos_unauthorized(client: TestClient):
    response = client.post(
        "/fields/1/photos",
        files={"photos": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_upload_photos_field_not_found(client: TestClient, authenticate_user: User):
    response = client.post(
        "/fields/1/photos",
        files={"photos": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Field not found"}


def test_upload_photos_not_owner(client: TestClient, authenticate_user: User):
    field = FieldFactory()

    response = client.post(
        f"/fields/{field.id}/photos",
        files={"photos": ("logo.png", b"image", "image/png")},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not the owner of this field"}


def test_upload_photos_invalid_file_type(client: TestClient, authenticate_user: User):
    field = FieldFactory(owner=authenticate_user)

    response = client.post(
        f"/fields/{field.id}/photos",
        files={"photos": ("logo.txt", b"image", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}
