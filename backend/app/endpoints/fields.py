from pathlib import Path

from app.models.file import File
from app.models.user import User
from app.repositories.fields import FieldRepository
from app.schemas.fields import FieldResponse
from app.schemas.files import FileResponse
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, UploadFile

router = APIRouter()


@router.get("/", response_model=list[FieldResponse])
def get_fields(
    current_user: User = Depends(get_current_user),
    field_repository: FieldRepository = Depends(),
):
    return field_repository.get_all()


@router.get("/{id}", response_model=FieldResponse)
def get_field(
    id: int,
    current_user: User = Depends(get_current_user),
    field_repository: FieldRepository = Depends(),
):
    field = field_repository.get_by_id(id)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    return field


@router.post("/{id}/avatar", response_model=FieldResponse)
def upload_avatar(
    id: int,
    avatar: UploadFile,
    current_user: User = Depends(get_current_user),
    field_repository: FieldRepository = Depends(),
):
    field = field_repository.get_by_id(id)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if field.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this field"
        )

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


@router.post("/{id}/photos", response_model=list[FileResponse])
def upload_photos(
    photos: list[UploadFile],
    id: int,
    current_user: User = Depends(get_current_user),
    field_repository: FieldRepository = Depends(),
):
    field = field_repository.get_by_id(id)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if field.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this field"
        )

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
