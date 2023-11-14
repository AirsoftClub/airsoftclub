from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.models.squad import Squad
from app.models.user import User
from app.permissions.squads import SquadPermissions
from app.repositories.squads import SquadRepository
from app.schemas.files import FileResponse
from app.schemas.squads import SquadResponse, SquadUpsertRequest
from app.schemas.users import UserResponse
from app.security.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[SquadResponse])
def get_squads(
    _: User = Depends(get_current_user), squad_repository: SquadRepository = Depends()
):
    return squad_repository.get_squads()


@router.get("/{id}", response_model=SquadResponse)
def get_squad(
    id: int,
    _: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    return squad


@router.get("/{id}/members", response_model=List[UserResponse])
def get_squad_members(
    id: int,
    _: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    return squad.members


@router.get("/{id}/photos", response_model=List[FileResponse])
def get_squad_photos(
    id: int,
    _: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    return squad.photos


@router.post("/{id}/photos", response_model=List[FileResponse])
def add_squad_photos(
    id: int,
    photos: List[UploadFile],
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    if squad.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner")

    return squad_repository.add_squad_photos(squad, photos)


@router.post("/{id}/avatar")
def add_squad_avatar(
    id: int,
    avatar: UploadFile,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    if squad.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner")

    return squad_repository.add_squad_avatar(squad, avatar)


@router.post("/")
def create_squad(
    request: SquadUpsertRequest,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = Squad(**request.model_dump(), owner_id=current_user.id)

    if squad_repository.get_count_by_name(squad.name):
        raise HTTPException(status_code=400, detail="Squad already exists")

    if (
        squad_repository.get_count_by_owner(squad.owner_id)
        >= SquadPermissions.MAX_OWNED
    ):
        raise HTTPException(
            status_code=400,
            detail=f"You can't create more than {SquadPermissions.MAX_OWNED} squads",
        )

    return squad_repository.upsert_squad(squad)


@router.put("/{id}")
def update_squad(
    id: int,
    request: SquadUpsertRequest,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = Squad(**request.model_dump(), owner_id=current_user.id)

    if not squad_repository.get_squad(id):
        raise HTTPException(status_code=404, detail="Squad not found")

    if squad_repository.get_count_by_name(squad.name):
        raise HTTPException(status_code=400, detail="Squad already exists")

    return squad_repository.upsert_squad(squad)


@router.get("/{id}/invitations", response_model=List[UserResponse])
def get_invited_users(
    id: int,
    _: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    return squad.invitations


@router.delete("/{id}")
def delete_squad(
    id: int,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    squad = squad_repository.get_squad(id)

    if not squad:
        raise HTTPException(status_code=404, detail="Squad not found")

    if squad.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner")

    return squad_repository.delete_squad(squad)
