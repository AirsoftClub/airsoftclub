import pytest
from app.models.field import Field
from app.models.user import User
from app.schemas.users import UserJWTPayload
from app.security.auth import token_encode
from fastapi.testclient import TestClient
from mock import mock_open, patch
from sqlalchemy.orm import Session
from tests.factories.user_factory import UserFactory


@pytest.mark.usefixtures("refresh_database")
def test_fields_get_all(
    client: TestClient, db_authorized_user: User, fields: list
) -> None:
    response = client.get(
        "/fields/", headers={"Authorization": f"Bearer {db_authorized_user.token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == len(fields)


def test_fields_get_all_unauthorized(client: TestClient) -> None:
    response = client.get("/fields/")
    assert response.status_code == 401


@pytest.mark.usefixtures("refresh_database")
def test_fields_get_one(
    client: TestClient, db_authorized_user: User, fields: list[Field]
) -> None:
    response = client.get(
        f"/fields/{fields[0].id}",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == fields[0].id


@pytest.mark.usefixtures("refresh_database")
def test_fields_get_one_unauthorized(client: TestClient, fields: list[Field]) -> None:
    response = client.get(f"/fields/{fields[0].id}")
    assert response.status_code == 401


@pytest.mark.usefixtures("refresh_database")
@patch("builtins.open", mock_open(read_data=b"image"))
@patch("os.makedirs", lambda *args, **kwargs: None)
def test_fields_upload_avatar(
    client: TestClient, db_authorized_user: User, fields: list[Field]
) -> None:
    response = client.post(
        f"/fields/{fields[0].id}/avatar",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
        files={"avatar": ("test.jpg", open("tests/test.png", "rb"), "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["id"] == fields[0].id


@pytest.mark.usefixtures("refresh_database")
def test_fields_upload_avatar_invalid_file_type(
    client: TestClient, db_authorized_user: User, fields: list[Field]
) -> None:
    response = client.post(
        f"/fields/{fields[0].id}/avatar",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
        files={"avatar": ("test.jpg", b"image", "image/gif")},
    )
    assert response.status_code == 400


@pytest.mark.usefixtures("refresh_database")
def test_fields_only_owner_can_upload_avatar(
    client: TestClient, fields: list[Field], db: Session
) -> None:
    new_user = UserFactory()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_user.token = token_encode(
        UserJWTPayload(
            id=new_user.id,
            name=new_user.name,
            lastname=new_user.lastname,
            email=new_user.email,
        )
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = client.post(
        f"/fields/{fields[0].id}/avatar",
        headers={"Authorization": f"Bearer {new_user.token}"},
        files={"avatar": ("test.jpg", b"image", "image/jpeg")},
    )
    assert response.status_code == 403


def test_fields_upload_avatar_requires_authorization(client: TestClient) -> None:
    response = client.post("/fields/1/avatar")
    assert response.status_code == 401


@pytest.mark.usefixtures("refresh_database")
@patch("builtins.open", mock_open(read_data=b"image"))
@patch("os.makedirs", lambda *args, **kwargs: None)
def test_fields_upload_photos(
    client: TestClient, db_authorized_user: User, fields: list[Field]
) -> None:
    response = client.post(
        f"/fields/{fields[0].id}/photos",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
        files={
            "photos": ("test.jpg", open("tests/test.png", "rb"), "image/png"),
        },
    )
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("refresh_database")
def test_fields_upload_photos_field_doesnt_exists(
    client: TestClient, db_authorized_user: User
):
    response = client.post(
        "/fields/1/photos",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
        files={
            "photos": ("test.jpg", b"image", "image/jpeg"),
        },
    )
    assert response.status_code == 404, response.text


def test_fields_upload_photos_requires_authorization(client: TestClient) -> None:
    response = client.post("/fields/1/photos")
    assert response.status_code == 401


@pytest.mark.usefixtures("refresh_database")
def test_fields_upload_photos_invalid_mime_types(
    client: TestClient, db_authorized_user: User, fields: list[Field]
) -> None:
    response = client.post(
        "/fields/1/photos",
        headers={"Authorization": f"Bearer {db_authorized_user.token}"},
        files={
            "photos": ("test.jpg", b"image", "image/gif"),
        },
    )
    assert response.status_code == 400, response.text


@pytest.mark.usefixtures("refresh_database")
def test_fields_only_owner_can_upload_photos(
    client: TestClient, fields: list[Field], db: Session
) -> None:
    new_user = UserFactory()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_user.token = token_encode(
        UserJWTPayload(
            id=new_user.id,
            name=new_user.name,
            lastname=new_user.lastname,
            email=new_user.email,
        )
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = client.post(
        f"/fields/{fields[0].id}/photos",
        headers={"Authorization": f"Bearer {new_user.token}"},
        files={"photos": ("test.jpg", b"image", "image/jpeg")},
    )
    assert response.status_code == 403, response.text
