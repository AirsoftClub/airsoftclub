from pathlib import Path

from app.models.field import Field
from app.models.file import File
from app.models.user import User
from app.repositories.fields import FieldRepository
from app.repositories.users import UserRepository
from app.schemas.fields import FieldDistanceResponse, FieldResponse, FieldUpsertRequest
from app.schemas.files import FileResponse
from app.security.auth import get_admin_user, get_current_user
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic_extra_types.coordinate import Latitude, Longitude

router = APIRouter()


def get_current_field(
    field_id: int,
    field_repository: FieldRepository = Depends(),
) -> Field:
    """
    Returns the field of the corresponding field_id

    Raises 404 if field not found
    """
    field = field_repository.get_by_id(field_id)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    return field


def get_owned_field(
    field: Field = Depends(get_current_field),
    current_user: User = Depends(get_current_user),
) -> Field:
    """
    Returns the field of the corresponding field_id only if the current user owns it.
    Raises 404 if field is not found
    Raises 403 if user is not owner
    """
    if field.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this field"
        )

    return field


@router.get("/", response_model=list[FieldResponse])
def get_fields(
    current_user: User = Depends(get_current_user),
    field_repository: FieldRepository = Depends(),
):
    return field_repository.get_all()


@router.get("/distance", response_model=list[FieldDistanceResponse])
def get_field_by_distance(
    latitude: Latitude,
    longitude: Longitude,
    limit: int = 10,
    field_repository: FieldRepository = Depends(),
):
    return [
        {
            "id": field.id,
            "name": field.name,
            "description": field.description,
            "latitude": field.latitude,
            "longitude": field.longitude,
            "avatar": field.avatar,
            "distance": distance,
        }
        for field, distance in field_repository.get_all_by_distance(
            latitude, longitude, limit
        )
    ]


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(field: Field = Depends(get_current_field)):
    return field


@router.post("/", response_model=FieldResponse)
def create_field(
    payload: FieldUpsertRequest,
    admin: User = Depends(get_admin_user),
    field_repository: FieldRepository = Depends(),
    user_repository: UserRepository = Depends(),
):
    user = user_repository.get_by_email(payload.owner)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if field_repository.get_count_by_name(payload.field.name):
        raise HTTPException(status_code=400, detail="Field already exists")

    return field_repository.create(payload.field, user)


@router.post("/{field_id}/avatar", response_model=FieldResponse)
def upload_avatar(
    avatar: UploadFile,
    field: Field = Depends(get_owned_field),
    field_repository: FieldRepository = Depends(),
):
    if avatar.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    directory = Path(f"static/fields/{field.id}/avatar")

    if not directory.exists():
        directory.mkdir(parents=True)

    path = directory / str(avatar.filename)

    with open(path, "wb") as buffer:
        buffer.write(avatar.file.read())

    field.avatar = File(path=path.as_posix())

    return field_repository.update(field)


@router.post("/{field_id}/photos", response_model=list[FileResponse])
def upload_photos(
    photos: list[UploadFile],
    field: Field = Depends(get_owned_field),
    field_repository: FieldRepository = Depends(),
):
    for photo in photos:
        if photo.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

    directory = Path(f"static/fields/{field.id}/photos")

    if not directory.exists():
        directory.mkdir(parents=True)

    for photo in photos:
        path = directory / str(photo.filename)
        with open(path, "wb") as buffer:
            buffer.write(photo.file.read())

        field.photos.append(File(path=path.as_posix()))

    field_repository.update(field)

    return field.photos
